from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.db.models import Avg
from django.template.loader import get_template
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, mixins, filters
from rest_framework.decorators import api_view, action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.request import Request

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb import settings
from .filters import TitleFilter
from .models import User, Title, Category, Genre, Review, Comment
from .permissions import IsAdmin, IsAdminOrReadOnly, IsAuthorOrModeratorOrAdminOrReadOnly
from .serializers import UserSerializer, SendEmailSerializer, ConfirmEmailSerializer, TitleReadSerializer, \
    TitleWriteSerializer, CategorySerializer, GenreSerializer, ReviewSerializer, CommentSerializer
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly
                                        )


@api_view(http_method_names=('POST',))
def send_email_confirmation(request):
    serializer = SendEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    user, _ = User.objects.get_or_create(email=email, username=email)
    user.is_active = False
    user.set_unusable_password()
    user.save()
    # сгенерировать код для подтверждения
    token = default_token_generator.make_token(user)

    # отправить письмо с кодом на почту
    subject = 'Код подтверждения для авторизации пользователя'
    from_email = settings.EMAIL_SENT_FORM
    ctx = {'confirmation_code': token}
    html_letter = get_template('email/send_email_confirmation.html').render(context=ctx)
    plain_letter = get_template('email/send_email_confirmation.txt').render(context=ctx)
    letter = EmailMultiAlternatives(subject, plain_letter, from_email, [email])
    letter.attach_alternative(html_letter, 'text/html')
    letter.send()
    return Response('Confirmation mail sent')


@api_view(http_method_names=('POST',))
def confirm_email(request):
    serializer = ConfirmEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    confirmation_code = serializer.data.get('confirmation_code')
    user = get_object_or_404(User, email=email)
    correct_token = default_token_generator.check_token(user, confirmation_code)
    if correct_token:
        user.is_active = True
        user.save()

        token = AccessToken.for_user(user)
        return Response(
            {'token': str(token)},
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {'confirmation_code': "Wrong confirmation code"},
            status=status.HTTP_400_BAD_REQUEST
        )


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    lookup_value_regex = '[A-Za-z0-9@-_.]+'
    permission_classes = [IsAdmin]

    @action(detail=False, methods=['GET', 'PATCH'], permission_classes=[IsAuthenticated])
    def me(self, request: Request, **kwargs):
        user = request.user
        if request.method == 'PATCH':
            serializer = self.get_serializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            # if not user.is_staff:
            #     serializer.save(role=user.role, partial=True)
            # else:
            serializer.save(partial=True)
        else:
            serializer = self.get_serializer(user)

        return Response(serializer.data)


class GetPostDeleteViewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.ListModelMixin,
                           GenericViewSet):
    pass


class GenreViewSet(GetPostDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class CategoryViewSet(GetPostDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class TitlesViewSet(ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg("reviews__score"))
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrModeratorOrAdminOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return Review.objects.filter(title=title.id)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrModeratorOrAdminOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        review = get_object_or_404(Review, pk=self.kwargs['review_id'], title=title)
        return Comment.objects.filter(review=review)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        review = get_object_or_404(Review, pk=self.kwargs['review_id'], title=title)
        serializer.save(author=self.request.user, review=review)

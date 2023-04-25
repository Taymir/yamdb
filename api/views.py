from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from rest_framework import status
from rest_framework.decorators import api_view, action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.request import Request

from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb import settings
from .models import User
from .serializers import UserSerializer, SendEmailSerializer, ConfirmEmailSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly


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
    permission_classes = [IsAuthenticated & IsAdminUser]

    @action(detail=False, methods=['GET', 'PATCH'], permission_classes=[IsAuthenticated])
    def me(self, request: Request, **kwargs):
        user = request.user
        if request.method == 'PATCH':
            serializer = self.get_serializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            if not user.is_staff:
                serializer.save(role=user.role, partial=True)
            else:
                serializer.save(partial=True)
        else:
            serializer = self.get_serializer(user)

        return Response(serializer.data)

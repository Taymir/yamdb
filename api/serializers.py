from rest_framework import serializers

from .models import User, Title, Category, Genre, Review, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'bio', 'email', 'role')


class SendEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ConfirmEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField()


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field='slug',
        queryset=Category.objects.all()
    )

    genre = serializers.SlugRelatedField(
        many=True,
        read_only=False,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    rating = serializers.ReadOnlyField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'  # ('id', 'text', 'author', 'score', 'pub_date')

    author = serializers.SlugRelatedField(read_only=True, slug_field='username')
    title = TitleSerializer(read_only=True)

    def validate(self, attrs):
        if self.context['request'].method == 'POST' and Review.objects.filter(author=self.context['request'].user,
                                                                              title=self.context['view'].kwargs.get(
                                                                                  'title_id')).exists():
            raise serializers.ValidationError("Пользователь уже оставлял отзыв на это произведение")
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

from rest_framework import serializers

from .models import User, Title, Category, Genre, Review, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'username', 'bio', 'email', 'role')


class SendEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ConfirmEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        lookup_field = 'slug'
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        lookup_field = 'slug'
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')


class TitleWriteSerializer(serializers.ModelSerializer):
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

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'text', 'author',
                  'score', 'pub_date')

    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')
    score = serializers.IntegerField(max_value=10, min_value=1)
    # title = TitleWriteSerializer(read_only=True)

    def validate(self, attrs):
        if self.context['request'].method == 'POST' and Review.objects.filter(
                author=self.context['request'].user,
                title=self.context['view'].kwargs.get(
                    'title_id')).exists():
            raise serializers.ValidationError(
                "Пользователь уже оставлял отзыв на это произведение")
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

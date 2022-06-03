from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from reviews.models import User, Comments, Review, Title, Category, Genre


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "username", "first_name", "last_name", "email", "role", "bio"
        )


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "email")

    def validate(self, data):
        if data["username"] == "me":
            raise serializers.ValidationError(
                'Нельзя создать пользователя с никнеймом - "me"'
            )
        return data


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "confirmation_code")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = "__all__"
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True,
    )

    def create(self, validated_data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        title_id = self.context['view'].kwargs.get('title_id')
        if Review.objects.filter(
                title=title,
                author=author).exists():
            raise serializers.ValidationError('нельзя оставить отзыв дважды')
        return Review.objects.create(**validated_data)

    def validate_score(self, value):
        if 0 >= value >= 10:
            raise serializers.ValidationError('Проверьте оценку')
        return value

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
        read_only_fields = ('id', 'author', 'title')


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )

    class Meta:
        model = Comments
        fields = '__all__'
        read_only_fields = ('id', 'review')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('name', 'slug')

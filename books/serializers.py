from datetime import timedelta
from rest_framework import serializers
from .models import Author, Genre, Book , Borrow
from django.utils import timezone

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        model = Book
        fields = '__all__'

class BookCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'



class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        fields = ['id', 'user', 'book', 'borrowed_at']
        read_only_fields = ['id', 'user', 'borrowed_at']

    def validate(self, attrs):
        user = self.context['request'].user
        book = attrs.get('book')

        # Check if this user has already borrowed this book and not returned it
        already_borrowed = Borrow.objects.filter(user=user, book=book, returned_at__isnull=True).exists()
        if already_borrowed:
            raise serializers.ValidationError("You have already borrowed this book and haven't returned it.")
        active_borrows = Borrow.objects.filter(user=user, returned_at__isnull=True).count()
        if active_borrows >= 3:
            raise serializers.ValidationError("Borrow limit reached (max 3 books). Return some books first.")

        return attrs

    def create(self, validated_data):
        # Ensure user is automatically set from request
        request = self.context.get('request')
        validated_data['user'] = request.user
        validated_data['due_date'] = timezone.now().date() + timedelta(days=14)  # 2 weeks
        return super().create(validated_data)

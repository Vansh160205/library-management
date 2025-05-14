from rest_framework import generics, permissions
from rest_framework.mixins import Response
from .models import Book
from .serializers import BookSerializer, BookCreateUpdateSerializer
from django.utils import timezone
from rest_framework import generics
from .models import Author, Genre, Borrow
from .serializers import AuthorSerializer, GenreSerializer, BorrowSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from accounts.permissions import IsLibrarian
from .utils.ai_recommender import get_ai_recommendations


class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Public

class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Public

class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookCreateUpdateSerializer
    permission_classes = [IsLibrarian]

    def perform_create(self, serializer):
        serializer.save()

class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookCreateUpdateSerializer
    permission_classes = [IsLibrarian]

class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookCreateUpdateSerializer
    permission_classes = [IsLibrarian]


class AuthorListCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsLibrarian]

class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsLibrarian]

class   GenreListCreateView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsLibrarian]


class GenreDeleteView(generics.DestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsLibrarian]

class GenreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsLibrarian]

class BorrowBookView(generics.CreateAPIView):
    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer
    permission_classes = [permissions.IsAuthenticated]

class CurrentBorrowedBooksView(generics.ListAPIView):
    serializer_class = BorrowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Borrow.objects.filter(user=self.request.user, returned_at__isnull=True)

class ReturnBookView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            borrow = Borrow.objects.get(pk=pk, user=request.user, returned_at__isnull=True)
        except Borrow.DoesNotExist:
            return Response({"error": "Borrow record not found or already returned."}, status=404)

        borrow.returned_at = timezone.now()
        borrow.save()

        return Response({"message": "Book returned successfully."})
    

class RecommendBooksView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        # Get genres of books the user has borrowed before
        borrowed_books = Borrow.objects.filter(user=user).select_related('book')
        genres = borrowed_books.values_list('book__genre', flat=True).distinct()


        # Recommend books in those genres that the user hasn't borrowed
        borrowed_book_ids = Borrow.objects.filter(user=user,returned_at__isnull=True).values_list('book_id', flat=True)
        recommended_books = Book.objects.filter(genre__in=genres).exclude(id__in=borrowed_book_ids)[:10]

        serializer = BookSerializer(recommended_books, many=True)
        return Response(serializer.data)


class AIRecommendBooksView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        # Get user’s borrowed book titles
        borrowed_books = Borrow.objects.filter(user=user).select_related('book')
        book_titles = borrowed_books.values_list('book__title', flat=True)

        if not book_titles:
            return Response({"detail": "No borrowed books found."})

        # Get AI recommendations based on user's borrowed books
        ai_recommendations = get_ai_recommendations(book_titles)

        # Extract book titles from AI recommendations
        recommended_books = ai_recommendations.split('\n')

        # Find books from the recommendations that are available in the library
        available_books = Book.objects.filter(title__in=recommended_books)

        # If some books aren't available, recommend similar available books
        unavailable_books = set(recommended_books) - set(available_books.values_list('title', flat=True))

        if unavailable_books:
            # Find alternative books from the same genres
            genres = Book.objects.filter(title__in=recommended_books).values_list('genre', flat=True)
            alternative_books = Book.objects.filter(genre__in=genres).exclude(title__in=recommended_books)[:5]

            # Add the alternatives to the final recommendations
            available_books = available_books | alternative_books

        # Return available books or alternatives
        serializer = BookSerializer(available_books, many=True)
        return Response({
            "recommended_books": serializer.data,
            "unavailable_books": list(unavailable_books),
        })

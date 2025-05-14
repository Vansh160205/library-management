from django.urls import path
from .views import (
    AIRecommendBooksView, AuthorDetailView, BookListView, BookDetailView,
    BookCreateView, BookUpdateView, BookDeleteView,
    AuthorListCreateView, BorrowBookView, CurrentBorrowedBooksView, GenreDeleteView, GenreDetailView, GenreListCreateView, RecommendBooksView, ReturnBookView
)

urlpatterns = [
    path('', BookListView.as_view(), name='book-list'),
    path('<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('create/', BookCreateView.as_view(), name='book-create'),
    path('update/<int:pk>/', BookUpdateView.as_view(), name='book-update'),
    path('delete/<int:pk>/', BookDeleteView.as_view(), name='book-delete'),
    path('authors/', AuthorListCreateView.as_view(), name='author-list-create'),
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),

    path('genres/', GenreListCreateView.as_view(), name='genre-list-create'),
    path('genres/<int:pk>/', GenreDetailView.as_view(), name='genre-detail'),
    path('genres/delete/<int:pk>/', GenreDeleteView.as_view(), name='genre-list-create'),
    
    path('borrow/', BorrowBookView.as_view(), name='borrow-book'),
    path('return/<int:pk>/', ReturnBookView.as_view(), name='return-book'),
    path('borrowed/current/', CurrentBorrowedBooksView.as_view(), name='current-borrowed-books'),

    path('recommend/', RecommendBooksView.as_view(), name='recommend-books'),
    path('recommend/ai/', AIRecommendBooksView.as_view(), name='ai-recommend-books'),


]

from django.shortcuts import render  # Renders HTML templates with context data
from rest_framework import viewsets, status  # viewsets: base classes for API views; status: HTTP status codes
from rest_framework.response import Response  # Standardizes API responses
from rest_framework.decorators import action  # Adds custom actions to viewsets
from django.db.models import Q  # Builds complex database queries (AND/OR logic)
from .models import Book  # Imports the Book model from the current app
from .serializers import BookSerializer  # Imports the serializer for Book model

# Create your views here.
class BookViewSet(viewsets.ModelViewSet):

    """
    ViewSet for managing books in the book catalog application.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned books to a given author,
        by filtering against a 'author' query parameter in the URL.
        """
        queryset = Book.objects.all()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(author__icontains=search)
            )

        return queryset.order_by('-created_at')
    
    def create(self, request, *args, **kwargs):
        """
        Create a new book entry.
        """
        serializer = self.get_serializer(data=request.data)
        print(serializer)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'message': 'Book created successfully',
                    'data': serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'message': 'Book creation failed',
                'errors': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    
    def update(self, request, *args, **kwargs):
        """
        Update an existing book entry.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'message': 'Book updated successfully',
                    'data': serializer.data
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'message': 'Book update failed',
                'errors': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, *args, **kwargs):
        """
        Delete a book entry.
        """
        instance = self.get_object()
        instance.delete()
        return Response(
            {
                'message': 'Book deleted successfully'
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Custom action to get statistics about books.
        Returns the total number of books and the most recent book.
        """
        total_books = Book.objects.count()
        most_recent_book = Book.objects.order_by('-created_at').first()

        stats = {
            'total_books': total_books,
            'most_recent_book': most_recent_book.title if most_recent_book else None
        }

        return Response(
            {
                'message': 'Statistics retrieved successfully',
                'data': stats
            },
            status=status.HTTP_200_OK
        )


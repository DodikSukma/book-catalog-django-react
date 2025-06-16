from django.db import models
"""
This module defines the Book model for the book catalog application.
Classes:
    Book: Represents a book with fields for title, author, cover image URL, description, and timestamps.
Note:
    The Book model includes metadata for verbose naming and default ordering by creation date.
"""

# Create Models Book 
class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name='Book Title')
    author = models.CharField(max_length=100, verbose_name='Author')
    cover = models.URLField(max_length=200, verbose_name='Cover Image URL', blank=True, null=True)
    description = models.TextField(verbose_name='Description', blank=True, null=True)
    created_at = models.DateField(verbose_name='Created At', blank=True, null=True)
    updated_at = models.DateField(verbose_name='Updated At', blank=True, null=True)

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        ordering = ['-created_at']

    def __str__(self):
        return self.title




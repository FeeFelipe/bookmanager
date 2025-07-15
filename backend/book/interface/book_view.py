import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import QuerySet

from book.application.commands.book_commands import BookCommands
from book.application.queries.book_queries import BookQueries
from book.domain.book_entities import Book
from book.interface.serializer.book_input_serializer import BookInputSerializer
from book.interface.serializer.book_output_serializer import BookOutputSerializer


class BookView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.book_commands = BookCommands()
        self.book_queries = BookQueries()
        self.logger = logging.getLogger(__name__)

    def get(self, request, book_id: int = None):
        self.logger.info(f"[BookView] GET /book/{book_id or ''} requested")

        try:
            if book_id:
                book = self.book_queries.get_by_id(book_id)
                if not book:
                    self.logger.warning(f"[BookView] Book {book_id} not found")
                    return Response({"detail": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

                serializer = BookOutputSerializer(book)
                return Response(serializer.data)

            search = request.query_params.get("search")
            if search:
                self.logger.info(f"[BookView] Applying fuzzy search: {search}")
                queryset: QuerySet = self.book_queries.get_queryset()
                books = queryset.annotate(
                    similarity=TrigramSimilarity("title", search)
                ).filter(similarity__gt=0.3).order_by("-similarity")
            else:
                books = self.book_queries.get_all()

            self.logger.info(f"[BookView] Returned {len(books)} books")
            serializer = BookOutputSerializer(books, many=True)
            return Response(serializer.data)

        except Exception:
            if book_id:
                self.logger.exception(f"[BookView] Error retrieving book {book_id}")
                return Response({"detail": "Error retrieving book"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            self.logger.exception("[BookView] Error retrieving book list")
            return Response({"detail": "Error retrieving book list"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        self.logger.info(f"[BookView] POST /book | Request data: {request.data}")
        serializer = BookInputSerializer(data=request.data, context={'request': request})

        if not serializer.is_valid():
            self.logger.warning(f"[BookView] POST validation failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            book_entity = Book(**serializer.validated_data)
            book = self.book_commands.create(book_entity)
            output = BookOutputSerializer(book)
            self.logger.info(f"[BookView] Book created successfully: {output.data}")
            return Response(output.data, status=status.HTTP_201_CREATED)
        except Exception:
            self.logger.exception(f"[BookView] Error creating book")
            return Response({"detail": "Error creating book"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, book_id: int):
        self.logger.info(f"[BookView] PUT /book/{book_id} | Request data: {request.data}")
        serializer = BookInputSerializer(data=request.data, context={'request': request})

        if not serializer.is_valid():
            self.logger.warning(f"[BookView] PUT validation failed for {book_id}: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            book_entity = Book(**serializer.validated_data)
            book = self.book_commands.update(book_id, book_entity)
            output = BookOutputSerializer(book)
            self.logger.info(f"[BookView] Book {book_id} updated successfully")
            return Response(output.data)
        except ValueError:
            self.logger.warning(f"[BookView] Book {book_id} not found for update")
            return Response({"detail": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            self.logger.exception(f"[BookView] Error updating book {book_id}")
            return Response({"detail": "Error updating book"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, book_id: int):
        self.logger.info(f"[BookView] DELETE /book/{book_id} requested")
        try:
            self.book_commands.delete(book_id)
            self.logger.info(f"[BookView] Book {book_id} deleted successfully")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError:
            self.logger.warning(f"[BookView] Book {book_id} not found for deletion")
            return Response({"detail": "Book not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            self.logger.exception(f"[BookView] Error deleting book {book_id}")
            return Response({"detail": "Error deleting book"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

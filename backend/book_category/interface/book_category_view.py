import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from book_category.application.commands.book_category_commands import BookCategoryCommands
from book_category.application.queries.book_category_queries import BookCategoryQueries
from book_category.domain.book_category_entities import BookCategory
from book_category.interface.serializer.book_category_input_serializer import BookCategoryInputSerializer
from book_category.interface.serializer.book_category_output_serializer import BookCategoryOutputSerializer


class BookCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.book_category_commands = BookCategoryCommands()
        self.book_category_queries = BookCategoryQueries()
        self.logger = logging.getLogger(__name__)

    def get(self, request, book_category_id: int = None):
        if book_category_id:
            self.logger.info(f"[BookCategoryView] GET /bookcategory/{book_category_id} requested")
            try:
                book_category = self.book_category_queries.get_by_id(book_category_id)
                if book_category:
                    self.logger.info(f"[BookCategoryView] BookCategory {book_category_id} found")
                    serializer = BookCategoryOutputSerializer(book_category)
                    return Response(serializer.data)
                self.logger.warning(f"[BookCategoryView] BookCategory {book_category_id} not found")
                return Response({"detail": "BookCategory not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception:
                self.logger.exception(f"[BookCategoryView] Error retrieving book {book_category_id}")
                return Response({"detail": "Error retrieving book"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        self.logger.info("[BookCategoryView] GET /bookcategory list requested")
        try:
            book_categories = self.book_category_queries.get_all()
            self.logger.info(f"[BookCategoryView] Returned {len(book_categories)} book categories")
            serializer = BookCategoryOutputSerializer(book_categories, many=True)
            return Response(serializer.data)
        except Exception:
            self.logger.exception(f"[BookCategoryView] Error retrieving book category list")
            return Response({"detail": "Error retrieving book category list"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        self.logger.info(f"[BookCategoryView] POST /bookcategory | Request data: {request.data}")
        serializer = BookCategoryInputSerializer(data=request.data, context={'request': request})

        if not serializer.is_valid():
            self.logger.warning(f"[BookCategoryView] POST validation failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            book_category_entity = BookCategory(**serializer.validated_data)
            book_category = self.book_category_commands.create(book_category_entity)
            output = BookCategoryOutputSerializer(book_category)
            self.logger.info(f"[BookCategoryView] BookCategory created successfully: {output.data}")
            return Response(output.data, status=status.HTTP_201_CREATED)
        except Exception:
            self.logger.exception(f"[BookCategoryView] Error creating book category")
            return Response({"detail": "Error creating book category"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, book_category_id: int):
        self.logger.info(f"[BookCategoryView] PUT /bookcategory/{book_category_id} | Request data: {request.data}")
        serializer = BookCategoryInputSerializer(data=request.data, context={'request': request})

        if not serializer.is_valid():
            self.logger.warning(f"[BookCategoryView] PUT validation failed for {book_category_id}: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            book_category_entity = BookCategory(**serializer.validated_data)
            book_category = self.book_category_commands.update(book_category_id, book_category_entity)
            output = BookCategoryOutputSerializer(book_category)
            self.logger.info(f"[BookCategoryView] BookCategory {book_category_id} updated successfully")
            return Response(output.data)
        except ValueError:
            self.logger.warning(f"[BookCategoryView] BookCategory {book_category_id} not found for update")
            return Response({"detail": "BookCategory not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            self.logger.exception(f"[BookCategoryView] Error updating book category {book_category_id}")
            return Response({"detail": "Error updating book category"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, book_category_id: int):
        self.logger.info(f"[BookCategoryView] DELETE /bookcategory/{book_category_id} requested")
        try:
            self.book_category_commands.delete(book_category_id)
            self.logger.info(f"[BookCategoryView] BookCategory {book_category_id} deleted successfully")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError:
            self.logger.warning(f"[BookCategoryView] BookCategory {book_category_id} not found for deletion")
            return Response({"detail": "BookCategory not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            self.logger.exception(f"[BookCategoryView] Error deleting book category {book_category_id}")
            return Response({"detail": "Error deleting book category"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from book_stock.application.commands.book_stock_commands import BookStockCommands
from book_stock.application.queries.book_stock_queries import BookStockQueries
from book_stock.domain.book_stock_entities import BookStock
from book_stock.interface.serializer.book_stock_input_serializer import BookStockInputSerializer
from book_stock.interface.serializer.book_stock_output_serializer import BookStockOutputSerializer


class BookStockView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stock_commands = BookStockCommands()
        self.stock_queries = BookStockQueries()
        self.logger = logging.getLogger(__name__)

    def get(self, request, book_stock_id: int = None):
        if book_stock_id:
            self.logger.info(f"[BookStockView] GET /book_stock/{book_stock_id} requested")
            try:
                book_stock = self.stock_queries.get_by_id(book_stock_id)
                if book_stock:
                    self.logger.info(f"[BookStockView] BookStock {book_stock_id} found")
                    serializer = BookStockOutputSerializer(book_stock)
                    return Response(serializer.data)
                self.logger.warning(f"[BookStockView] BookStock {book_stock_id} not found")
                return Response({"detail": "BookStock not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception:
                self.logger.exception(f"[BookStockView] Error retrieving book_stock {book_stock_id}")
                return Response({"detail": "Error retrieving book_stock"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        self.logger.info("[BookStockView] GET /bookstock list requested")
        try:
            book_stocks = self.stock_queries.get_all()
            self.logger.info(f"[BookStockView] Returned {len(book_stocks)} stocks")
            serializer = BookStockOutputSerializer(book_stocks, many=True)
            return Response(serializer.data)
        except Exception:
            self.logger.exception(f"[BookStockView] Error retrieving book_stock list")
            return Response({"detail": "Error retrieving book_stock list"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        self.logger.info(f"[BookStockView] POST /bookstock | Request data: {request.data}")
        serializer = BookStockInputSerializer(data=request.data, context={'request': request})

        if not serializer.is_valid():
            self.logger.warning(f"[BookStockView] POST validation failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            book_stock_entity = BookStock(**serializer.validated_data)
            book_stock = self.stock_commands.create(book_stock_entity)
            output = BookStockOutputSerializer(book_stock)
            self.logger.info(f"[BookStockView] BookStock created successfully: {output.data}")
            return Response(output.data, status=status.HTTP_201_CREATED)
        except Exception:
            self.logger.exception(f"[BookStockView] Error creating book_stock")
            return Response({"detail": "Error creating book_stock"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, book_stock_id: int):
        self.logger.info(f"[BookStockView] PUT /book_stock/{book_stock_id} | Request data: {request.data}")
        serializer = BookStockInputSerializer(data=request.data, context={'request': request})

        if not serializer.is_valid():
            self.logger.warning(f"[BookStockView] PUT validation failed for {book_stock_id}: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            book_stock_entity = BookStock(**serializer.validated_data)
            book_stock = self.stock_commands.update(book_stock_id, book_stock_entity)
            output = BookStockOutputSerializer(book_stock)
            self.logger.info(f"[BookStockView] BookStock {book_stock_id} updated successfully")
            return Response(output.data)
        except ValueError:
            self.logger.warning(f"[BookStockView] BookStock {book_stock_id} not found for update")
            return Response({"detail": "BookStock not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            self.logger.exception(f"[BookStockView] Error updating book_stock {book_stock_id}")
            return Response({"detail": "Error updating book_stock"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, book_stock_id: int):
        self.logger.info(f"[BookStockView] DELETE /book_stock/{book_stock_id} requested")
        try:
            self.stock_commands.delete(book_stock_id)
            self.logger.info(f"[BookStockView] BookStock {book_stock_id} deleted successfully")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError:
            self.logger.warning(f"[BookStockView] BookStock {book_stock_id} not found for deletion")
            return Response({"detail": "BookStock not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            self.logger.exception(f"[BookStockView] Error deleting book_stock {book_stock_id}")
            return Response({"detail": "Error deleting book_stock"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

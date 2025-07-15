import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from author.application.commands.author_commands import AuthorCommands
from author.application.queries.author_queries import AuthorQueries
from author.domain.author_entities import Author
from author.interface.serializer.author_input_serializer import AuthorInputSerializer
from author.interface.serializer.author_output_serializer import AuthorOutputSerializer


class AuthorView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.author_commands = AuthorCommands()
        self.author_queries = AuthorQueries()
        self.logger = logging.getLogger(__name__)

    def get(self, request, author_id: int = None):
        if author_id:
            self.logger.info(f"[AuthorView] GET /author/{author_id} requested")
            try:
                author = self.author_queries.get_by_id(author_id)
                if author:
                    self.logger.info(f"[AuthorView] Author {author_id} found")
                    serializer = AuthorOutputSerializer(author)
                    return Response(serializer.data)
                self.logger.warning(f"[AuthorView] Author {author_id} not found")
                return Response({"detail": "Author not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception:
                self.logger.exception(f"[AuthorView] Error retrieving author {author_id}")
                return Response({"detail": "Error retrieving author"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        self.logger.info("[AuthorView] GET /author list requested")
        try:
            authors = self.author_queries.get_all()
            self.logger.info(f"[AuthorView] Returned {len(authors)} authors")
            serializer = AuthorOutputSerializer(authors, many=True)
            return Response(serializer.data)
        except Exception:
            self.logger.exception("[AuthorView] Error retrieving author list")
            return Response({"detail": "Error retrieving author list"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        self.logger.info(f"[AuthorView] POST /author | Request data: {request.data}")
        serializer = AuthorInputSerializer(data=request.data, context={'request': request})

        if not serializer.is_valid():
            self.logger.warning(f"[AuthorView] POST validation failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            author_entity = Author(**serializer.validated_data)
            author = self.author_commands.create(author_entity)
            output = AuthorOutputSerializer(author)
            self.logger.info(f"[AuthorView] Author created successfully: {output.data}")
            return Response(output.data, status=status.HTTP_201_CREATED)
        except Exception:
            self.logger.exception(f"[AuthorView] Unexpected error creating author")
            return Response({"detail": "Error creating author"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, author_id: int):
        self.logger.info(f"[AuthorView] PUT /author/{author_id} | Request data: {request.data}")
        serializer = AuthorInputSerializer(data=request.data, context={'request': request})

        if not serializer.is_valid():
            self.logger.warning(f"[AuthorView] PUT validation failed for {author_id}: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            author_entity = Author(**serializer.validated_data)
            author = self.author_commands.update(author_id, author_entity)
            output = AuthorOutputSerializer(author)
            self.logger.info(f"[AuthorView] Author {author_id} updated successfully")
            return Response(output.data)
        except ValueError:
            self.logger.warning(f"[AuthorView] Author {author_id} not found for update")
            return Response({"detail": "Author not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            self.logger.exception(f"[AuthorView] Error updating author {author_id}")
            return Response({"detail": "Error updating author"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, author_id: int):
        self.logger.info(f"[AuthorView] DELETE /author/{author_id} requested")
        try:
            self.author_commands.delete(author_id)
            self.logger.info(f"[AuthorView] Author {author_id} deleted successfully")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError:
            self.logger.warning(f"[AuthorView] Author {author_id} not found for deletion")
            return Response({"detail": "Author not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            self.logger.exception(f"[AuthorView] Error deleting author {author_id}")
            return Response({"detail": "Error deleting author"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

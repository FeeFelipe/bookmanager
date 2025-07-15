import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from branch.application.commands.branch_commands import BranchCommands
from branch.application.queries.branch_queries import BranchQueries
from branch.domain.branch_entities import Branch
from branch.interface.serializer.branch_input_serializer import BranchInputSerializer
from branch.interface.serializer.branch_output_serializer import BranchOutputSerializer


class BranchView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.branch_commands = BranchCommands()
        self.branch_queries = BranchQueries()
        self.logger = logging.getLogger(__name__)

    def get(self, request, branch_id: int = None):
        if branch_id:
            self.logger.info(f"[BranchView] GET /branch/{branch_id} requested")
            try:
                branch = self.branch_queries.get_by_id(branch_id)
                if branch:
                    self.logger.info(f"[BranchView] Branch {branch_id} found")
                    serializer = BranchOutputSerializer(branch)
                    return Response(serializer.data)
                self.logger.warning(f"[BranchView] Branch {branch_id} not found")
                return Response({"detail": "Branch not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception:
                self.logger.exception(f"[BranchView] Error retrieving branch {branch_id}")
                return Response({"detail": "Error retrieving branch"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        self.logger.info("[BranchView] GET /branch/ list requested")
        try:
            branches = self.branch_queries.get_all()
            self.logger.info(f"[BranchView] Returned {len(branches)} branches")
            serializer = BranchOutputSerializer(branches, many=True)
            return Response(serializer.data)
        except Exception:
            self.logger.exception(f"[BranchView] Error retrieving branch list")
            return Response({"detail": "Error retrieving branch list"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        self.logger.info(f"[BranchView] POST /branch | Request data: {request.data}")
        serializer = BranchInputSerializer(data=request.data, context={'request': request})

        if not serializer.is_valid():
            self.logger.warning(f"[BranchView] POST validation failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            branch_entity = Branch(**serializer.validated_data)
            branch = self.branch_commands.create(branch_entity)
            output = BranchOutputSerializer(branch)
            self.logger.info(f"[BranchView] Branch created successfully: {output.data}")
            return Response(output.data, status=status.HTTP_201_CREATED)
        except Exception:
            self.logger.exception(f"[BranchView] Error creating branch")
            return Response({"detail": "Error creating branch"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, branch_id: int):
        self.logger.info(f"[BranchView] PUT /branch/{branch_id} | Request data: {request.data}")
        serializer = BranchInputSerializer(data=request.data, context={'request': request})

        if not serializer.is_valid():
            self.logger.warning(f"[BranchView] PUT validation failed for {branch_id}: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            branch_entity = Branch(**serializer.validated_data)
            branch = self.branch_commands.update(branch_id, branch_entity)
            output = BranchOutputSerializer(branch)
            self.logger.info(f"[BranchView] Branch {branch_id} updated successfully")
            return Response(output.data)
        except ValueError:
            self.logger.warning(f"[BranchView] Branch {branch_id} not found for update")
            return Response({"detail": "Branch not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            self.logger.exception(f"[BranchView] Error updating branch {branch_id}")
            return Response({"detail": "Error updating branch"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, branch_id: int):
        self.logger.info(f"[BranchView] DELETE /branch/{branch_id} requested")
        try:
            self.branch_commands.delete(branch_id)
            self.logger.info(f"[BranchView] Branch {branch_id} deleted successfully")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError:
            self.logger.warning(f"[BranchView] Branch {branch_id} not found for deletion")
            return Response({"detail": "Branch not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            self.logger.exception(f"[BranchView] Error deleting branch {branch_id}")
            return Response({"detail": "Error deleting branch"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

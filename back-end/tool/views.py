from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from tool.serializers import ToolSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from tool.models import Tool

# CRUD view for tool model
class ToolView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk=None):
        return Tool.objects.get(pk=pk)

    def get(self, request, *args, **kwargs):
        pk = kwargs.pop('pk', None)
        if pk:
            try:
                tool = self.get_object(pk)
                serializer = ToolSerializer(tool)
            except Tool.DoesNotExist:
                return Response({'detail': 'Tool Not Found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            tools = Tool.objects.all()
            serializer = ToolSerializer(tools, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ToolSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        tool = self.get_object(pk)
        serializer = ToolSerializer(tool, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        tool = self.get_object(pk)
        tool.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

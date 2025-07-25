from logging import exception

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from utils import render_data, render_message

from ...models import FileUpload
from ...serializers import FileUploadSerializer


class FileUploadGenericAPIView(GenericAPIView):
    queryset = FileUpload
    serializer_class = FileUploadSerializer
    permission_classes = [IsAuthenticated]


class ListFileUploadView(FileUploadGenericAPIView):

    def get(self, request):
        try:
            queryset = self.queryset.objects.all().order_by('-id')
            serializer = self.serializer_class(queryset, many=True)

            return Response(
                render_data(data=serializer.data, success='true'),
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            return Response(
                render_message(message=str(error), success='false'),
                status=status.HTTP_400_BAD_REQUEST
            )


class DetailFileUploadView(FileUploadGenericAPIView):

    def get(self, request, file_upload_id):
        try:
            file_upload = self.queryset.objects.get(id=file_upload_id)
            serializer = self.serializer_class(file_upload, many=False)

            return Response(
                render_data(data=serializer.data, success='true'),
                status=status.HTTP_200_OK,
            )
        except FileUpload.DoesNotExist:
            return Response(
                render_message(message="File not found.", success='false'),
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as error:
            return Response(
                render_message(message=str(error), success='false'),
                status=status.HTTP_400_BAD_REQUEST
            )


class CreateFileUploadView(FileUploadGenericAPIView):

    def post(self, request):
        try:
            title = request.data['title']
            file = request.FILES['file']
            uploaded_by = request.user

            file_upload = self.queryset.objects.create(
                title=title, file=file,
                uploaded_by=uploaded_by)

            serializer = self.serializer_class(file_upload)

            return Response(
                render_data(data=serializer.data, success='true'),
                status=status.HTTP_201_CREATED
            )
        except Exception as error:
            return Response(
                render_message(message=str(error), success='false'),
                status=status.HTTP_400_BAD_REQUEST
            )


class UpdateFileUploadView(FileUploadGenericAPIView):

    def patch(self, request, file_upload_id):
        try:
            file_upload = self.queryset.objects.get(id=file_upload_id)

            if request.user != file_upload.uploaded_by and not request.user.is_staff:
                return Response(
                    render_message(message="You do not have permission to update this file.", success='false'),
                    status=status.HTTP_403_FORBIDDEN
                )

            serializer = self.serializer_class(
                instance=file_upload, data=request.data, partial=True
            )

            if serializer.is_valid():
                serializer.save()

                return Response(
                    render_data(data=serializer.data, success='true'),
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    render_message(message=serializer.errors, success='false'),
                    status=status.HTTP_400_BAD_REQUEST
                )
        except FileUpload.DoesNotExist:
            return Response(
                render_message(message="File not found.", success='false'),
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as error:
            return Response(
                render_message(message=str(error), success='false'),
                status=status.HTTP_400_BAD_REQUEST
            )


class DeleteFileUploadView(FileUploadGenericAPIView):

    def delete(self, request, file_upload_id):
        try:
            file_upload = self.queryset.objects.get(id=file_upload_id)

            if request.user != file_upload.uploaded_by and not request.user.is_staff:
                return Response(
                    render_message(message="You do not have permission to delete this file.", success='false'),
                    status=status.HTTP_403_FORBIDDEN
                )

            file_upload.delete()

            return Response(
                render_message(message="File has been deleted successfully.", success='true'),
                status=status.HTTP_200_OK
            )
        except FileUpload.DoesNotExist:
            return Response(
                render_message(message="File not found.", success='false'),
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as error:
            return Response(
                render_message(message=str(error), success='false'),
                status=status.HTTP_400_BAD_REQUEST
            )
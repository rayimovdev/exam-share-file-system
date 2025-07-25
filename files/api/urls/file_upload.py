from django.urls import path
from ..views.file_upload import ListFileUploadView, DetailFileUploadView, \
    CreateFileUploadView, UpdateFileUploadView, DeleteFileUploadView

urlpatterns = [
    path('list/', ListFileUploadView.as_view(), name='list-file_upload'),
    path('detail/<int:file_upload_id>/', DetailFileUploadView.as_view(), name='detail-file_upload'),
    path('create/', CreateFileUploadView.as_view(), name='create-file_upload'),
    path('update/<int:file_upload_id>/', UpdateFileUploadView.as_view(), name='update-file_upload'),
    path('delete/<int:file_upload_id>/', DeleteFileUploadView.as_view(), name='delete-file_upload'),
]
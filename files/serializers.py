from rest_framework import serializers

from .models import FileUpload
from users.serializers import UserSerializerWithName

class FileUploadSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializerWithName()

    class Meta:
        model = FileUpload
        fields = [
            'id', 'title', 'file', 'uploaded_by', 'uploaded_at',
        ]
        read_only_fields = ['uploaded_at', 'uploaded_by']

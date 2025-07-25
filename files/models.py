from django.db import models
from django.contrib.auth.views import get_user_model

User = get_user_model()

class FileUpload(models.Model):
    title = models.CharField(max_length=500)
    file = models.FileField(upload_to='file-upload/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title[:50]}  {self.uploaded_at}'

# from django.db import models

# # Create your models here.

# from django.db import models
# from django.contrib.auth.models import User

# class FileUpload(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     file_name = models.CharField(max_length=255)
#     file_url = models.URLField()
#     uploaded_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.file_name

from django.db import models # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.core.validators import FileExtensionValidator # type: ignore

class FileUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(
        upload_to="uploads/", 
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'png', 'docx', 'txt'])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.file.name}"

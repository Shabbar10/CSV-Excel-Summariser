from django.db import models


# Create your models here.
class FileUpload(models.Model):
    file = models.FileField(upload_to="uploads/")
    name = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    summary = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}'s upload at {self.uploaded_at}"

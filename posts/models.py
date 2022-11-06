from django.db import models

# Create your models here.

class Posts(models.Model):
    postId = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name="POSTID",
    )
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title
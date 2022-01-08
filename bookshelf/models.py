from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.fields.CharField(max_length=255)
    surname = models.fields.CharField(max_length=255)
    age = models.fields.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.name} {self.surname}"


class Book(models.Model):
    title = models.fields.CharField(max_length=255)
    description = models.fields.TextField(null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title
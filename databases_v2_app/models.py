from django.db import models


class Author(models.Model):
    """
    Author model class
    """

    name = models.CharField(max_length=255)
    key = models.CharField(
        max_length=255, default=""
    )  # This is the key from the API (like isbn but for authors)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model class
    """

    title = models.CharField(max_length=255, default="")
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE
    )  # One-to-many relationship (An author can have many books, but a book can only have one author)
    isbn = models.CharField(max_length=255, default="")
    publishers = models.CharField(max_length=255, default="")
    number_of_pages = models.IntegerField(default=0)

    def __str__(self):
        return self.title


# class MongoBook(models.Model):
#     """
#     MongoBook model class
#     """

#     # author = models.ForeignKey(Author, on_delete=models.CASCADE)
#     average_rating = models.FloatField(default=0)
#     description = models.TextField(default="")
#     publisher_year = models.IntegerField(default=0)
#     ratings_count = models.IntegerField(default=0)
#     title = models.CharField(max_length=255, default="")

#     class Meta:
#         # Set the database alias to 'mongodb'
#         app_label = "databases_v2_app"
#         db_table = "library_database_collection"

#     def __str__(self):
#         return self.title

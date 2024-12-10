from django.db import models
from django.contrib.auth.models import User  # Import the User model for user-specific bookmarks

# Define the Bookmark model
class Bookmark(models.Model):
    # The ForeignKey relationship indicates that each bookmark is associated with a specific user.
    # If the user is deleted, their bookmarks will also be deleted (on_delete=models.CASCADE).
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # The title of the bookmark. It's a CharField with a maximum length of 255 characters.
    title = models.CharField(max_length=255)

    # The URL for the bookmark. It's a URLField which ensures only valid URLs can be stored.
    url = models.URLField()

    # The created_at field automatically stores the timestamp when the bookmark is created.
    created_at = models.DateTimeField(auto_now_add=True)

    # The __str__ method is used to define how the bookmark object is represented as a string.
    # In this case, it will return the title of the bookmark.
    def __str__(self):
        return self.title

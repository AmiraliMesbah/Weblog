from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Custom user model extending Django's default User model."""

    email = models.EmailField(unique=True)  # Ensure unique email for authentication

    bio = models.TextField(blank=True)  # Short user biography
    website = models.URLField(blank=True)
    date_of_birth = models.DateField(blank=True)
    friends = models.ManyToManyField('self', symmetrical=False, related_name='friends', blank=True)
    joined_date = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    social_links = models.JSONField(blank=True, null=True)

    def __str__(self):
        """Return the username when converting the object to a string."""
        return self.username

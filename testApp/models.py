from django.db import models

class Lecture(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
from django.contrib.auth.models import User

class Review(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lecture} - {self.user}"

from django.conf import settings

class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    lecture = models.ForeignKey(
        "Lecture",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="likes"
    )

    review = models.ForeignKey(
        "Review",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="likes"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "lecture"],
                name="unique_lecture_like"
            ),
            models.UniqueConstraint(
                fields=["user", "review"],
                name="unique_review_like"
            ),
        ]

# testApp/models.py
from django.contrib.auth.models import User

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lecture = models.ForeignKey(
        Lecture, on_delete=models.CASCADE,
        null=True, blank=True
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        null=True, blank=True
    )

    class Meta:
        unique_together = ("user", "lecture", "review")

import uuid

from django.contrib.postgres.fields import CICharField
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_extensions.db.fields import AutoSlugField


class Category(models.Model):
    """The name of words category."""
    id = AutoSlugField(
        populate_from="name",
        primary_key=True,
        max_length=255,
    )
    name = CICharField(
        verbose_name=_("Name"),
        max_length=255,
        unique=True,
    )

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ("name",)

    def __str__(self) -> str:
        return str(self.name)


class Word(models.Model):
    """The word with translate."""
    id = AutoSlugField(
        populate_from="english",
        primary_key=True,
        max_length=255,
    )
    english = CICharField(
        verbose_name=_("Word in english"),
        max_length=255,
        unique=True,
    )
    russian = CICharField(
        verbose_name=_("Word in russian"),
        max_length=255,
    )
    categories = models.ManyToManyField(
        "training.Category",
        related_name="words",
        related_query_name="word",
        blank=False,
    )
    users = models.ManyToManyField(
        "users.User",
        related_name="words",
        related_query_name="word",
        through="UserWord",
    )

    class Meta:
        verbose_name = _("Word")
        verbose_name_plural = _("Words")
        ordering = ("english",)

    def __str__(self) -> str:
        return f"{self.english} - {self.russian}"


class UserWord(models.Model):
    """Intermediate model for user-word relationship.

    Rank says about how user learned this word:
        0 - new word for user
        1-99 - in studying
        100 - studied
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
    )
    word = models.ForeignKey(
        "training.Word",
        on_delete=models.RESTRICT,
        related_name="user_words",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="user_words",
    )
    rank = models.PositiveIntegerField(
        verbose_name=_("Rank"),
        validators=[MaxValueValidator(100)],
        default=0,
    )
    learned_times = models.PositiveIntegerField(
        verbose_name=_("Word learned times"),
        validators=[MaxValueValidator(3)],
        default=0,
    )

    class Meta:
        verbose_name = _("User word")
        verbose_name_plural = _("User words")
        unique_together = ("user", "word")
        ordering = ("rank",)

    def __str__(self):
        return f"{self.user}: {self.word} Rank:{self.rank}/100"

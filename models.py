from django.db import models


class Tag(models.Model):
    class Group(models.TextChoices):
        CATEGORY = "category", "Category"
        EMOTION = "emotion", "Emotion"
        SEASON = "season", "Season / Life Event"
        PERSON = "person", "Person"
        TIME = "time", "Time of Day"

    name = models.CharField(max_length=100)
    slug = models.SlugField()
    group = models.CharField(max_length=20, choices=Group.choices)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ("slug", "group")
        ordering = ["group", "name"]

    def __str__(self):
        return self.name


class PromiseQuerySet(models.QuerySet):
    def search(self, query):
        """Naive icontains search across verse text and tag names.
        Swap for SQLite FTS5 here later without touching callers."""
        return self.filter(
            models.Q(verse_text__icontains=query) | models.Q(tags__name__icontains=query)
        ).distinct()

    def in_group(self, group):
        return self.filter(tags__group=group).distinct()


class Promise(models.Model):
    book = models.CharField(max_length=30)
    chapter = models.PositiveSmallIntegerField()
    verse_start = models.PositiveSmallIntegerField()
    verse_end = models.PositiveSmallIntegerField(null=True, blank=True)
    verse_ref = models.CharField(max_length=50)  # denormalized display, e.g. "Philippians 4:6-7"
    verse_text = models.TextField()
    version = models.CharField(max_length=20, default="NIV")
    tags = models.ManyToManyField(Tag, related_name="promises")
    created_at = models.DateTimeField(auto_now_add=True)

    objects = PromiseQuerySet.as_manager()

    class Meta:
        ordering = ["book", "chapter", "verse_start"]

    def __str__(self):
        return self.verse_ref

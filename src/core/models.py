from django.db import models
from django.utils.translation import gettext_lazy as _

class WarriorPost(models.Model):
    """
    The data model for a Warrior class news post.

    Fields:
    -------
        - original_source: CharField
            The source of the post. Sources cane be on of:
            '/r/wow/', '/r/classicwow/', 'Icy Veins', 'MMO Champion'.
        - source_link: TextField
            The link to the original source of the post.
        - created: DateTimeField
            The timestamp of when the post was scraped.
        updated: DateTimeField
            The timestamp of when the post was last updated.
    """

    class SourceType(models.TextChoices):
       REDDIT_WOW = 'rwow', _('/r/wow/')
       REDDIT_CLASSIC_WOW = 'rclass', _('/r/classicwow/')
       ICY_VEINS = 'icy', _('Icy Veins')
       MMO_CHAMPION = 'mmo', _('MMO Champion')
 
    original_source = models.CharField(
        max_length=20,
        choices=SourceType.choices,
    )
    source_link = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.source_link[0:60]



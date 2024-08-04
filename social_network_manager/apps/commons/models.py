from django.db import models
from django.utils import timezone

from apps.commons import constants as commons_constants


class DatesModel(models.Model):
    """
    Abstract model for dates
    """
    created_at = models.DateTimeField(commons_constants.HELP_TEXT['CREATED_AT'], default=timezone.now)
    updated_at = models.DateTimeField(commons_constants.HELP_TEXT['UPDATED_AT'], auto_now=True)

    class Meta(object):
        abstract = True

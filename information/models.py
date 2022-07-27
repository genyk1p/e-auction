from django.db import models
from tinymce.models import HTMLField


class Information(models.Model):
    NOTIFICATION_CLASS = [
        ('notification is-primary', 'notification is-primary'),
        ('notification is-link', 'notification is-link'),
        ('notification is-info', 'notification is-info'),
        ('notification is-success', 'notification is-success'),
        ('notification is-warning', 'notification is-warning'),
        ('notification is-danger', 'notification is-danger'),
        ('notification is-primary is-light', 'notification is-primary is-light'),
        ('notification is-link is-light', 'notification is-link is-light'),
        ('notification is-info is-light', 'notification is-info is-light'),
        ('notification is-success is-light', 'notification is-success is-light'),
        ('notification is-warning is-light', 'notification is-warning is-light'),
        ('notification is-danger is-light', 'notification is-danger is-light')
    ]

    slug = models.SlugField()
    title = models.CharField(max_length=100)
    content = HTMLField()
    meta_tag_description = models.TextField()
    notification_class = models.CharField(max_length=40, choices=NOTIFICATION_CLASS, default='notification is-primary')

    def __str__(self):
        return self.title
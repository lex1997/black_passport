from django.db import models

STATUS_CHOICES = (
    ('new', 'New'),
    ('active', 'Active'),
    ('off', 'Off'),
)


class Terrorist(models.Model):
    name = models.CharField(max_length=255)
    birthday = models.DateField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='new')
    tms_create = models.DateTimeField(auto_now_add=True)
    tms_archive = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'birthday'], name='terrorist_name_birthday')
        ]


class Passport(models.Model):
    series = models.CharField(max_length=4)
    number = models.CharField(max_length=6)
    tms_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.series

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['series', 'number'], name='passport_series_number')
        ]

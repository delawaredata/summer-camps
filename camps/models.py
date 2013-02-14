from django.db import models
from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import PhoneNumberField

STATE_CHOICES = (
    ('DE', 'Delaware'),
    ('PA', 'Pennsylvania'),
    ('NJ', 'New Jersey'),
    ('MD', 'Maryland'),
)
COUNTY_CHOICES = (
    ('NNC', 'Northern New Castle'),
    ('SNC', 'Southern New Castle'),
    ('KC', 'Kent County'),
    ('SC', 'Sussex County'),
    ('OOS', 'Out of State')
)
CATEGORY_CHOICES = (
    ('a', 'Arts'),
    ('d', 'Day'),
    ('e', 'Education'),
    ('h', 'Half-Day'),
    ('r', 'Residential'),
    ('s', 'Sports'),
    ('b', 'Spring Break')
)


class Organization(models.Model):
    """
    Model to hold information about each organization,
    including login information to maintain camps.
    """
    user = models.OneToOneField(User)
    organization = models.CharField('Organization', max_length=255)
    phone = PhoneNumberField()
    website = models.URLField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2, choices=STATE_CHOICES, default="DE")
    zip_code = models.CharField("Zip Code", max_length=10)

    class Meta:
        ordering = ['organization']

    def __unicode__(self):
        return "%s" % self.organization

    def get_contact_name(self):
        return "%s" % self.user.get_full_name()

    def get_absolute_url(self):
        return "/camps/%s" % self.id

    def _get_full_address(self):
        return u'%s, %s, %s %s' % (self.address, self.city, self.state, self.zip_code)
    full_address = property(_get_full_address)


class Camp(models.Model):
    """
    Camp model holds all the fun info for the summer camps.
    """
    organization = models.ForeignKey('Organization')
    camp_name = models.CharField('Camp', max_length=255)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=1)
    new = models.BooleanField('New camp')
    venue = models.CharField("Camp Venue", max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2, choices=STATE_CHOICES, default="DE")
    zip_code = models.CharField("Zip Code", max_length=10)
    county = models.CharField(choices=COUNTY_CHOICES, max_length=3)
    website = models.URLField(max_length=255, null=True, blank=True)
    phone = PhoneNumberField(blank=True, null=True)
    vacancies = models.IntegerField('No. of campers', max_length=5, blank=True, null=True)
    min_age = models.IntegerField('Minimum age', max_length=2, blank=True, null=True)
    max_age = models.IntegerField('Maximum age', max_length=2, blank=True, null=True)
    info = models.TextField('Camp info.')
    cost = models.CharField(max_length=140)
    start_date = models.DateField('Start date')
    end_date = models.DateField('End date')
    times = models.CharField(max_length=140, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["start_date"]

    def __unicode__(self):
        return "%s" % self.camp_name

    def _get_full_address(self):
            return u'%s, %s, %s %s' % (self.address, self.city, self.state, self.zip_code)
    full_address = property(_get_full_address)

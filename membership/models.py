from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import SET_DEFAULT


MEMBERSHIP_CHOICES = (
    ('Enterprise', 'Enterprise'),
    ('Professional', 'Professional'),
    ('Free', 'Free')
)


class Membership(models.Model):
    slug = models.SlugField()
    membership_type = models.CharField(choices=MEMBERSHIP_CHOICES,
                                       default='Free',
                                       max_length=30)
    price = models.IntegerField(default=15)
    # strip_plane_id = models.CharField(max_length=40)

    def __str__(self):
        return self.membership_type


class UserMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_subscribed = models.BooleanField(default=False)
    membership = models.ForeignKey(
        Membership, on_delete=SET_DEFAULT, default="Free")
    expiry_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user.username + ' ' + self.membership.membership_type


class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_membership = models.ForeignKey(Membership, on_delete=models.CASCADE)
    price = models.IntegerField()
    txn_id = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username + ' ' + str(self.price)

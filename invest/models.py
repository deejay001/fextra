from django.db import models
import secrets
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from decimal import Decimal
from django.dispatch import receiver

# Create your models here.

STATUS = (
    (0, "valid"),
    (1, "active"),
    (2, "expired"),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    ref_num = models.IntegerField(null=True, default=0)
    ref_code = models.CharField(max_length=8, null=True)

    def __str__(self):
        return self.user.username

    @classmethod
    def gen_refcode(cls, sender, instance, created, *args, **kwargs):

        if created:
            id_string = str(instance.id)
            upper_alpha = "ABCDEFGHJKLMNPQRSTVWXYZ"
            random_string = "".join(secrets.choice(upper_alpha) for i in range(8))
            instance.ref_code = (random_string + id_string)[-8:]
            instance.save()


post_save.connect(Profile.gen_refcode, sender=Profile)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):

    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Plan(models.Model):
    title = models.CharField(max_length=20)
    time = models.DurationField()

    def __str__(self):
        return self.title


class Coupon(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name='coupon')
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='coupon')
    stake = models.DecimalField(max_digits=10, decimal_places=2)
    output = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    code = models.CharField(max_length=8, blank=True, null=True, unique=True)
    status = models.IntegerField(choices=STATUS, default=STATUS)
    created_on = models.DateTimeField(auto_now_add=True)
    expire_on = models.DateTimeField(null=True, blank=True)

    @classmethod
    def gen_code(cls, sender, instance, created, *args, **kwargs):

        if created:
            id_string = str(instance.id)

            upper_alpha = "ABCDEFGHJKLMNPQRSTVWXYZ"
            random_str = "".join(secrets.choice(upper_alpha) for i in range(8))
            instance.code = (random_str + id_string)[-8:]
            instance.save()

    def get_stake(self):
        return int(self.stake)

    def put_return(self):
        stake = self.get_stake()
        plan = self.plan.title

        if plan == "Daily":
            out = (0.1 * stake) + stake
        elif plan == "Weekly":
            out = (0.25 * stake) + stake
        else:
            out = (0.4 * stake) + stake

        self.output = Decimal(out)

    def save(self, *args, **kwargs):
        self.put_return()

        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.code


post_save.connect(Coupon.gen_code, sender=Coupon)

STATUS1 = (
    (0, "Pending"),
    (1, "Paid"),
)


class Wtype(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Withdrawal(models.Model):
    w_type = models.ForeignKey(Wtype, on_delete=models.CASCADE, related_name='withdrawal', null=True)
    name = models.CharField(max_length=30)
    ac_name = models.CharField(max_length=100)
    ac_num = models.CharField(max_length=10)
    cash = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    bank = models.CharField(max_length=20)
    review = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS1, default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_on']

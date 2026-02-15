from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone

def avatar_upload_path(instance, filename): return f"accounts/{instance.pk}/avatar/{filename}"

class Accounts(AbstractUser): # Custom accounts
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='accounts_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='accounts_set',
        blank=True
    )
    
    display_name     = models.CharField    (max_length=20 , blank=True, null=True)
    bio              = models.TextField    (max_length=500, blank=True, null=True)
    status           = models.CharField    (max_length=50 , blank=True, null=True)
    timestamp_status = models.DateTimeField(                blank=True, null=True)

    num_phone  = models.CharField(max_length=20, blank=True, null=True)
    avatar     = models.ImageField(
        upload_to=avatar_upload_path,
        blank=True, null=True )

    date_birth = models.DateField(blank=True, null=True)
    gender     = models.BooleanField(default=False) # Male | Female

    following  = models.ManyToManyField('self', related_name="connection", symmetrical=False, blank=True)
    timeout = models.DateTimeField(blank=True, null=True)

    # devices = models.ManyToManyField('Devices', related_name='accounts', blank=True) # type: ignore

    def __str__(self) -> str:
        return self.username
    
    def is_timeout(self):
        if self.timeout:
            if timezone.now() > self.timeout:
                self.timeout = None
                self.save()
            else:
                return timezone.now() < self.timeout
        return False

    def is_active(self):
        return super().is_active
    
    def followers(self):
        return self.connection.all() # type: ignore
    
    def friends(self):
        return self.following.filter(pk__in=self.connection.values_list('pk', flat=True)) # type: ignore

    

    def get_age(self):
        if self.date_birth:
            today = timezone.now().date()
            return today.year - self.date_birth.year - ((today.month, today.day) < (self.date_birth.month, self.date_birth.day))
        return None
    def is_happy_birthday(self):
        if self.date_birth:
            today = timezone.now().date()
            return (today.month, today.day) == (self.date_birth.month, self.date_birth.day)
        return False

class Devices(models.Model):
    user = models.ForeignKey(Accounts, related_name='devices', on_delete=models.CASCADE)
    device_name = models.CharField(max_length=100)
    last_used = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.device_name} ({self.user.username})"
    def access_denied(self):
        self.user.timeout = timezone.now() + timezone.timedelta(minutes=15) # 15 minutes timeout
        self.user.save()
    def access_granted(self): # Remove timeout when access is granted. # When account's owner login with new device, access is denied until account's owner access_granted.
        self.user.timeout = None
        self.user.save()
    # if account used Devices when Login is hacked/new devices.

class MessageTo(models.Model):
    sender    = models.ForeignKey(Accounts, related_name='sent_messages'    , on_delete=models.CASCADE) # From
    receiver  = models.ForeignKey(Accounts, related_name='received_messages', on_delete=models.CASCADE) # To
    content   = models.TextField ( )
    timestamp = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.sender == self.receiver:
            raise ValidationError("You cannot send message to yourself.")
        if self.sender.is_timeout():
            raise ValidationError("You are in timeout. You cannot send message.")
        if self.receiver.is_timeout():
            raise ValidationError("The receiver is in timeout. You cannot send message to the receiver.")

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username} at {self.timestamp}"

class Report(models.Model):
    class ReasonChoices(models.TextChoices):
        SPAM                  = 'SP', 'Spam'
        FRAUD                 = 'FR', 'Fraud'
        DATING                = 'DA', 'Dating'
        SUSPRISIOUS_ACCOUNT   = 'SA', 'Suspicious Account'
        HACKING               = 'HK', 'Hacking'
        BULLYINH              = 'BU', 'Bullying'   
        INAPPROPRIATE_CONTENT = 'IC', 'Inappropriate Content'
        HARASSMENT            = 'HA', 'Harassment'
        OTHER                 = 'OT', 'Other'
    reporter = models.ForeignKey(Accounts, related_name='reports_made', on_delete=models.CASCADE) # Who report
    reported = models.ForeignKey(Accounts, related_name='reports_received', on_delete=models.CASCADE) # Who is reported
    reason   = models.TextField(choices=ReasonChoices.choices)
    timestamp = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.reporter == self.reported:
            raise ValidationError("You cannot report yourself.")
        if Report.objects.filter(reporter=self.reporter, reported=self.reported).exists():
            raise ValidationError("You have already reported this account.")
    
    def accept_report(self, days=7): # Who's Moderator accept report, account is reported will be timeout for 7 days. # When Moderator use Custom timeout, use days parameter to set timeout. # When Moderator use Custom timeout, use days parameter to set timeout.
        self.reported.timeout = timezone.now() + timezone.timedelta(days=days) # 7 days timeout
        self.reported.save()
        self.delete() # Delete report after accept report.

    

    def __str__(self):
        return f"Report from {self.reporter.username} against {self.reported.username} at {self.timestamp}"

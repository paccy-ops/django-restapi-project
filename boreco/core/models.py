from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.db import models
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from boreco.azure_storage import PrivateAzureStorage


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a new user"""
        if not email:
            raise ValueError("User must have an email")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """create and save new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user models that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ('id',)
        db_table = "users"

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }


class Client(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True)
    cvr = models.CharField(unique=True, db_index=True, max_length=255)
    client_name = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ('created_at',)
        db_table = 'clients'

    def __str__(self):
        return self.client_name


class ClientAssignment(models.Model):
    cvr = models.CharField(unique=True, db_index=True, max_length=255)
    client = models.ForeignKey('Client', null=True, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=255, null=True, blank=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assignment = models.CharField(max_length=255)
    created_at = models.DateField(auto_created=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ('created_at',)
        db_table = 'clientassignment'


class Dividends(models.Model):
    """dividend"""
    cvr = models.CharField(db_index=True, max_length=255)
    client = models.ForeignKey('Client', null=True, on_delete=models.SET_NULL)
    client_name = models.CharField(max_length=255, null=True, blank=True)
    client_responsible = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    client_responsible_name = models.CharField(max_length=255, null=True, blank=True)
    accounting_period_start = models.CharField(null=True, blank=True, max_length=255)
    accounting_period_end = models.CharField(null=True, blank=True, max_length=255)
    decision_date = models.DateField(null=True, blank=True)
    skat_recipient_vat = models.FloatField(null=True, blank=True)
    skat_recepient_tax = models.FloatField(null=True, blank=True)
    skat_total_dividend = models.FloatField(null=True, blank=True)
    skat_total_tax = models.FloatField(null=True, blank=True)
    caseware_total_dividend = models.IntegerField(default=0)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)
        db_table = 'dividends'

    def __str__(self):
        return self.client.client_name


class AccountStatus(models.Model):
    cvr = models.CharField(db_index=True, max_length=255)
    client = models.ForeignKey('Client', null=True, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=255, null=True, blank=True)
    period_date = models.DateField(null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    balance = models.FloatField(null=True, blank=True)
    order = models.IntegerField(default=0)
    status = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ('created_at',)
        db_table = 'accountStatus'

    def __str__(self):
        return self.client.client_name


class AccountStatusDeficit(models.Model):
    cvr = models.CharField(db_index=True, max_length=255)
    client = models.ForeignKey('Client', null=True, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=255, null=True, blank=True)
    date = models.CharField(max_length=255, null=True, blank=True)
    entry = models.CharField(max_length=255, null=True, blank=True)
    period = models.CharField(max_length=255, null=True, blank=True)
    balance = models.CharField(max_length=255, null=True, blank=True)
    order = models.IntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ('created_at',)
        db_table = 'accountStatusDeficit'

    def __str__(self):
        return self.client.client_name


class AccountStatusDeficitTotal(models.Model):
    cvr = models.CharField(db_index=True, max_length=255)
    total = models.CharField(db_index=True, max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ('created_at',)
        db_table = 'accountStatusDeficitTotal'

    def __str__(self):
        return self.client.client_name


class VatCurrent(models.Model):
    cvr = models.CharField(db_index=True, max_length=255)
    client = models.ForeignKey('Client', on_delete=models.CASCADE, null=True, blank=True)
    client_name = models.CharField(max_length=255, null=True, blank=True)
    period_start = models.DateField(null=True, blank=True)
    period_end = models.DateField(null=True, blank=True)
    filing_deadline = models.DateField(null=True, blank=True)
    client_responsible = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    client_responsible_name = models.CharField(max_length=255, null=True, blank=True)
    report_contact_name = models.CharField(max_length=255, null=True, blank=True)
    report_contact_phone = models.CharField(max_length=255, null=True, blank=True)
    report_contact_email = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)
        db_table = 'vatcurrent'

    def __str__(self):
        return self.client.client_name


class AccountStatement(models.Model):
    cvr = models.CharField(unique=True, db_index=True, max_length=255)
    client = models.ForeignKey('Client', null=True, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=255)
    entry_date = models.DateField(auto_now=True)
    entry_name = models.CharField(max_length=255)
    further_initiatives = models.CharField(max_length=255)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    balance = models.DecimalField(decimal_places=2, max_digits=10)

    class Meta:
        ordering = ('entry_date',)
        db_table = 'accountstatement'

    def __str__(self):
        return self.client.client_name


class VatPastRecord(models.Model):
    cvr = models.CharField(db_index=True, max_length=255, null=False)
    client = models.ForeignKey('Client', null=True, blank=True, on_delete=models.SET_NULL)
    client_name = models.CharField(max_length=255, null=True, blank=True)
    period_start = models.DateField(null=True, blank=True)
    period_end = models.DateField(null=True, blank=True)
    receipt_number = models.IntegerField(default=0, null=True, blank=True)
    receipt = models.FileField(storage=PrivateAzureStorage(), blank=True, null=True)
    filing_date = models.DateField(null=True, blank=True)
    filing_deadline = models.DateField(null=True, blank=True)
    person_cvr = models.CharField(max_length=255, null=True, blank=True)
    person_filing_vat = models.CharField(max_length=255, null=True, blank=True)
    client_address = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    output_vat = models.CharField(max_length=255, null=True, blank=True)
    vat_goods_abroad = models.CharField(max_length=255, null=True, blank=True)
    vat_services_abroad = models.CharField(max_length=255, null=True, blank=True)
    input_vat = models.CharField(max_length=255, null=True, blank=True)
    oil_bottled_gas_vat = models.CharField(max_length=255, null=True, blank=True)
    electricity_vat = models.CharField(max_length=255, null=True, blank=True)
    natural_vat = models.CharField(max_length=255, null=True, blank=True)
    coal_vat = models.CharField(max_length=255, null=True, blank=True)
    co2_vat = models.CharField(max_length=255, null=True, blank=True)
    water_vat = models.CharField(max_length=255, null=True, blank=True)
    total_vat = models.CharField(max_length=255, null=True, blank=True)
    scrape_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    order = models.IntegerField(default=0, null=True, blank=True)
    client_responsible = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    client_responsible_name = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    indicating_type = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ('created_at',)
        db_table = 'vatpastrecord'

    def __str__(self):
        return self.client_name


class TaxReturn(models.Model):
    cvr = models.CharField(unique=True, db_index=True, max_length=255)
    client = models.ForeignKey('Client', null=True, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=255)
    skatAmount = models.IntegerField()
    casewareAmount = models.IntegerField()
    identifier = models.CharField(max_length=100)
    filingStatus = models.CharField(max_length=100)

    class Meta:
        db_table = 'taxreturn'

    def __str__(self):
        return self.client.client_name


class Tinglysning(models.Model):
    @staticmethod
    def get_absolute_url():
        return reverse('tinglysning:upload')

    cvr = models.CharField(db_index=True, max_length=255)
    client = models.ForeignKey('Client', null=True, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=255, null=True, blank=True)
    client_responsible = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    client_responsible_name = models.CharField(max_length=255, null=True, blank=True)
    tinglysning = models.CharField(max_length=255, null=True, blank=True)
    document_type = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=255, null=True, blank=True)
    concern = models.CharField(max_length=255, null=True, blank=True)
    date_serial = models.CharField(max_length=255, null=True, blank=True)
    file_uploaded = models.FileField(storage=PrivateAzureStorage(), blank=True, null=True)

    class Meta:
        db_table = 'tinglysning'
        ordering = ('-cvr',)

    def __str__(self):
        return self.client.client_name


class Skattekonto(models.Model):
    cvr = models.CharField(unique=True, db_index=True, max_length=255)
    client = models.ForeignKey('Client', null=True, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=255, null=True, blank=True)
    client_responsible = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    client_responsible_name = models.CharField(max_length=255, null=True, blank=True)
    endingBalance = models.IntegerField()
    statementAccount = models.CharField(max_length=255)

    class Meta:
        db_table = 'skattekonto'

    def __str__(self):
        return self.client.client_name


class EIndkomst(models.Model):
    cvr = models.CharField(db_index=True, max_length=255)
    client = models.ForeignKey('Client', null=True, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=255, null=True, blank=True)
    client_responsible = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    client_responsible_name = models.CharField(max_length=255, null=True, blank=True)
    year = models.CharField(max_length=255, null=True)
    month = models.CharField(max_length=255, null=True)
    quarter = models.IntegerField(default=0)
    data = models.JSONField()
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = 'eindkomst'
        ordering = ('-created_at',)

    def __str__(self):
        return self.client.client_name


class VatAccountInfo(models.Model):
    cvr = models.CharField(max_length=255, db_index=True)
    client = models.ForeignKey('Client', models.CASCADE, null=True, blank=True)
    client_name = models.CharField(max_length=255, null=True, blank=True)
    payment_id = models.CharField(max_length=255)
    refund_limit = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ('-created_at',)
        db_table = "vataccountinfo"

    def __str__(self):
        return self.client.client_name


class Virkinfo(models.Model):
    cvr = models.CharField(max_length=255, db_index=True)
    client = models.ForeignKey('Client', models.CASCADE, null=True, blank=True)
    client_name = models.CharField(max_length=255, null=True, blank=True)
    managers = models.CharField(max_length=255, null=True, blank=True)
    address1 = models.CharField(max_length=255, null=True, blank=True)
    address2 = models.CharField(max_length=255, null=True, blank=True)
    postcode = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    financial_year = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ('created_at',)
        db_table = "virkinfo"

    def __str__(self):
        return self.client.client_name

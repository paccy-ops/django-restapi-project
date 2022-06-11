from core.models import User
from django.contrib import admin
from core import models
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class EIndkomstResource(resources.ModelResource):
    class Meta:
        model = models.EIndkomst

class TinglysningResource(resources.ModelResource):
    class Meta:
        model = models.Tinglysning


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_verified', 'is_active', 'is_staff', 'is_superuser']
    search_fields = ['email']
    list_per_page = 10


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['cvr', 'client_name', 'created_at', 'updated_at']
    search_fields = ['cvr', 'client_name']
    ordering = ['cvr']
    list_filter = ['cvr', 'client_name']
    list_per_page = 10


@admin.register(models.VatPastRecord)
class VatPastRecordAdmin(admin.ModelAdmin):
    list_display = ['cvr', 'client', 'filing_date', 'filing_deadline', 'period_start', 'period_end', 'receipt_number']
    search_fields = ['cvr', 'client_name']
    ordering = ['cvr', 'client']

    list_filter = ['cvr', 'client']
    list_per_page = 10


@admin.register(models.VatCurrent)
class VatcurrentRecordAdmin(admin.ModelAdmin):
    list_display = ['cvr', 'client', 'period_start', 'period_end', 'filing_deadline']
    search_fields = ['cvr', 'client__client_name']
    ordering = ['cvr', 'client']
    list_filter = ['cvr', 'client']
    list_per_page = 10


@admin.register(models.Dividends)
class DividendsAdmin(admin.ModelAdmin):
    list_display = ['cvr', 'client', 'skat_recipient_vat', 'skat_recepient_tax', 'decision_date']
    search_fields = ['cvr', 'client__client_name']
    ordering = ['cvr', 'client']
    list_filter = ['cvr', 'client']
    list_per_page = 10


@admin.register(models.AccountStatus)
class AccountStatusAdmin(admin.ModelAdmin):
    list_display = ['cvr', 'client', 'status', 'amount', 'balance', 'period_date', 'order']
    search_fields = ['client__client_name', 'status']
    list_per_page = 10

@admin.register(models.Tinglysning)
class TinglysningAdmin(ImportExportModelAdmin):
    resource_class = TinglysningResource
    def image_tag(self, obj):
        return format_html('<img src="{}" width="{}" height={} />'.format(obj.file_uploaded.url, 60, 60))

    image_tag.short_description = 'Image'
    list_display = ['cvr', 'client', 'tinglysning', 'role', 'concern', 'image_tag']
    search_fields = ['client']
    list_per_page = 10


@admin.register(models.EIndkomst)
class EIndkomstAdmin(ImportExportModelAdmin):
    resource_class = EIndkomstResource
    list_display = ['cvr', 'client', 'year', 'month', 'quarter']
    search_fields = ['cvr']
    list_per_page = 10


admin.site.register(models.ClientAssignment)
admin.site.register(models.VatAccountInfo)

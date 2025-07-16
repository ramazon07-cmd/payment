from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('click_trans_id', 'merchant_trans_id', 'error', 'error_note')

from django.db import models

class Payment(models.Model):
    click_trans_id = models.CharField(max_length=100)
    merchant_trans_id = models.CharField(max_length=100)
    merchant_confirm_id = models.CharField(max_length=100)
    sign_string = models.CharField(max_length=255)
    error = models.IntegerField()
    error_note = models.TextField()

    def __str__(self):
        return f"{self.merchant_trans_id} - {self.click_trans_id}"

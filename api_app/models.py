from django.db import models

class Transaction(models.Model):
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.CharField(max_length=255)
    external_reference = models.CharField(max_length=64)
    request_id = models.CharField(max_length=64, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.request_id

class ApiResponse(models.Model):
    request_id = models.CharField(max_length=64)
    response_id = models.CharField(max_length=64)
    status = models.CharField(max_length=20)
    external_reference = models.CharField(max_length=64)

    def __str__(self):
        return self.request_id

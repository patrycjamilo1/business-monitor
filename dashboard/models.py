from django.db import models

class SalesData(models.Model):
    date = models.DateField()
    product = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    def total_sales(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.date} - {self.product}: {self.quantity} szt. x {self.price} zł"

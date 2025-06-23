from django.db import models

# Create your models here.

class DailySaleSummary(models.Model):
    summary_date = models.DateField(unique=True)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2)
    products_sold_count = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Summary for {self.summary_date}"

    class Meta:
        verbose_name_plural = "Daily sale summaries"
        ordering = ["-summary_date"]

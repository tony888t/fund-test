from django.db import models
from django.utils.translation import gettext_lazy as _


class Fund(models.Model):
    class Strategy(models.TextChoices):
        LONG_SHORT_EQUITY = "LSE", _("Long/Short Equity")
        GLOBAL_MACRO = "GLM", _("Global Micro")
        ARBITRAGE = "ARB", _("Arbitrage")

    name = models.CharField(max_length=100)
    strategy = models.CharField(max_length=3, choices=Strategy)
    aum = models.PositiveIntegerField()
    inception_date = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.strategy}"

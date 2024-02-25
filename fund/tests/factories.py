from random import randrange

import arrow
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice

from fund.models import Fund


class FundFactory(DjangoModelFactory):
    class Meta:
        model = Fund

    name = "Awesome stock"
    strategy = FuzzyChoice(Fund.Strategy)
    aum = randrange(350000)
    inception_date = arrow.utcnow().date()

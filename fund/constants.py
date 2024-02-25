from fund.models import Fund

STRATEGY_MAP = {x.label.lower(): x.value for x in Fund.Strategy}

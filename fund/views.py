import csv
import logging
from collections import namedtuple

from django.db import transaction
from django.db.models import Sum
from django.db.utils import DatabaseError
from django.shortcuts import render, redirect

from .forms import FundUploadForm
from .models import Fund
from .constants import STRATEGY_MAP


logger = logging.getLogger(__name__)


@transaction.atomic
def process_csv_handler(data_row: list[namedtuple], filename: str) -> None:
    for row in data_row:
        # Only process row if all data is available - name, strategy, aum and inception_date
        if not all(row):
            logger.error(f"Missing data in csv - {filename}")
            continue

        try:
            Fund.objects.get_or_create(
                name=row.name,
                strategy=STRATEGY_MAP[row.strategy.lower()],
                aum=row.aum,
                inception_date=row.inception_date,
            )
        except DatabaseError as e:
            logger.error(f"DB Error 0 {e}. File {filename}")


def fund_upload(request):
    if request.method == "POST":
        form = FundUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES["csv_file"]
            decoded_file = csv_file.read().decode("utf-8")
            reader = csv.reader(decoded_file.splitlines(), delimiter=",")
            next(reader)

            Columns = namedtuple(
                "Fund", ("name", "strategy", "aum", "inception_date")
            )
            rows = [Columns(*x) for x in reader]

            process_csv_handler(rows, csv_file.name)

            return redirect("fund_list")
    else:
        form = FundUploadForm()
    return render(request, "fund/upload.html", {"form": form})


def fund_list(request):
    strategy_filter = request.GET.get("strategy_filter", "")
    if strategy_filter:
        funds = Fund.objects.filter(strategy=strategy_filter)
    else:
        funds = Fund.objects.all()
    total_funds = funds.count()
    total_aum = funds.aggregate(Sum("aum"))["aum__sum"] or 0

    return render(
        request,
        template_name="fund/funds.html",
        context={
            "strategies": Fund.Strategy,
            "funds": funds,
            "total_funds": total_funds,
            "total_aum": total_aum,
        },
    )

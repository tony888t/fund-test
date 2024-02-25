from django.urls import path, include

from rest_framework.routers import DefaultRouter
from fund.api import api_views
from fund import views

router = DefaultRouter()
router.register(r"funds", api_views.FundViewSet, basename="fund")

urlpatterns = [
    path("", include(router.urls)),
    path("funds-upload/", views.fund_upload, name="fund_upload"),
    path("fund-list/", views.fund_list, name="fund_list"),
]

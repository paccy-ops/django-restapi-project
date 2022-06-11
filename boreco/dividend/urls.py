from dividend import views
from django.urls import path

app_name = "dividend"

urlpatterns = [
    path('', views.DividendViewList.as_view(), name="dividend-list"),
    path('<int:cvr>', views.DividendViewDetails.as_view(), name="dividends-detail"),
]

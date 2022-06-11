from django.urls import path

from eindkomst import views

app_name = "eindkomst"


urlpatterns = [
    path('', views.EIndkomstListCreateView.as_view(), name="eindkomst-list"),
    path('<int:id>', views.EIndkomstDetailView.as_view(), name="eindkomst-detail"),
    path('by_cvr', views.UniqueCvrAndClient.as_view(), name="by_unique_cvr"),
    path('order_by_year_month/<int:cvr_pk>', views.OrderByMonthAndCvrAndClient.as_view(), name="order_year"),

]

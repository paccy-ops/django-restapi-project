from django.urls import path

from taxreturn import views

app_name = "taxreturn"

urlpatterns = [
    path('', views.TaxReturnListCreateView.as_view(), name="tax-return"),
    path("<int:cvr>", views.TaxReturnDetailView.as_view(), name="tax-details")
]

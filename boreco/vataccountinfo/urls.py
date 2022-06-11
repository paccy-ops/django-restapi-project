from django.urls import path

from vataccountinfo import views

app_name = "vataccountinfo"

urlpatterns = [
    path('', views.VatAccountInfoViewList.as_view(), name="vat-account-info-list"),
    path('<int:id>', views.VatAccountInfoViewDetails.as_view(), name="vat-account-info-detail"),
    path('send-email/<int:cvr_pk>', views.AccountInfoForEmail.as_view(), name="account-send-email"),
]

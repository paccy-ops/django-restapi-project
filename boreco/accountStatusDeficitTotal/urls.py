from accountStatusDeficitTotal import views
from django.urls import path

app_name = "accountStatusDeficitTotal"

urlpatterns = [
    path('', views.AccountDeficitTotalViewList.as_view(), name="account-list"),
    path('<int:cvr>', views.AccountStatusDeficitTotalViewDetails.as_view(), name="account-detail"),
    path('by_cvr/<int:cvr_pk>', views.AccountstatusDeficitTotalByCvr.as_view(), name="account_by_cvr_pk"),
    path('account-by-cvr', views.AccountStatusDeficitTotalList.as_view(), name="accounts-cvr-list"),
]
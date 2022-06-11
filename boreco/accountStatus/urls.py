from accountStatus import views
from django.urls import path

app_name = "accountStatus"

urlpatterns = [
    path('', views.AccountStatusViewList.as_view(), name="account-list"),
    path('<int:id>', views.AccountStatusViewDetails.as_view(), name="account-detail"),
    path('account-by-cvr', views.AccountStatusList.as_view(), name="accounts-cvr-list"),
]

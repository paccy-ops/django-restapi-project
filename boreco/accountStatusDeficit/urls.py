from accountStatusDeficit import views
from django.urls import path

app_name = "accountStatusDeficit"

urlpatterns = [
    path('', views.AccountStatusDeficitViewList.as_view(), name="account-list"),
    path('<int:id>', views.AccountStatusDeficitViewDetails.as_view(), name="account-detail"),
    path('account-by-cvr', views.AccountStatusDeficitList.as_view(), name="accounts-cvr-list"),
    path('client_unique_cvr', views.AccountstatusDeficitUniqueCvr.as_view(), name="client-name-list"),
    path('order_by/<int:cvr_pk>', views.OrderByOrderAccountstatusdeficit.as_view(), name="order_by-order-list"),
]

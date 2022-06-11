from accountStatement import views
from django.urls import path

app_name = "accountStatement"

urlpatterns = [
    path('', views.AccountStatementViewList.as_view(), name="accountStatement-list"),
    path('<int:cvr>', views.AccountStatementViewDetails.as_view(), name="accountStatement-detail"),
]

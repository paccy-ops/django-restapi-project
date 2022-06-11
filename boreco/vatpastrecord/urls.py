from django.urls import path

from vatpastrecord import views

app_name = "vatpastrecord"

urlpatterns = [
    path('', views.VatPastRecordViewList.as_view(), name="vatpastrecord-list"),
    path('<int:id>', views.VatPastRecordViewDetails.as_view(), name="vatpastrecord-detail"),
    path('by_cvr', views.UniqueCvrAndClient.as_view(), name="by_unique_cvr"),
]

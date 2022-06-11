from django.urls import path

from vatCurrent import views

app_name = "vatCurrent"

urlpatterns = [
    path('', views.VatCurrentViewList.as_view(), name="vatCurrent-list"),
    path('<int:cvr>', views.VatCurrentViewDetails.as_view(), name="vatCurrent-detail"),
]

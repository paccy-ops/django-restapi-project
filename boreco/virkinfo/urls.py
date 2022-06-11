from django.urls import path

from virkinfo import views

app_name = "virkinfo"

urlpatterns = [
    path('', views.VirkInfoViewList.as_view(), name="virkinfo-list"),
    path('<int:cvr>', views.VirkInfoViewDetails.as_view(), name="virkinfo-detail")
]

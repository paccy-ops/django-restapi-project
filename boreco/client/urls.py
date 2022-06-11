from client import views
from django.urls import path

app_name = "client"

urlpatterns = [
    path('', views.ClientList.as_view(), name="client-list"),
    path('<int:cvr>', views.ClientDetailView.as_view(), name="client_detail"),
    # path('client', views.AllClientData, name="all-client"),
    path('save', views.SaveData.as_view(), name="save-client"),

]

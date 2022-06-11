from django.urls import path
from Skattekonto import views

app_name = "Skattekonto"

urlpatterns = [
    path('', views.SkattekontoListCreateView.as_view(), name="Skattekonto-list"),
    path('<int:cvr>', views.SkattekontoDetailView.as_view(), name="Skattekonto-detail")
]

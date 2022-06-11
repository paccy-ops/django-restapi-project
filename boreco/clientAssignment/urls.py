from clientAssignment import views
from django.urls import path

app_name = "clientAssignment"

urlpatterns = [
    path('', views.ClientAssignmentListView.as_view(), name="client-assignment"),
    # path('create', views.ClientAssignmentCreate.as_view(), name="client-assignment-create"),
    path('<int:cvr>', views.ClientAssignmentDetailView.as_view(), name="client-assignment-detail"),
]

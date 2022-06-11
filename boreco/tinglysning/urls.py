from django.urls import path

from tinglysning import views

app_name = 'tinglysning'

urlpatterns = [
    path('', views.TinglysningListView.as_view(), name='tinglysning-list'),
    path('<int:cvr>', views.TinglysningDetailView.as_view(), name='tinglysning-detail'),
    path('download/<int:id>/', views.FileDownloadAPIView.as_view(), name="file-download")
]

from django.urls import path
from . import views


urlpatterns = [
    path('', views.StartingPageView.as_view(), name='starting_page'),
    path('posts', views.AllPostView.as_view(),name='posts_page'),
    path("posts/<slug:slug>", views.PostDetail.as_view(),name='post-detail-page'),
    path("read-later", views.LoadLaterView.as_view(),name='read-later'),
]

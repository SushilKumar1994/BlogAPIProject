from django.urls import path, include, re_path
from blogapp import views

#

urlpatterns = [
    path('create_user/', views.UserCreate.as_view(), name='account-create'),

    path('login/',views.MyTokenObtainPairView.as_view()),

    path('get_userprofile/',views.GetUserProfileData.as_view()),   
    
    re_path('update_userprofile/(?P<id>\d+)/', views.UpdateUserAPIView.as_view()),

    path('post_create/',views.PostCreateAPIView.as_view(),name="create"),
    
    path('post_list/',views.PostListAPIView.as_view(),name="list"),

    path('post_detail/<int:id>/',views.PostDetailAPIView.as_view(),name="detail"),

    re_path('post_edit/(?P<id>\d+)/',views.PostUpdateAPIView.as_view(),name="Edit"),
   
    re_path('post_delete/(?P<id>\d+)/',views.PostDeleteAPIView.as_view(),name="delete"),

    path('comment_create/',views.CommentCreateAPIView.as_view(),name="comment_create"),

    path('comment_list/',views.CommentListAPIView.as_view(),name="comment_list"),

    re_path('comment_edit/(?P<id>\d+)/',views.CommentUpdateAPIView.as_view(),name="comment_edit"),

    re_path('comment_delete/(?P<id>\d+)/',views.CommentDeleteAPIView.as_view(),name="comment_delete"),

]


from django.urls import path

from .views import (AdminCategoryList, AdminDraftList, AdminPostCategory,
                    AdminPostDetail, AdminPostList, CreatePost, DeletePost,
                    EditPost, GetLikeUser, PostbyCategory, PostComments,
                    PostCommentUser, PostDetail, PostLikeUser, PostList,
                    PostListDetailFillter, PostViews, TopPostList)

app_name = 'blog_api'

urlpatterns = [
    path('', PostList.as_view(), name='listcreate'),
    path('posts/top/', TopPostList.as_view(), name='toppost'),
    path('post/view/', PostViews.as_view(), name='postview'),
    path('post/like/<str:pk>/', PostLikeUser.as_view(), name='postlike'),
    path('post/getlike/<str:pk>/', GetLikeUser.as_view(), name='getlike'),
    path('post/comment/', PostCommentUser.as_view(), name='postcommentuser'),
    path('post/category/', AdminPostCategory.as_view(), name='adminpostcategory'),
    path('category/<str:pk>/', PostbyCategory.as_view(), name='postbycateg'),
    path('search/', PostListDetailFillter.as_view(), name='postsearch'),
    path('post/<str:pk>/', PostDetail.as_view(), name='detailcreate'),
    path('post/<str:pk>/comment/', PostComments.as_view(), name='postcomment'),

    # ADMIN
    path('admin/list/', AdminPostList.as_view(), name='adminpostlist'),
    path('admin/draft/', AdminDraftList.as_view(), name='admindraftlist'),
    path('admin/category/', AdminCategoryList.as_view(), name='admincategorylist'),
    path('admin/create/', CreatePost.as_view(), name='createpost'),
    path('admin/edit/postdetail/<int:pk>/', AdminPostDetail.as_view(), name='admindetailpost'),
    path('admin/edit/<int:pk>/', EditPost.as_view(), name='editpost'),
    path('admin/delete/<int:pk>/', DeletePost.as_view(), name='deletepost'),
]

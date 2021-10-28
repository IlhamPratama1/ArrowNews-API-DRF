from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from rest_framework.documentation import include_docs_urls
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import MyTokenObtainPairView

urlpatterns = [
    # API Token
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Project URL
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')),

    # Blog API Application
    path('api/', include('blog_api.urls', namespace='blog_api')),

    # User Management
    path('api/user/', include('users.urls', namespace='users')),

    # API Schema Documentation
    path('docs/', include_docs_urls(title='BlogApi')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

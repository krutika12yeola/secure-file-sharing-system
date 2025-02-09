# from django.urls import path
# from .views import upload_file
# from .views import generate_presigned_url
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# urlpatterns = [
#     path('upload/', upload_file, name='upload_file'),
#     path('download/', generate_presigned_url, name='generate_presigned_url'),
#     path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
# ]



from django.urls import path # type: ignore
from .views import upload_file, generate_presigned_url
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView # type: ignore

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('download/', generate_presigned_url, name='generate_presigned_url'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

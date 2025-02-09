# from django.shortcuts import render

# # Create your views here.

# import boto3
# from django.conf import settings
# from rest_framework.response import Response
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from .models import FileUpload

# s3_client = boto3.client(
#     's3',
#     aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#     aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
#     region_name=settings.AWS_REGION
# )

# BUCKET_NAME = settings.AWS_STORAGE_BUCKET_NAME

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def upload_file(request):
#     file = request.FILES['file']
#     s3_client.upload_fileobj(file, BUCKET_NAME, file.name)

#     file_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{file.name}"

#     FileUpload.objects.create(user=request.user, file_name=file.name, file_url=file_url)

#     return Response({"message": "File uploaded successfully!", "file_url": file_url})
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def generate_presigned_url(request):
#     file_name = request.GET.get('file_name')

#     url = s3_client.generate_presigned_url(
#         'get_object',
#         Params={'Bucket': BUCKET_NAME, 'Key': file_name},
#         ExpiresIn=3600  # 1-hour expiration
#     )

#     return Response({"presigned_url": url})





from django.shortcuts import render # type: ignore
import boto3 # type: ignore
from django.conf import settings # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.decorators import api_view, permission_classes # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore
from .models import FileUpload

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION
)

BUCKET_NAME = settings.AWS_STORAGE_BUCKET_NAME

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_file(request):
    """
    Upload a file to AWS S3 and store its metadata in the database.
    """
    if 'file' not in request.FILES:
        return Response({"error": "No file provided"}, status=400)

    file = request.FILES['file']
    
    try:
        s3_client.upload_fileobj(file, BUCKET_NAME, file.name)
        file_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{file.name}"

        FileUpload.objects.create(user=request.user, file_name=file.name, file_url=file_url)

        return Response({"message": "File uploaded successfully!", "file_url": file_url}, status=201)

    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_presigned_url(request):
    """
    Generate a presigned URL for downloading a file from AWS S3.
    """
    file_name = request.GET.get('file_name')

    if not file_name:
        return Response({"error": "File name is required"}, status=400)

    try:
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': file_name},
            ExpiresIn=3600  # URL valid for 1 hour
        )

        return Response({"presigned_url": url}, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=500)

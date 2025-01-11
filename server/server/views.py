from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import auth, exceptions

def home(request):
    return HttpResponse("Hello, Django!")



class VerifyIdTokenView(APIView):
    def post(self, request):
        id_token = request.data.get("idToken")

        if not id_token:
            return Response({"error": "ID token is missing"}, status=status.HTTP_400_BAD_REQUEST)

        try:    
            # Verify the ID token using Firebase Admin SDK
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token["uid"]

            # Get user details from Firebase
            user = auth.get_user(uid)
            user_data = {
                "uid": user.uid,
                "email": user.email,
                "display_name": user.display_name,
                "photo_url": user.photo_url,
            }
            for value in user_data:
                print(value,end=":")

            return Response({"success": True, "user": user_data}, status=status.HTTP_200_OK)
        except exceptions.FirebaseError as e:
            return Response({"error": "Invalid ID token", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
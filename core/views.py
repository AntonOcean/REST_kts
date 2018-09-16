from django.contrib.auth import login, authenticate
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import viewsets, generics, permissions, status, renderers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from core.serializers import UserSerializer, TokenSerializer, TopicSerializer
from core.models import User, Topic, Comment

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class TopicList(generics.ListAPIView):
    queryset = Topic.objects.all().order_by('-created')
    serializer_class = TopicSerializer


class TopicCreate(generics.CreateAPIView):
    queryset = Topic.objects.all().order_by('-created')
    serializer_class = TopicSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(creator_id=self.request.user.id)


class LoginView(generics.CreateAPIView):
    """
    POST auth.login/
    """
    # This permission class will overide the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        if "username" not in request.data or "password" not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            login(request, user)
            serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

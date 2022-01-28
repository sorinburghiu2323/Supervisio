from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.users.models import User
from api.users.serializers import UserPostSerializer, UserSerializer
from api.users.utils import get_token_response


class UserViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=["POST"], url_path="login")
    def login(self, request):
        """
        Login function to authenticate users with email and password.
        """
        email = request.data.get("email")
        password = request.data.get("password")
        if not email or not password:
            return Response({"detail": "Bad fields."}, status=400)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "User does not exist."}, status=404)
        if not user.is_active:
            return Response({"detail": "User account has been deleted."}, status=404)
        if not user.check_password(password):
            return Response({"detail": "Incorrect password."}, status=401)
        return Response(get_token_response(user), status=200)

    @action(
        detail=False,
        methods=["POST"],
        url_path="logout",
        permission_classes=[IsAuthenticated],
    )
    def logout(self, request):
        """
        Logout a logged in user.
        """
        Token.objects.get(user=request.user).delete()
        return Response({"detail": "User logged out."}, status=200)

    @action(
        detail=False,
        methods=["GET", "PATCH"],
        url_path="me",
        authentication_classes=[IsAuthenticated],
    )
    def users_me(self, request):
        """
        Endpoint to manage the currently logged in user.
        """
        user = request.user
        if request.method == "GET":
            return Response(UserSerializer(user).data)
        if request.method == "PATCH":
            if not user.is_supervisor:
                return Response({"detail": "User is not supervisor."}, status=403)
            serializer = UserPostSerializer(user, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=400)
            serializer.save()
            return Response(status=200)

    @action(
        detail=False,
        methods=["GET"],
        url_path="supervisors",
        authentication_classes=[IsAuthenticated],
    )
    def users_supervisors(self, request):
        supervisors = User.objects.filter(is_supervisor=True)
        return Response(UserSerializer(supervisors, many=True).data)

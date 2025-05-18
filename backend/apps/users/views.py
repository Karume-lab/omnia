from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from djoser.serializers import SendEmailResetSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from djoser.email import ActivationEmail


User = get_user_model()


class CustomJWTTokenCreateView(TokenObtainPairView):
    """
    Custom JWT token creation view that extends the default
    SimpleJWT TokenObtainPairView to add behavior for unverified users.

    If a user attempts to log in but their account is not active (i.e., not verified),
    this view sends a verification email and returns a custom error message
    instead of issuing tokens.
    """

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for JWT token creation.

        Checks if the user with the provided email exists and is active.
        If the user is inactive, triggers sending an activation email
        and returns a 403 Forbidden response with an explanatory message.

        Otherwise, delegates to the parent class to process token creation normally.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: DRF Response containing JWT tokens or error message.
        """
        email = request.data.get("email")  # type: ignore
        user = User.objects.filter(email=email).first()

        if user and not user.is_active:
            # Send activation email
            self.send_activation_email(user, request)

            return Response(
                {
                    "detail": _(
                        "Your account is not verified. "
                        "A verification email has been sent to your inbox."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # Proceed with normal JWT token obtain process
        return super().post(request, *args, **kwargs)

    def send_activation_email(self, user, request=None):
        """
        Send the activation email to the specified user.
        Uses Djoser's ActionViewMixin directly.
        Args:
            user (User): The user instance to send the activation email to.
            request (HttpRequest, optional): The current request object.
        """

        # Create a simplified request if none provided
        if request is None:
            request = HttpRequest()
            request.META = {"HTTP_HOST": "localhost:8000"}

        # Prepare data for the serializer
        context = {"request": request}
        data = {"email": user.email}

        # Create and validate the serializer
        serializer = SendEmailResetSerializer(data=data, context=context)
        serializer.is_valid(raise_exception=True)

        context = {"user": user}
        to = [user.email]
        ActivationEmail(request, context).send(to)

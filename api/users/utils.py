from rest_framework.authtoken.models import Token


def get_token_response(user):
    """
    Method gets or creates a token for a user logging in, and returns the string
    for returning to the frontend.
    :param user: User instance.
    :return: dict - response token.
    """
    token, _ = Token.objects.get_or_create(user=user)
    response = {"token": "Token " + str(token)}
    return response

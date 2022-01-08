from rest_framework.exceptions import ValidationError


def convert_to_bool(value):
    """
    To use for query parameters data.
    :param value: param from query.
    :return: bool or ValidationError.
    """
    if value in ["True", "true", True, 1, "1"]:
        return True
    elif value in ["False", "false", False, 0, "0"]:
        return False
    raise ValidationError({"detail": "Filter value does not exist."})

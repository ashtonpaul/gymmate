from datetime import date

from rest_framework import serializers


class FutureDateValidator(object):
    """
    Validate that a date is not in the future
    """
    def __init__(self, message=None):
        if not message:
            self.message = 'Future dates are not allowed'
        else:
            self.message = message

    def __call__(self, value):
        if value > date.today():
            raise serializers.ValidationError(self.message)


class PasswordValidator(object):
    """
    Validate user passwords
    """
    def __init__(self, message=None):
        if not message:
            self.message = 'Password must be at least 6 characters'
        else:
            self.message = message

    def __call__(self, value):
        if len(value) < 6:
            raise serializers.ValidationError(self.message)

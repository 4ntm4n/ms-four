from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, response_id, timestamp):

        print("!!! response id: ", response_id.pk)
        return (
            six.text_type(response_id.pk) + six.text_type(timestamp) +
            six.text_type(response_id.completed)
        )

account_activation_token = AccountActivationTokenGenerator()
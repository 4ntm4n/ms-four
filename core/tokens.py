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


from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode


# "a01".join(urlsafe_base64_encode(force_bytes(num)))
# same as "a01".join(id) -> same as secret.join(id)

#urlsafe_base64_encode(force_bytes(a01".join(urlsafe_base64_encode(force_bytes(num)))))
# same as urlsafe_base64_encode(force_bytes(secret.join(id)))

class EncryptDecrypt():
    def encrypt_link(self, name, num):
        """ 
        1. join own secret with id encryption
        2. extend encryption by encrypt the newly made string
        results in single encrypted scattered secret, double encrypted id
        """

        id = urlsafe_base64_encode(force_bytes(num))
        secret = "a01"
        ext_encryption = urlsafe_base64_encode(force_bytes(secret.join(id)))
        return f"{ext_encryption}"
    

    def decrypt_link(self, link):
        
        decoded_link = force_str(urlsafe_base64_decode(link))
        secret = "a01"
        encrypted_id = decoded_link.replace(secret, "")
        id = force_str(urlsafe_base64_decode(encrypted_id))
        return id


link = EncryptDecrypt()



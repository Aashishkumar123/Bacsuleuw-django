from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.contrib.auth import get_user_model


User = get_user_model()

class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, pk, timestamp):
        return (text_type('is_active')+text_type(pk)+text_type(timestamp))

token_generator=AppTokenGenerator()

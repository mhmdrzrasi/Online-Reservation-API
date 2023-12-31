from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, phone_number, password):

        if not email:
            raise ValueError("Users must have an email address")

        if not phone_number:
            raise ValueError("Users must have a phone number")

        user = self.model(
            email=self.normalize_email(email),
            phone_number=phone_number
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password):
        user = self.create_user(email, phone_number, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

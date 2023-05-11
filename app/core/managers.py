from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(
        self, email, password=None, first_name=None, last_name=None, phone=None
    ):
        if not email:
            raise ValueError("У пользователя должен быть email")
        user = self.model(
            email=self.normalize_email(email),
        )
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = False
        user.is_onboarding = False
        user.phone = phone
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        user = self.model(
            email=email,
            password=password,
        )
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.set_password(user.password)
        user.save(using=self._db)

        return user

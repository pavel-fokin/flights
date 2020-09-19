import pytest


@pytest.fixture
def user(django_user_model):
    username = "new_user"
    password = "Quwye1!!"

    user_ = django_user_model.objects.create(username=username)
    user_.password_ = password
    user_.set_password(password)
    user_.save()
    return user_

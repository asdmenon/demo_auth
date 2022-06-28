from django.contrib.auth.backends import ModelBackend
from .models import CivilIdAuth
from django.contrib.auth.models import User
import requests


class CivilIDBackend(ModelBackend):
    def authenticate(self, request, **kwargs):
        civ_id = kwargs["civil_id"]
        try:
            if CivilIdAuth.objects.filter(civil_id=civ_id).exists():
                civ_obj = CivilIdAuth.objects.get(civil_id=civ_id)
                if civ_obj.user is None:
                    cv_user = User(username=civ_id)
                    cv_user.save()
                    civ_obj.user = cv_user
                civ_obj.save()
                return civ_obj.user
            # If a CivilId object does not exist, create a user and CivilId object to store.
            else:
                cv_user = User(username=civ_id)
                cv_user.save()
                civ_obj = CivilIdAuth.objects.create(user=cv_user, civil_id=civ_id)
                civ_obj.save()
                return civ_obj.user
        except CivilIdAuth.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return CivilIdAuth.objects.get(civil_id=user_id)
        except CivilIdAuth.DoesNotExist:
            return None

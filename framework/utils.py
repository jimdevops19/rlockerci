import subprocess
from framework import constants, settings
import logging

logger = logging.getLogger(__name__)


class OcOutput(list):
    """
    Class takes a list of output (table kubectl output)
        and converts it to a dictionary to read columns easier
    Example:
        ["NAME","STATUS","queue_service_pod","Running"] - >
        {
            "name":"queue_service_pod",
            "status":"running"
        }
    Validations:
        List length is even, if not, something in the received list is wrong
    """

    def as_dict(self) -> dict:
        l = len(self) / 2
        l = int(l) if l.is_integer() and l != 0 else None
        if l:
            keys = map(
                str.lower, self[:l]
            )  # Better to have lower char keys, more pythonic
            values = map(
                str.lower, self[l:]
            )  # Better to have lower char keys, more pythonic
            return dict(zip(keys, values))
        else:
            return {}


class DjangoPod:
    def __init__(self, name=None):
        self.name = name or self.get_first_pod_from_deployment()
        self.__django_superuser = None

    def get_first_pod_from_deployment(self):
        django_pod_name_command = f"oc get pods -n {settings.get('NAMESPACE')} -l {constants.LABEL_STR_DJANGO} -o=jsonpath={{@.items[0].metadata.name}}"
        pod_name = (
            subprocess.check_output(django_pod_name_command, shell=True)
            .decode("utf-8")
            .rstrip()
        )
        return pod_name

    def migrate_db(self):
        migrate_db_cmd = f"oc exec -n {settings.get('NAMESPACE')} {self.name} -- python manage.py migrate"
        run_migrate_db = (
            subprocess.check_output(migrate_db_cmd, shell=True).decode("utf-8").rstrip()
        )

        # TODO: REPLACE TO LOGGER:
        print(run_migrate_db)

        return None

    def create_or_get_super_user(self):
        try:
            superuser_cmd = f"oc exec -n {settings.get('NAMESPACE')} {self.name} -- python manage.py createsuperuser --noinput"
            run_create_super_user = (
                subprocess.check_output(superuser_cmd, shell=True)
                .decode("utf-8")
                .rstrip()
            )

            # TODO: REPLACE TO LOGGER:
            print(run_create_super_user)

            return None
        except:
            logger.warning(
                msg="Skipping superuser creation, user might be already existing!"
            )

        finally:
            # TODO GET THE SUPERUSER USER DYNAMICALLY AND NOT HARDCODE:
            self.__django_superuser = "admin"

    def get_superuser_token(self):
        get_user_token_cmd = f"oc exec -n {settings.get('NAMESPACE')} {self.name} -- python manage.py retrieve_token -u {self.__django_superuser}"
        run_get_user_token = (
            subprocess.check_output(get_user_token_cmd, shell=True)
            .decode("utf-8")
            .rstrip()
        )

        return run_get_user_token

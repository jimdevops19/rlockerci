import os
from framework import constants, settings
from framework.pipeline_utils import Dir, ProcessTemplateFile

# TODO: THOSE CLASSES COULD BE SINGLETON, CONSIDER CONVERTING THEM
class HelmBase:
    ACTION = None
    INSTANCES = []
    REPLACEMENT_DICT = {}

    def __init__(self):
        self.__class__.run()
        self.__class__.INSTANCES.append(self)


    @classmethod
    def __template_files(cls):
        """
        Process the replacement_dict
        """
        if not cls.REPLACEMENT_DICT == {}:
            with Dir(constants.RLOCKER_CHART_DIR):
                tpl_file = ProcessTemplateFile("values.yaml")
                tpl_file.process(cls.REPLACEMENT_DICT)

    @classmethod
    def __deploy(cls):
        with Dir(constants.RLOCKER_CHART_DIR):
            os.system(
                f"helm {cls.ACTION} {settings.get('RELEASE_NAME')} --namespace={settings.get('NAMESPACE')} ."
            )

    @classmethod
    def run(cls):
        cls.__template_files()
        cls.__deploy()

class HelmChartInstallRun(HelmBase):
    ACTION = "install"
    REPLACEMENT_DICT = {
        "QUEUE_SERVICE_TAG" : settings.get("TAGS").get("QUEUE_SERVICE"),
        "DJANGO_TAG" : settings.get("TAGS").get("DJANGO"),
        "NGINX_TAG" : settings.get("TAGS").get("NGINX"),
        "DJANGO_SECRET": settings.get("DJANGO_CHART_VALUES").get("DJANGO_SECRET"),
        "DEBUG": settings.get("DJANGO_CHART_VALUES").get("DEBUG"),
        "DJANGO_SUPERUSER_USERNAME": settings.get("DJANGO_CHART_VALUES").get(
            "DJANGO_SUPERUSER_USERNAME"
        ),
        "DJANGO_SUPERUSER_PASSWORD": settings.get("DJANGO_CHART_VALUES").get(
            "DJANGO_SUPERUSER_PASSWORD"
        ),
        "DJANGO_SUPERUSER_EMAIL": settings.get("DJANGO_CHART_VALUES").get(
            "DJANGO_SUPERUSER_EMAIL"
        ),
        "POSTGRESQL_USER": settings.get("POSTGRESQL_USER"),
        "POSTGRESQL_PASSWORD": settings.get("POSTGRESQL_PASSWORD"),
        "POSTGRESQL_DATABASE": settings.get("POSTGRESQL_DATABASE"),
    }


class HelmChartUpgradeRun(HelmBase):
    ACTION = "upgrade"

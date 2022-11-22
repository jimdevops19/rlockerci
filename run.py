from framework import constants, settings
from framework.component import Component
from framework.pipeline_utils import Dir, ProcessTemplateFile, ProcessRegularFile
from framework.utils import DjangoPod
from framework.helm import HelmChartUpgradeRun, HelmChartInstallRun
import subprocess
import os
import logging

logger = logging.getLogger(__name__)


class Database(Component):
    WAIT_TIME = 120
    POD_CONDITION_CMD = (
        f"oc get pods -l {constants.LABEL_STR_DB} -n {settings.get('NAMESPACE')}"
    )

    def deploy(self):
        """
        Deploy a postgresql database to a cluster
        :return:
        """
        # Process the env.template file so that we can start db deployment
        with Dir(constants.DB_DIR):
            tpl_file = ProcessTemplateFile(constants.ENV_DB_FILE)
            tpl_file.process(
                {
                    "POSTGRESQL_USER": settings.get("POSTGRESQL_USER"),
                    "POSTGRESQL_PASSWORD": settings.get("POSTGRESQL_PASSWORD"),
                    "POSTGRESQL_DATABASE": settings.get("POSTGRESQL_DATABASE"),
                }
            )

            create_ns = f"oc create ns {settings.get('NAMESPACE')} --dry-run=client -o yaml | oc apply -f -"
            process_template = f"oc process postgresql-persistent -n openshift --param-file={constants.ENV_DB_FILE} | oc create -f - -n {settings.get('NAMESPACE')}"

            os.system(create_ns)
            os.system(process_template)

class Web(Component):
    WAIT_TIME = 120
    POD_CONDITION_CMD = (
        f"oc get pods -l {constants.LABEL_STR_DJANGO} -n {settings.get('NAMESPACE')}"
    )

    def __init__(self, django_pod: DjangoPod):
        super(Web, self).__init__()
        self.django_pod = django_pod

    def deploy(self):
        """
        Deployment of Web component
        Currently, we deploy both DJANGO, NGINX from the helm chart.
        :return:
        """
        HelmChartInstallRun()

    def post_deployment(self):
        self.django_pod.migrate_db()
        self.django_pod.create_or_get_super_user()

class QueueService(Component):
    WAIT_TIME = 120
    POD_CONDITION_CMD = f"oc get pods -l {constants.LABEL_STR_QUEUE_SERVICE} -n {settings.get('NAMESPACE')}"

    def __init__(self, web_instance: Web):
        """
        Queue Service component is DEPENDENT on the entire web component
        Hence, we need it's object before initializing successfully the instance
        """
        super(QueueService, self).__init__()
        self.web_instance = web_instance

    def deploy(self):
        """
        Queue service is being deployed with the helm chart, but it does not
            have the necessary key values YET!
        Until the helm chart is completed, we wait for metadata from the Openshift/Kubernetes.
        So that we can also deploy the Queue Service component successfully
        """

        self.template_services_env(
            token=self.web_instance.django_pod.get_superuser_token()
        )
        HelmChartUpgradeRun()

    def template_services_env(self, route=None, token=None):
        """
        This is a function that reads the route generated after rlocker deployment
            and reads the generated full URL.
        And this URL needs to be given as env variable to the queue service as RESOURCE_LOCKER_URL
        :return:
        """
        get_route_cmd = f"oc get route -n {settings.get('NAMESPACE')} resourcelocker -o=jsonpath={{@.spec.host}}".split()
        route = route or subprocess.check_output(get_route_cmd).decode("utf-8").replace(
            "'", ""
        )
        # TODO Make a default value for the token parameter too ?
        with Dir(constants.RLOCKER_CHART_DIR):
            tpl_file = ProcessRegularFile("values.yaml")
            tpl_file.process(
                {
                    "RESOURCE_LOCKER_TOKEN": token,
                    "RESOURCE_LOCKER_URL": f"http://{route}",
                }
            )

def main():
    if not Database.is_pod_exists():
        db = Database()
        db.deploy()
        Database.is_pod_exists(wait=Database.WAIT_TIME)

    if not Web.is_pod_exists():
        HelmChartInstallRun()
        Web.is_pod_exists(wait=Web.WAIT_TIME)

    django_pod = DjangoPod()
    web = Web(
        django_pod
    )
    # TODO: Could be addressed better, Create the django pod instance inside ?
    web.post_deployment()

    # TODO: Add if queueservice exists  ??
    qs = QueueService(web_instance=web)
    qs.template_services_env(token=web.django_pod.get_superuser_token())
    HelmChartUpgradeRun()
    #TODO: This line has to stay commented out, fix the methodology of verifying pod existance here!
    #QueueService.is_pod_exists(wait=QueueService.WAIT_TIME)

    # Finishing Touches:
    cmd_finalization_cmd = f"oc get all -n {settings.get('NAMESPACE')}"
    print("DEPLOYMENT OF RESOURCE LOCKER DONE SUCCESSFULLY! ✔️")

    print(f"PRINTING OUTPUT OF: {cmd_finalization_cmd}")
    os.system(cmd_finalization_cmd)

if __name__ == "__main__":
    main()
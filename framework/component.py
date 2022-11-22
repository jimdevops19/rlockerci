from framework import constants, settings
from abc import abstractmethod
from framework.utils import OcOutput
import time
import logging
import subprocess

logger = logging.getLogger(__name__)


class Component:
    """
    A base class for deploying a component on cluster
    """

    WAIT_TIME = 0
    POD_CONDITION_CMD = None

    def __init__(self):
        assert (
            self.WAIT_TIME > 0
        ), "Component Class Implementation is not complete. Please create a WAIT_TIME Class Variable that is greater than 0"
        assert (
            self.POD_CONDITION_CMD
        ), "Component Class Implementation is not complete. Please create a POD_CONDITION_CMD Class variable. For i.e: oc get pods -l app=app -n ns"

    @abstractmethod
    def deploy(self):
        """
        Run the cmd commands to deploy the component
        :return:
        """
        pass

    @abstractmethod
    def test(self):
        """
        Run the cmd commands to test the component
        :return:
        """
        pass

    @abstractmethod
    def post_deployment(self):
        """
        Run the cmd commands to do things post deployment (for i.e. creating users)
        :return:
        """
        pass

    @classmethod
    def is_pod_exists(cls, wait=0, already_waited=0):
        """
        Parameters:
        :param wait: How much time to wait before raising TimeOut Exception
        :param already_waited: The time already waited initialized as a parameter here,
            because we use recursive calls and always override when passing arg

        Implementation:
            1) Start with a command to check it's output:
            2) Parse the result
            3) Write the condition to check and return True/False accordingly
        """
        result = (
            subprocess.check_output(cls.POD_CONDITION_CMD, shell=True)
            .decode("utf-8")
            .split()
        )
        result = OcOutput(result).as_dict()
        if result.get("status") == constants.STATUS_RUNNING:
            return True
        elif result.get("status") == constants.STATUS_FAILED:
            raise Exception(
                f"Unmatch in the expected phase! Output: {result}\n"
                "Check the logs of the pod!"
            )

        n = 0 or already_waited
        if wait:
            if already_waited > wait:
                raise TimeoutError()
            logger.log(
                level=logging.WARNING,
                msg=f"Executing command: {cls.POD_CONDITION_CMD} \n"
                f"Status is: {result.get('status')} ... {n}/{wait}",
            )
            time.sleep(constants.SLEEP_TIME)

            # Recursion of function, in some time we should get out unless the wait is reached
            cls.is_pod_exists(wait=wait, already_waited=n + constants.SLEEP_TIME)
        else:
            return False

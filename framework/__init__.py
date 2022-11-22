import yaml
from framework import constants

# NOTE: Always use:
# from framework import settings
# to refer to the settings in the project
with open(constants.SETTINGS_FILE, "r") as f:
    settings = yaml.safe_load(f)

import os
from pathlib import Path
import datetime


NOW = datetime.datetime.now().strftime("%H-%M-%S_%m-%d-%Y")
BASE_DIR = Path(__file__).resolve().parent.parent
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.yaml")
SERVICES_CHART_DIR = os.path.join(BASE_DIR, "rlocker-chart", "charts", "services-chart")
DB_DIR = os.path.join(BASE_DIR, "db")
RLOCKER_CHART_DIR = os.path.join(BASE_DIR, "rlocker-chart")
ENV_DB_FILE = "db-data.env"
LABEL_STR_DB = "name=postgresql"
LABEL_STR_DJANGO = "app=django"
LABEL_STR_QUEUE_SERVICE = "app=queue-service"
STATUS_RUNNING = "running"
STATUS_FAILED = "failed"
SLEEP_TIME = 3

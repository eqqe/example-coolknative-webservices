import os
from pathlib import Path

ROOT_DIR = Path(__file__).parent.absolute()
REDIS_ADDRESS = 'redis-master.redis'
MINIO_ADDRESS = 'minio-hl-svc.minio'
FLUENT_ADDRESS = 'fluentd.knative-monitoring'

LANGUAGE_ID_FILE_NAME = 'lid.176.bin'
LANGUAGE_ID_BUCKET_NAME = 'apps-resources'

# TODO change 90 to MINIO_BUCKET_LOGS_EXPIRATION_DAYS from
# TODO config map of cicd config-install-azure-kubernetes-infrastructure
MINIO_BUCKET_LOGS_EXPIRATION_DAYS = 90

EVENT_LISTENER_TEKTON_ADDRESS = 'http://el-internal-listener.cicd:8080'
GET_LOGS_KNATIVE_MONITORING_ADDRESS = 'http://get-logs.knative-monitoring/'

DEBUG = "gunicorn" not in os.environ.get("SERVER_SOFTWARE", "")

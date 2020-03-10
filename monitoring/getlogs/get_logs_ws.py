import os
from utils_webservices.definitions import get_minio_client
from utils_webservices.flask_utils import setup_app, declare_method, GetLogsJob

app = setup_app()
kwargs = {'mc': get_minio_client()}
declare_method(app, 'get_logs', GetLogsJob, **kwargs)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8088)))

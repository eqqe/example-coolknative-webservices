import os
from utils_webservices.flask_utils import setup_app, declare_method
from namespace1.webservice.utils import MyJob

app = setup_app()
declare_method(app, 'webservice', MyJob)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8086)))

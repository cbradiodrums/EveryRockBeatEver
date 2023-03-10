import os
import secrets
from flask import Flask


def create_app(test_config=None):
    """ Create and configure an instance of the Flask application.
        Read Footer for launch instructions. """
    # Instantiate APP and Assign APP Context
    app = Flask(__name__, instance_relative_config=True, static_folder='_static')
    app_key = secrets.token_hex(16)
    app.config.from_mapping(APP_CONTEXT=os.getenv('CONTEXT'), APP_VERSION='1.0.0.1b',
                            SECRET_KEY=f'{app_key}')

    # If this is a Full environment, use all resources (development)
    if os.getenv('CONTEXT') == 'FULL':
        app.config.from_mapping(
            # Use Cloud Resources
            CLOUD_SERVER=os.getenv('ENDPOINT_URL'), CLOUD_REGION=os.getenv('REGION_NAME'),
            CLOUD_SECRET_ID=os.getenv('CLOUD_SECRET_ID'), CLOUD_SECRET_KEY=os.getenv('CLOUD_SECRET_KEY'),
            CLOUD_BUCKET=os.getenv('BUCKET'),
            # Catalog App Version
            APP_KEY=app_key
        )
    # If this is a Cloud deployment, use cloud resources (production with multiple users)
    elif os.getenv('CONTEXT') == 'CLOUD':
        app.config.from_mapping(
            # Use Exclusively Cloud Resources
            CLOUD_SERVER=os.getenv('ENDPOINT_URL'), CLOUD_REGION=os.getenv('REGION_NAME'),
            CLOUD_SECRET_ID=os.getenv('CLOUD_SECRET_ID'), CLOUD_SECRET_KEY=os.getenv('CLOUD_SECRET_KEY'),
            CLOUD_BUCKET=os.getenv('BUCKET'),
            # Catalog App Version
            APP_KEY=app_key
        )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register the database commands
    from EveryRockBeatEver import db

    # apply the blueprints to the app
    from EveryRockBeatEver import views, functions

    app.register_blueprint(views.bp)
    app.register_blueprint(functions.bp)
    app.add_url_rule("/", endpoint="index")

    return app

# -- To Run app ('EveryRockBeatEver') (from top level in Terminal) --
# $ python -m venv venv  # Virtual environment
# $ source venv/Scripts/activate  # (bash terminal)
# pip install -r requirements.txt
# $ flask --app EveryRockBeatEver --debug run  # (debug tag optional)

# -- To Run Pytest (from top level in Terminal) --
# $ python -m pytest

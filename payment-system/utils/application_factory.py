from base.connect_db import ConnectDB
from controller.user_controller import user_blueprint
from flask_api import FlaskAPI

from controller.root_controller import root_blueprint
from controller.wallet_controller import wallet_blueprint


def create_app():
    app = FlaskAPI(__name__)

    ConnectDB.connect_database()

    app.register_blueprint(wallet_blueprint, url_prefix='/wallet')
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(root_blueprint, url_prefix='')


    return app

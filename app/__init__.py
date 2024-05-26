

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_mail import Mail





load_dotenv()
secret_key = os.getenv('SECRET_KEY')
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
mail = Mail()


def create_app():
    app = Flask(__name__)
    api = Api(app)
    app.config['SECRET_KEY'] = str(secret_key)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:wahid1234@localhost:3306/bank'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587  # 465 for SSL
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'your-email@gmail.com' # replace with real gmail id
    app.config['MAIL_PASSWORD'] = 'your-email-password'# replace with gmail-id's password
    mail.init_app(app)
    db.init_app(app)
    jwt.init_app(app)

    from app.controllers.signup import signup
    app.register_blueprint(signup, url_prefix = '/auth')
    from app.controllers.login import login
    app.register_blueprint(login, url_prefix = '/auth')
    from app.controllers.logout import logout
    app.register_blueprint(logout, url_prefix = '/auth')
    from app.controllers.role_change import Role_Change
    api.add_resource(Role_Change, '/change_role/<int:user_id>')
    from app.controllers.account_details import AccountDetailsBP
    api.add_resource(AccountDetailsBP, '/account_details', '/account_details/<int:user_id>')
    from app.controllers.transaction import TransactionAPI
    api.add_resource(TransactionAPI, '/transaction', '/transaction/<int:transaction_id>')
    from app.controllers.transaction_with_days import TransactionWithDaysAPI
    api.add_resource(TransactionWithDaysAPI, '/transactionwithdays', '/transactionwithdays/<int:days>')
    from app.controllers.banker_account_list import BankerAccountAPI
    api.add_resource(BankerAccountAPI, '/banker/accounts', '/banker/accounts/<int:user_id>')
    from app.controllers.banker_transaction_list import BankerTransactionAPI
    api.add_resource(BankerTransactionAPI, '/banker/transaction', '/banker/transaction/<int:user_id>')
    from app.controllers.mail_transaction import MailRequestAPI
    api.add_resource(MailRequestAPI, '/transaction_mail_request')



    return app
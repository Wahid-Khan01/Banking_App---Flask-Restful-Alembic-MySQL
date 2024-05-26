from app import db



class AccountDetails(db.Model):
    __tablename__ = "account_details"

    account_id = db.Column(db.Integer, primary_key=True)
    account_holder_name = db.Column(db.String(100), nullable=False)
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    ifsc_code = db.Column(db.String(20), nullable=False)
    branch_name = db.Column(db.String(100), nullable=False)
    father_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    mobile_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    balance = db.Column(db.Float, nullable=False)
    nominee = db.Column(db.String(100), nullable=True)
    pan_linked = db.Column(db.Boolean, default=False)
    account_type = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

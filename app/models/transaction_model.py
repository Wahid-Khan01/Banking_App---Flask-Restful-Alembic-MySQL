from app import db


class Transaction(db.Model):
    __tablename__ = "transaction"

    transaction_id = db.Column(db.Integer, primary_key=True)
    debit = db.Column(db.Float, nullable=True)
    credit = db.Column(db.Float, nullable=True)
    debit_type = db.Column(db.String(50), nullable=True)
    credit_type = db.Column(db.String(50), nullable=True)
    location = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    

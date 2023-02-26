from config.config import *
import bcrypt
from datetime import datetime
class ResidentInformation(UserMixin, db.Model):
    __tablename__ = 'Resident_Information'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    resident_name = db.Column(db.String(300))
    resident_email = db.Column(db.String(300), unique=True, index=True)
    password = db.Column(db.String(200))
    self_cnic_number = db.Column(db.BigInteger)
    owner_cnic_number = db.Column(db.BigInteger)
    flat_number = db.Column(db.String(10))
    confirmed = db.Column(db.Boolean, default=False)
    confirmed_on = db.Column(db.String(80))
    registration_count = db.Column(db.Integer, autoincrement=True)
    
    def __init__(self, resident_name, resident_email, password, self_cnic_number, owner_cnic_number, flat_number,confirmed_on,registration_count):
        self.resident_name = resident_name
        self.resident_email = resident_email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.self_cnic_number = self_cnic_number
        self.owner_cnic_number = owner_cnic_number
        self.flat_number = flat_number
        self.confirmed_on = datetime.now()
        self.registration_count=registration_count

class ResidentInformationMatch(db.Model):
    __tablename__ = 'Resident_Information_Match'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_cnic_number = db.Column(db.BigInteger, nullable=False)
    flat_number = db.Column(db.String(10))


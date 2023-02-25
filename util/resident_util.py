from model.resident_model import *
from config.config import *

def LoadUserById(user_id):
    return ResidentInformation.query.get(int(user_id))


def get_self_cnic_number(self_cnic_number):
    return ResidentInformation.query.filter_by(self_cnic_number=self_cnic_number).first()
    
def get_owner_cnic_number(owner_cnic_number):
    return ResidentInformationMatch.query.filter_by(owner_cnic_number=owner_cnic_number).first()

def get_flat_number(flat_number):
    return ResidentInformationMatch.query.filter_by(flat_number=flat_number).first()

import re
def is_valid_email(email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(regex, email))

def get_owner_cnic_number_limit(owner_cnic_number):
    return ResidentInformation.query.filter_by(owner_cnic_number=owner_cnic_number).all()

def add_resident(resident_name, resident_email,password,self_cnic_number,owner_cnic_number,flat_number,confirmed_on,registration_count):
    resident = ResidentInformation(resident_name=resident_name, resident_email=resident_email,password=password,self_cnic_number=self_cnic_number,owner_cnic_number=owner_cnic_number,flat_number=flat_number,confirmed_on=confirmed_on,registration_count=registration_count)
    db.session.add(resident)
    db.session.commit()

from model.resident_model import *
from config.config import *
from flask import *

def LoadUserById(user_id):
    return ResidentInformation.query.get(int(user_id))

def get_resident_email(resident_email):
    return ResidentInformation.query.filter_by(resident_email=resident_email).first()

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


def get_cnic_of_flat_number(flat_number,owner_cnic_number):
    return ResidentInformationMatch.query.filter_by(flat_number=flat_number, owner_cnic_number=owner_cnic_number).first()

def get_owner_flat_number(flat_number):
    return ResidentInformation.query.filter_by(flat_number=flat_number).all()

def add_resident(resident_name, resident_email,password,self_cnic_number,owner_cnic_number,flat_number,confirmed_on,registration_count):
    resident = ResidentInformation(resident_name=resident_name, resident_email=resident_email,password=password,self_cnic_number=self_cnic_number,owner_cnic_number=owner_cnic_number,flat_number=flat_number,confirmed_on=confirmed_on,registration_count=registration_count)
    db.session.add(resident)
    db.session.commit()

import time,uuid,hashlib
import threading

token_hashes = {}

def generate_activation_token(email):
    payload = {'email': email, 'exp': time.time() + 300}
    token = str(uuid.uuid4().hex)[:10]
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    token_hashes[token_hash] = payload
    return token

def verify_activation_token(token):
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    payload = token_hashes.get(token_hash)
    if payload is not None and payload['exp'] > time.time():
        return payload['email']
    else:
        return None

def delete_token(token):
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    if token_hash in token_hashes:
        del token_hashes[token_hash]

def delete_expired_tokens():
    while True:
        time.sleep(60)
        now = time.time()
        expired_tokens = [token_hash for token_hash, payload in token_hashes.items() if payload['exp'] <= now]
        for token_hash in expired_tokens:
            del token_hashes[token_hash]
threading.Thread(target=delete_expired_tokens, daemon=True).start()


def send_verification_email(email,name):
    token = generate_activation_token(email)
    url = url_for('resident_model.activate', token=token, _external=True)
    msg = Message('Verify your email address', sender='cryptonain5@gmail.com', recipients=[email])
    msg.html = render_template('verify_email.html', url=url,name=name)
    mail.send(msg)
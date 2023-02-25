from flask import *
from config.config import *
from util.resident_util import *
import bcrypt
resident_router  = Blueprint('resident_model',__name__,static_folder='static', template_folder='view/template')
login_manager.login_view = 'resident_model.login'

@login_manager.user_loader
def load_user(user_id):
    return LoadUserById(user_id)

@resident_router.route('/register',methods=['POST','GET'])
def resident_register():
    try:
        if request.method == 'POST':
            resident_name = request.form.get('resident-name')
            resident_email = request.form.get('resident-email')
            self_cnic_number = request.form.get('self-cnic-number')
            owner_cnic_number = request.form.get('owner-cnic-number')
            flat_number = request.form.get('flat-number')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm-password')
            existing_resident = get_self_cnic_number(self_cnic_number)
            if existing_resident:
                error_message = "The provided CNIC number already exists"
                return render_template('register.html', error_message=error_message)

            existing_owner = get_owner_cnic_number(owner_cnic_number)
            if not existing_owner:
                error_message = "The provided owner's CNIC number does not exist in the database"
                return render_template('register.html', error_message=error_message)

            existing_flat = get_flat_number(flat_number)
            if not existing_flat:
                error_message = "The provided flat number does not exist in the database"
                return render_template('register.html', error_message=error_message)

            if password != confirm_password:
                error_message = "The provided passwords do not match"
                return render_template('register.html', error_message=error_message)

            if len(password) < 8:
                error_message = "The password should have a minimum length of 8 characters"
                return render_template('register.html', error_message=error_message)

            if not is_valid_email(resident_email):
                error_message = "The provided email is not valid"
                return render_template('register.html', error_message=error_message)

            owner_residents = get_owner_cnic_number_limit(owner_cnic_number)
            if len(owner_residents) >= 3:
                error_message = "You have reached the maximum limit of registered residents for this owner"
                return render_template('register.html', error_message=error_message)
            
            add_resident(resident_name=resident_email,resident_email=resident_email,password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),self_cnic_number=self_cnic_number,owner_cnic_number=owner_cnic_number,flat_number=flat_number,confirmed_on=datetime.now(), registration_count=+1)
            message = "Registration successful"
            return render_template('register.html', message=message)
    except Exception as e:
            error_message = f'Error creating user: {str(e)}'
            return render_template('register.html', error_message=error_message)

    return render_template('register.html'),404

@resident_router.route('/')
def resident_login():
    return render_template('login.html')
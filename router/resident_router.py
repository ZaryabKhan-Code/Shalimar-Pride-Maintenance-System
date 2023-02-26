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
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_model.resident_dashboard_route'))
    try:
        if request.method == 'POST':
            resident_name = request.form.get('resident-name')
            resident_email = request.form.get('resident-email')
            self_cnic_number = request.form.get('self-cnic-number')
            owner_cnic_number = request.form.get('owner-cnic-number')
            flat_number = request.form.get('flat-number')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm-password')
            
            existing_resident_email = get_resident_email(resident_email)
            if existing_resident_email:
                error_message = "The email already exists"
                return render_template('register.html', error_message=error_message)
            
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
            
            check_flat_mumber_with_cnic = get_cnic_of_flat_number(flat_number,owner_cnic_number)
            
            if not check_flat_mumber_with_cnic:
                error_message = "The owner of the flat number is incorrect"
                return render_template('register.html',error_message=error_message) 
            
            if password != confirm_password:
                error_message = "The provided passwords do not match"
                return render_template('register.html', error_message=error_message)

            if len(password) < 8:
                error_message = "The password should have a minimum length of 8 characters"
                return render_template('register.html', error_message=error_message)

            if not is_valid_email(resident_email):
                error_message = "The provided email is not valid"
                return render_template('register.html', error_message=error_message)
            owner_residents = get_owner_flat_number(flat_number)
            if len(owner_residents) >= 3:
                error_message = "You have reached the maximum limit of registered residents for this owner"
                return render_template('register.html', error_message=error_message)
            
            add_resident(resident_name=resident_name,resident_email=resident_email,password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),self_cnic_number=self_cnic_number,owner_cnic_number=owner_cnic_number,flat_number=flat_number,confirmed_on=datetime.now(), registration_count=+1)
            send_verification_email(resident_email,resident_name)
            
            message = "Registration successful, activation link sent to email"
            return render_template('register.html', message=message)
    except Exception as e:
            error_message = f'Error creating user: {str(e)}'
            return render_template('register.html', error_message=error_message)

    return render_template('register.html'),404

@resident_router.route('/check_cnic/<cnic>')
def check_cnic(cnic):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_model.resident_dashboard_route'))
    existing_resident = get_self_cnic_number(cnic)
    if existing_resident:
        return jsonify({'error': 'The provided CNIC number already exists'})
    else:
        return jsonify({})
    
@resident_router.route('/owner_check_cnic/<cnic>',methods=['GET'])
def owner_check_cnic(cnic):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_model.resident_dashboard_route'))
    existing_owner = get_owner_cnic_number(cnic)
    if not existing_owner:
        return jsonify({'error': "The provided owner's CNIC number does not exist in the database"})
    else:
        return jsonify({})

@resident_router.route('/check_flat_number/<flat_number>',methods=['GET'])
def check_flat_number(flat_number):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_model.resident_dashboard_route'))
    existing_flat = get_flat_number(flat_number)
    if not existing_flat:
        return jsonify({'error': "The provided flat number does not exist in the database"})
    else:
        return jsonify({})

@resident_router.route('/check_email/<email>')
def check_email(email):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_model.resident_dashboard_route'))
    email_resident = get_resident_email(email)
    if email_resident:
        return jsonify({'error': 'Email already exists'})
    else:
        return jsonify({})


@resident_router.route('/check_flat', methods=['POST'])
def check_flat():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_model.resident_dashboard_route'))
    data = request.json
    flat_number = data.get('flat_number')
    owner_cnic_number = data.get('owner_cnic_number')
    
    check_flat_mumber_with_cnic = get_cnic_of_flat_number(flat_number, owner_cnic_number)
    
    if check_flat_mumber_with_cnic:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False}), 200

@resident_router.route('/check_max_residents', methods=['POST'])
def check_max_residents():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_model.resident_dashboard_route'))
    flat_number = request.json.get('flat_number')
    owner_residents = get_owner_flat_number(flat_number)
    
    if len(owner_residents) >= 3:
        return jsonify({'success': False, 'message': 'You have reached the maximum limit of registered residents for this owner'})
    
    return jsonify({'success': True})

@resident_router.route('/activate')
def activate():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_model.resident_dashboard_route'))
    token = request.args.get('token')
    try:
        email = verify_activation_token(token)
        if email is not None:
            activate = get_resident_email(email)
            activate.confirmed = True
            db.session.commit()
            delete_token(token)
            flash('Your email has been verified. You can now log in.')
            return render_template('verification_result.html', success=True)
        else:
            return render_template('verification_result.html', success=False)       
    except Exception as e:
        return f'Error Creating Token Contact Support'

@resident_router.route('/',methods=['POST','GET'])
def resident_login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_model.resident_dashboard_route'))
    try:
        if request.method == 'POST':
            cnic = request.form['self-cnic-number']
            password = request.form['password']
            user = get_self_cnic_number(cnic)
            if not user:
                error_message='Incorrect cnic or password.'
                return render_template('login.html', error_message=error_message)
            if not bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'):
                error_message='Incorrect email or password.'
                return render_template('login.html', error_message=error_message)
            login_user(user)
            return redirect(url_for('dashboard_model.resident_dashboard_route'))
        return render_template('login.html')
    except Exception as e:
        error_message = f'Loggin access denied: {str(e)}'
        return render_template('login.html', error_message=error_message)

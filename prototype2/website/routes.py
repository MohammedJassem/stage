from website import app,db
from flask import render_template,redirect, url_for, flash
from website.models import Item,User,Admin#,Role,UserRoles
from website.forms import RegisterForm,LoginForm
key_list = ["key1","key2","key3","key4","key5","key6"]
from flask_login import login_user,logout_user, login_required






@app.route('/')
@app.route('/home')
@login_required
def home():
	return render_template('home.html')


@app.route('/MapData')
@login_required
def Maps_data():
	items = Item.query.all()
	return render_template('MapsData.html', items=items)


@app.route('/team')
@login_required
def team():
	return render_template('team.html')

@app.route('/about')
@login_required
def About():
	return render_template('about.html')


@app.route('/Register',methods=['GET','POST'])
def Register():
	form = RegisterForm()
	
	
	if (form.validate_on_submit()) and (form.Admin_key.data in key_list):
		Admin_to_create = User(username=form.username.data,
			email_address=form.email_address.data,
			password=form.password1.data,Admin_key=form.Admin_key.data)
		#Admin_to_create.roles.append(Role(name='Admin'))
		db.session.add(Admin_to_create)
		db.session.commit()
		
		return redirect(url_for('home'))
	elif form.validate_on_submit() and (form.Admin_key.data not in key_list):
		User_to_create = User(username=form.username.data,email_address=form.email_address.data,password=form.password1.data)
		#User_to_create.roles.append(Role(name='Admin'))
		db.session.add(User_to_create)
		db.session.commit()
		return redirect(url_for('home'))
	if form.errors != {}: #If there are not errors from the validations
		for err_msg in form.errors.values():
			flash(f'There was an error with creating a user: {err_msg}', category='danger')

	return render_template('register.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('home'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home"))

	

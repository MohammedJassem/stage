from website import app,db
from flask import render_template,redirect, url_for
from website.models import Item,User,Admin
from website.forms import RegisterForm
key_list = ["key1","key2","key3","key4","key5","key6",]
@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html')


@app.route('/MapData')
def Maps_data():
	items = Item.query.all()
	return render_template('MapsData.html', items=items)


@app.route('/team')
def team():
	return render_template('team.html')

@app.route('/about')
def About():
	return render_template('about.html')


@app.route('/Register',methods=['GET','POST'])
def Register():
	form = RegisterForm()
	
	
	if form.validate_on_submit() and form.Admin_key.data in key_list:
		Admin_to_create = Admin(username=form.username.data,
			email_address=form.email_address.data,
			password_hash=form.password1.data,Admin_key=form.Admin_key.data)
		db.session.add(Admin_to_create)
		db.session.commit()
		
		return redirect(url_for('home'))
	elif form.validate_on_submit() :
		User_to_create = User(username=form.username.data,email_address=form.email_address.data,password_hash=form.password1.data)
		
		db.session.add(User_to_create)
		db.session.commit()
		return redirect(url_for('home'))
	if form.errors != {}: #If there are not errors from the validations
		for err_msg in form.errors.values():
			print(f'There was an error with creating a user: {err_msg}')

	return render_template('register.html', form=form)
	

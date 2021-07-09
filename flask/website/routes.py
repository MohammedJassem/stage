from website import app,db
from flask import render_template,redirect, url_for, flash
from website.models import Item,User,Admin,Role
from website.forms import RegisterForm,LoginForm,AddSensorForm,DeleteSensorForm,UpdateSensorForm,DeleteAdminForm
key_list = ["key1","key2","key3","key4","key5","key6"]
from flask_login import login_user,logout_user, login_required,LoginManager
from flask_user import roles_required,roles_accepted
from cassandra.cluster import Cluster
cluster = Cluster()
session = cluster.connect('water_leak')
dic = {}

login_manager = LoginManager()
import uuid
@app.route('/')
@app.route('/home')
@login_required

def home():
	items = Item.query.all()
	return render_template('home.html', items=items)


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
@roles_accepted("admin")
def About():
	return render_template('about.html')


@app.route('/Register',methods=['GET','POST'])
#@roles_required('admin')

def Register():
	form = RegisterForm()
	
	
	if (form.validate_on_submit()) and (form.Admin_key.data in key_list):
		a=form.username.data
		b=form.email_address.data
		c=form.password1.data
		d=form.Admin_key.data
		f=uuid.uuid1()
		Admin_to_create = User(username=form.username.data,
			email_address=form.email_address.data,
			password=form.password1.data,Admin_key=form.Admin_key.data,role=Role(name="admin"))
		idtable = Admin_to_create.id
		session.execute("""INSERT INTO user_by_role(username, id, emailAdress,password,Admin_key,idtable)VALUES(%s , %s, %s,%s,%s,%s)""",(a,f,b,c,d,idtable))

		db.session.add(Admin_to_create)
		db.session.commit()
		
		return redirect(url_for('home'))
	elif form.validate_on_submit() and (form.Admin_key.data not in key_list):
		User_to_create = User(username=form.username.data,email_address=form.email_address.data,password=form.password1.data,role=Role(name="user"))
		db.session.add(User_to_create)
		db.session.commit()
		return redirect(url_for('home'))
	if form.errors != {}: #If there are not errors from the validations
		for err_msg in form.errors.values():
			flash('There was an error with creating a user:{}'.format(err_msg), category='danger')

	return render_template('Register.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit()and (form.password.data == "123456"):
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash('Success! You are logged in as:{}'.format(attempted_user.username), category='success')
            return redirect(url_for('home'))
    elif form.validate_on_submit() and (form.password.data != "123456"):
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash('Success! You are logged in as: {}'.format(attempted_user.username), category='success')
            return redirect(url_for('homeAdmin'))
        else:
            flash('Username and password are not match! Please try again', category='danger')
    elif form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash('Success! You are logged in as: {}'.format(attempted_user.username), category='success')
            return redirect(url_for('Maps_data'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)




@app.route('/AddSensor',methods=['GET','POST'])
#@roles_required('admin')

def AddSensor():
	form = AddSensorForm()
	
	
	if form.validate_on_submit():
		a=form.soil_moisture.data
		b=form.status.data
		c=form.time.data
		d=form.sensor_location.data
		f=uuid.uuid1()
		Sensor_to_create = Item(soil_moisture=form.soil_moisture.data,
			status=form.status.data,
			time=form.time.data,sensor_location=form.sensor_location.data)
		db.session.add(Sensor_to_create)
		db.session.commit()
		idtable = Sensor_to_create.id
		#dic[idtable] = str(f)
	
		session.execute("""INSERT INTO sensor_by_status(status,id,soil_moisture,time,sensor_location,idtable)VALUES(%s , %s, %s,%s,%s,%s)""",(a,f,b,c,d,idtable))

		return redirect(url_for('home'))

	if form.errors != {}: #If there are not errors from the validations
		for err_msg in form.errors.values():
			flash('There was an error with creating a user: {}'.format(err_msg), category='danger')

	return render_template('AddSensor.html', form=form)


@app.route('/UpdatSensor',methods=['GET','POST'])

def UpdateSensor():
	form = UpdateSensorForm()
	
	
	if form.validate_on_submit():
		item = Item.query.filter_by(id=form.id_.data).first()
		if item:
			item.soil_moisture = form.soil_moisture.data
			item.status = form.status.data
			item.time = form.time.data
			item.sensor_location = form.sensor_location.data
			db.session.commit()
		idtable = item.id
		#key = dic[10]
		future = session.execute("SELECT * FROM sensor_by_status ")
		for row in future:
			if row.idtable == idtable:
				session.execute("UPDATE sensor_by_status SET time=%s,sensor_location=%s,soil_moisture=%s,status=%s WHERE id=%s",(item.time,item.sensor_location,item.soil_moisture,item.status,row.id ))

		return redirect(url_for('home'))

	if form.errors != {}: #If there are not errors from the validations
		for err_msg in form.errors.values():
			flash('There was an error with updating the Item: {}'.format(err_msg), category='danger')

	return render_template('UpdateSensor.html', form=form)






@app.route('/DeleteSensor',methods=['GET','POST'])
#@roles_required('admin')

def DeleteSensor():
	form=DeleteSensorForm()
	item = Item.query.filter_by(id=form.id_.data).first()
	
	if item:
		idtable = item.id
		keyy = "null"
		future = session.execute("SELECT * FROM sensor_by_status ")
		for row in future:
			if row.idtable == idtable:
				session.execute("UPDATE sensor_by_status SET time=%s,sensor_location=%s,soil_moisture=%s,status=%s,idtable=%s WHERE id=%s",(keyy,keyy,keyy,keyy,0,row.id ))
		db.session.delete(item)
		db.session.commit()
	return render_template('DeleteSensor.html', form=form)




@app.route('/DeleteAdmin',methods=['GET','POST'])
#@roles_required('admin')

def DeleteAdmin():
	form=DeleteAdminForm()
	item = User.query.filter_by(username=form.name.data).first()
	if item:
		idtable = item.id
		keyy = "null"
		future = session.execute("SELECT * FROM user_by_role ")
		for row in future:
			if row.idtable == idtable:
				session.execute("UPDATE sensor_by_status SET admin_key=%s,emailadress=%s,idtable=%s,password=%s, username=%s WHERE id=%s",(0,keyy,0,keyy,keyy,row.id ))

		db.session.delete(item)
		db.session.commit()
	return render_template('DeleteAdmin.html', form=form)


@app.route('/homebase')
def homebase():
    	return render_template('base.html')






@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out!", category='info')
    #return render_template('login.html')
    return redirect(url_for("login_page"))

	

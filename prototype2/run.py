from website import app


if __name__ == '__main__':
	app.run(debug=True)



"""
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///website.db'
db = SQLAlchemy(app)



class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    percentage = db.Column(db.Integer(), nullable=False)
    place = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)

    def __repr__(self):
        return f'Item {self.name}'
		



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
"""

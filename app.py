from enum import unique
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from random import choice
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///demo.db'
app.config['SECRET_KEY'] = 'some random string'
db = SQLAlchemy(app)

class ShortUrls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=True)
    short_id = db.Column(db.String(20), nullable=True, unique=True)
    created_at = db.Column(db.DateTime(), default=datetime.now(), nullable=False)

def generate_short_id(num_of_chars: int):
    return ''.join(choice(string.ascii_letters+string.digits) for _ in range(num_of_chars))

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        short_id = request.form['custom_id']

        if url and short_id:
            flash('Please only enter one field!')
            return redirect('/')

        if not url and not short_id:
            flash('You must enter at least one field!')
            return redirect('/')
        
        if url and not short_id:
            short_id = generate_short_id(4)
            # short_url = request.host_url + short_id
            new_link = ShortUrls(
                original_url = url, short_id = short_id, created_at = datetime.now()
            )
            try:
                db.session.add(new_link)
                db.session.commit()
            except:
                return 'There was an issue converting your url'
            short_url = request.host_url + short_id
            return render_template('index.html', short_url = short_url) 

        if short_id and not url:
            retreive = ShortUrls.query.filter_by(short_id=short_id.replace(request.host_url, '')).first()
            if retreive is not None:
                return render_template('index.html', short_url = retreive.original_url)
            else:
                flash("There's no record of this url")
                return redirect(url_for('index'))
            
    else:
        return render_template('index.html')

@app.route('/<short_id>')
def redirect_url(short_id):
    link = ShortUrls.query.filter_by(short_id=short_id).first()
    if link is not None:    
        return redirect(link.original_url)
    else:
        flash('Invalid URL')
        return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
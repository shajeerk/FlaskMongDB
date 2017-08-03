import os
from flask import Flask, flash, redirect, render_template, request, session, url_for

import mongo

app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile('config.cfg')
app.secret_key = os.urandom(12)



@app.route('/create_collection', methods=['GET', 'POST'])
def create_collection():
    try:
        name = request.form['name']
        address = request.form["address"]
        group = request.form["group"]
        phone = request.form.get("phone")
        offer_amt = request.form.get("offer_amt")
        collected_amt = request.form.get("collected_amt")
        care_of = request.form.get("care_of")
        payment_mode = request.form.get("payment_mode")
        remarks = request.form.get("remarks")
    
        val={
            "name":str(name),
            "address":str(address),
            "group":str(group),
            "phone":str(phone),
            "offer_amt":str(offer_amt),
            "collected_amt":str(collected_amt),
            "care_of":str(care_of),
            "payment_mode":str(payment_mode),
            "remarks":str(remarks),            
        }
        res = mongo.MongoDB().set_collection(val)
        print(res)
        return redirect(url_for('collections'))
    except Exception as e:
        print(e)


@app.route('/collections')
def collections():
    try:
        if session.get("user"):
            grouplist = mongo.MongoDB().group_list()
            res = None #mongo.MongoDB().collection_list()
            return render_template('collection.html',collections=res,groups=grouplist,user=session['user'])
        else:
            return render_template('login.html', error = "Your Session Expired")
    except Exception as e:
        print(e)


@app.route('/create_group', methods=['GET', 'POST'])
def create_group():
    try:
        name = request.form['name']
        res = mongo.MongoDB().set_group(name)
        print(res)
        return redirect(url_for('groups'))
    except Exception as e:
        print(e)


@app.route('/groups')
def groups():
    try:
        if session.get("user"):
            res = mongo.MongoDB().group_list()
            return render_template('group.html',groups=res,user=session['user'])
        else:
            return render_template('login.html', error = "Your Session Expired")
    except Exception as e:
        print(e)


@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    try:
        name = request.form['username']
        password = request.form["password"]
        group = request.form["group"]
        admin = request.form.get("is_admin") or False
    
        val={"username":str(name),"password":str(password),"group":group,"is_admin":admin}
        
        res = mongo.MongoDB().set_user(val)
        return redirect(url_for('users'))
    
    except Exception as e:
        print(e)


@app.route('/users')
def users():
    try:
        if session.get("user"):
            grouplist = mongo.MongoDB().group_list()
            user_list = mongo.MongoDB().users_list()
            return render_template('users.html',users=user_list,groups=grouplist,user=session['user'])
        else:
            return render_template('login.html', error = "Your Session Expired")
    except Exception as e:
        print(e)


@app.route('/home', methods=['GET', 'POST'])
def home():
    
    try:
        session['user'] = request.form['username']
        session['password'] = request.form['password']
        
        res = mongo.MongoDB().check_user(session['user'],session['password'])
        access_right = get_access_user()
        
        if res:
            return render_template('dashboard.html', user=session['user'],is_admin = access_right)
        else:
            return render_template('login.html', error = "Invalid Username or Password")
        
    except Exception as e:
        print(e)


def get_access_user():
    try:
        is_admin = mongo.MongoDB().check_access_right(session['user'])
        if is_admin is None:
            access_right = False
        else:
            access_right = True
            
        return access_right
    except Exception as e:
        print(e)


@app.route('/dashboard')
def dashboard():
    access_right = get_access_user()
    return render_template('dashboard.html', user=session['user'],is_admin = access_right)


@app.route("/logout")
def logout():
    session.pop('username', None)
    session.pop('password', None)
    return render_template('login.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/')
def index():
    return redirect(url_for('login'))



if __name__ == "__main__":

    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='10.161.113.156', port=9000, threaded=True)

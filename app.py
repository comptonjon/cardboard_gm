from flask import Flask, render_template, request, g, session, redirect, flash, jsonify
from models import db, connect_db, User, Card, TradeRequest, RequestCard
from forms import LoginForm, RegisterForm, CardForm, EditUserForm, TradeRequestForm, HiddenRequestForm
from sqlalchemy.exc import IntegrityError
from helpers import delete_record_from_s3, upload_img, load_card, delete_trade_request, decline_trade_request, accept_trade_request
from PIL import Image, UnidentifiedImageError
from ebay_api import get_recent_prices
from constants import API_LIMIT
import io
import os
import json
import datetime

USER_ID = "user_id"

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgres:///cg_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SQLALCHEMY_ECHO'] = True 

connect_db(app)

@app.before_request
def add_user_to_g():
    """Add authenticated user to flask g"""
    if USER_ID in session:
        g.user = User.query.get(session[USER_ID])
    else:
        g.user = None

########## APP ENTRY ROUTES ##########

@app.route('/index')
def show_index():
    """Show user app entry page"""
    return render_template('index.html')

@app.route('/')
def root_route():
    """Direct authentcated user home or unauthenticated user to show_index route"""
    if g.user:
        return redirect(f'/users/{g.user.id}')
    return redirect('/index')

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """Show user the login form.  Handle valid form submission by authenticating user."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(username=form.username.data, password=form.password.data)
        if user:
            add_user_to_session(user)
            return redirect(f'/users/{user.id}')
        else:
            flash("Incorrect Username or Password", 'error')
    return render_template("login.html", form=form)

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    """Register a new user"""
    if g.user:
        return redirect(f'/users/{g.user.id}')
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User.register(username=form.username.data,
                                 password=form.password.data,
                                 email = form.email.data,
                                 first_name = form.first_name.data,
                                 last_name = form.last_name.data)
        if new_user:
            db.session.add(new_user)
            try:
                db.session.commit()
                add_user_to_session(new_user)
                flash("User created", 'success')
                return redirect(f'/users/{new_user.id}')
            except IntegrityError:
                db.session.rollback()
                flash("Username already taken", 'error')
                return redirect('/register')
            except:
                db.session.rollback()
                flash("Error creating user", 'error')
                return redirect('/register')
    return render_template('register.html', form=form)

##########  USER ROUTES  ##########

@app.route('/users')
def show_users():
    """Show all users"""
    users = User.query.order_by(User.last_updated.desc()).limit(API_LIMIT).all()
    return render_template('users.html', users=users)

@app.route('/users/<int:id>')
def show_user(id):
    """Show single user by id"""
    user = User.query.get_or_404(id)
    cards = Card.query.filter(Card.owner_id == id).order_by(Card.last_updated.desc()).limit(API_LIMIT).all()
    return render_template('user.html', user=user, cards=cards)

@app.route('/users/<int:id>/edit', methods=['GET', 'POST'])
def edit_user_form(id):
    """Edit existing user data"""
    user = User.query.get_or_404(id)
    form = EditUserForm(obj=user)
    # delete username and password from the edit form
    del form.username
    del form.password
    if form.validate_on_submit():
        user.email = form.email.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.last_updated = datetime.datetime.utcnow()
        try:
            db.session.commit()
            flash("User account info saved", "success")
            if form.image.data:
                try:
                    img = Image.open(request.files[form.image.name])
                    width, height = img.size
                    img = img.crop((0, 0, min(width, height), min(width, height)))
                    upload_img(img, user)
                    user.has_img = True
                    user.last_updated = datetime.datetime.utcnow()
                    db.session.commit()
                except:
                    db.session.rollback()
                    flash("Image Error", 'error')
        except:
            db.session.rollback()
            flash("Changes could not be saved", 'error')
        return redirect(f'/users/{user.id}')
    return render_template('edit-user.html', user=user, form=form)

@app.route('/users/<int:id>/add_card', methods=['GET', 'POST'])
def add_new_card(id):
    """Add a new card from form data"""
    form = CardForm()
    if form.validate_on_submit():
        new_card = Card.createFromForm(form, owner_id=id)
        db.session.add(new_card)
        try:
            db.session.commit()
            flash("Card successfully added!", 'success')
            if form.image.data:
                try:
                    img = Image.open(request.files[form.image.name])
                    upload_img(img, new_card)
                    new_card.has_img = True
                    db.session.commit()
                except:
                    flash("Image file is unsupported type", 'error')
            return redirect(f'/users/{id}')
        except:
            db.session.rollback()
            flash("Error adding Card", 'error')
    return render_template('add-card.html', form=form)

@app.route('/users/<int:id>/delete', methods=['POST'])
def delete_user(id):
    """Delete the user from the db"""
    user = User.query.get_or_404(id)
    db.session.delete(user)
    try:
        # Delete the user avatar image from the S3 bucket
        delete_record_from_s3(user)
        db.session.commit()
        flash("User Deleted!", 'success')
        return redirect('/logout')
    except:
        db.session.rollback()
        flash("Error deleting user", 'error')
        return redirect("/")

@app.route('/users/<int:id>/requests', methods=['GET', 'POST'])
def show_requests(id):
    """Display trade requests that the user is involved in"""
    if g.user:
        form = TradeRequestForm()
        requests = TradeRequest.query.filter((TradeRequest.to_id == id) | (TradeRequest.from_id == id)).order_by(TradeRequest.last_updated.desc()).all()
        if form.validate_on_submit():
            request = TradeRequest.query.get_or_404(int(form.request_id.data))
            return handle_request_response(request, form) 
        return render_template('requests.html', requests=requests, form=form)
    else:
        flash("You must be logged in for access")
        return redirect("/")
    

##########  CARD ROUTES  ##########

@app.route('/cards')
def show_cards():
    cards = Card.query.order_by(Card.last_updated.desc()).limit(API_LIMIT).all()
    return render_template('cards.html', cards=cards)

@app.route('/cards/<int:id>', methods=['GET', 'POST'])
def show_card(id):
    card = Card.query.get_or_404(id)
    requests = [request for request in card.requests if request.accepted == None and request.valid_items]
    form = TradeRequestForm()
    if form.validate_on_submit():
        request = TradeRequest.query.get_or_404(int(form.request_id.data))
        return handle_request_response(request, form)
    return render_template('card.html', card=card, requests=requests, form=form)

@app.route('/cards/<int:id>/edit', methods=['GET', 'POST'])
def edit_card(id):
    card = Card.query.get_or_404(id)
    form = CardForm(obj=card)
    if form.validate_on_submit():
        load_card(card, form)
        card.last_updated = datetime.datetime.utcnow()
        if form.image.data:
            try:
                img = Image.open(request.files[form.image.name])
                upload_img(img, card)
                card.has_img = True
                db.session.commit()
            except UnidentifiedImageError:
                flash("Image file is unsupported type", 'error')
        try:
            db.session.commit()
            flash("Changes saved", 'success')
            return redirect(f'/users/{card.user.id}')
        except:
            db.session.rollback()
            flash("error saving changes", 'error')
    return render_template('edit-card.html', form=form, card=card)

@app.route('/cards/<int:id>/new-request', methods=['GET', 'POST'])
def create_trade_request(id):
    """Create a new trade request"""
    if g.user:
        form = HiddenRequestForm()
        card = Card.query.get_or_404(id)
        if form.validate_on_submit():
            # Decode the JSON data
            data = json.loads(form.req_data.data)
            # Get the ids from the form
            ids = data.get('c_ids', [])
            # Check that there are offered card ids
            if len(ids) == 0:
                flash('You must select cards to trade', 'error')
                return redirect(request.url)
            # Create the request and add to database
            new_request = TradeRequest(to_id=card.owner_id, from_id=g.user.id)
            db.session.add(new_request)
            db.session.commit()
            # Add the offered request cards to the trade request
            for id in ids:
                request_card = RequestCard(request_id=new_request.id, card_id=id)
                db.session.add(request_card)
                db.session.commit()
            # Add the requested request card to the trade request
            requested_card = RequestCard(requested=True, request_id=new_request.id, card_id=card.id)
            db.session.add(requested_card)
            db.session.commit()
            flash('Request Created', 'success')  
        else:
            # Send card data for title display in template
            requested_card = Card.query.get_or_404(id)
            g_user_cards = g.user.cards
            # Add users card collection in JSON to the template.  This will prevent server calls for a limited data set.
            card_json = []
            for card in g_user_cards:
                card_json.append(card.serialize())
            return render_template('trade-request.html', cards=card_json, requested_card=requested_card, form=form)
    return redirect('/')


@app.route('/cards/<int:id>/delete', methods=['POST'])
def delete_card(id):
    if g.user:
        card = Card.query.get_or_404(id)
        db.session.delete(card)
        try:
            db.session.commit()
            flash("Card Deleted!")
            if card.has_img: 
                delete_record_from_s3(card)
            return redirect(f'/users/{g.user.id}')
        except:
            db.session.rollback()
            flash('Error deleting card')
            return redirect(request.url)
    else:
        flash("You must be logged in for access")
        return redirect('/')

@app.route('/pricing')
def show_ebay_price_lookup():
    return render_template('pricing.html')

##########  API ROUTES  ##########

@app.route('/api/cards')
def get_cards():
    limit = request.args.get('limit', None)
    offset = request.args.get('offset', 0)
    name = request.args.get('searchStr')
    id = request.args.get('userId')
    query = Card.query.order_by(Card.last_updated.desc())
    if id: 
        query = query.filter(Card.owner_id == id)
    if name:
        splitStr = name.split(" ")
        for token in splitStr:
            query = query.filter(Card.title.ilike(f'%{token}%'))
    query = query.offset(offset)
    if limit:
        query = query.limit(limit)
    obj_cards = query.all()
    results = []
    for card in obj_cards:
        results.append(card.serialize())
    return jsonify(results=results)

@app.route("/api/ebay")
def ebay():
    query_string = request.args.get('item')
    return get_recent_prices(query_string)

@app.route('/api/users')
def get_users():
    limit = request.args.get('limit', None)
    offset = request.args.get('offset', 0)
    name = request.args.get('searchStr')
    query = User.query.order_by(User.last_updated.desc())
    if name:
        query = query.filter(User.username.ilike(f'%{name}%'))
    query = query.offset(offset)
    if limit:
        query = query.limit(limit)
    obj_users = query.all()
    users = []
    for user in obj_users:
        users.append(user.serialize())
    return jsonify(results=users)

##########  LOGOUT AND USER SESSION  ##########

@app.route('/logout')
def logout_user():
    session.pop(USER_ID)
    flash("Goodbye!", 'success')
    return redirect('/')

def add_user_to_session(user):
    session[USER_ID] = user.id

def handle_request_response(request, form):
    if form.delete.data:        
        delete_trade_request(request)
        flash('Request Deleted!', 'success')
        return redirect(f'/users/{g.user.id}/requests')
    elif form.decline.data:
        decline_trade_request(request)
        flash('Request Declined!', 'success')
        return redirect('/')
    else:
        accept_trade_request(request)
        flash('Request Accepted!', 'success')
        return redirect('/')


    







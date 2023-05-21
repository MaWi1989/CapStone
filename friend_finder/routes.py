from . import app, db
from .models import User, Post, post_schema, all_posts_schema
from flask import render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import current_user, login_user, logout_user,  login_required
from werkzeug.urls import url_parse   
from werkzeug.security import check_password_hash
from .forms import LoginForm, SignUpForm, PostForm, EmptyForm, SchoolForm
import requests




@app.route('/', methods=['GET', 'POST'])
def home():
    # form = SchoolForm()
    # def see_school_list(city,state):
    #     url = "https://realtor-api-for-real-estate-data.p.rapidapi.com/realtor_data/schools/"

    #     querystring = {"city":f"{city}","state_code":f"{state}","school_level":"elementary","page":"1"}

    #     headers= {
    #     "X-RapidAPI-Key": "9b16110cdemsh97cefceb253d517p1e1aecjsn9ef744f7b15e",
    #     "X-RapidAPI-Host": "realtor-api-for-real-estate-data.p.rapidapi.com"
    #     }

    #     response = requests.get(url, headers=headers, params=querystring)

    #     data = response.json()

    #     school_list = [school['name'] for school in data]
    #     print(school_list)
       
    #     return render_template('home.html', form=form, posts=school_list)
    
    # city = form.city.data
    # state = form.state.data

    # see_school_list(city, state)

    return render_template('home.html')
    




# @app.route('/index')
# @login_required
# def index():
#     posts = [
#         {
#             'author': {'John'},
#             'message': 'Beautiful day in Portland!'
#         },
#         {
#             'author': {'Susan'},
#             'message': 'The Avengers movie was so cool!'
#         }
#     ]
#     return render_template('index.html', title='Index', posts=posts)




@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, key= form.key.data, email=form.email.data, password=form.password.data, city=form.city.data, state=form.state.data, school=form.school.data, grade=form.grade.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        login_user(user)
        return redirect(url_for('user', name=user.name))
    return render_template('signup.html', title='Sign Up', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        print(email, password)
        logged_user = User.query.filter(User.email == email).first()
        if logged_user and check_password_hash(logged_user.password, password):
            print(f'This is the logged user {logged_user}')
            login_user(logged_user)
            flash('You were successfully logged in: Via email/password', 'auth-success')
            return redirect(url_for('user', name=logged_user.name))
    
        else: 
            flash('Your email/password is incorrect', 'auth-failed')  
            return redirect(url_for('login'))
    return render_template('signin.html', form=form)

    


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))




@app.route('/user/<name>')
@login_required
def user(name):
    user = User.query.filter_by(name=name).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.date.desc()).paginate(
        page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('user', name=user.name, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', name=user.name, page=posts.prev_num) \
        if posts.has_prev else None
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url, form=form)





@app.route('/posts', methods=['GET', 'POST'])
@login_required
def see_posts():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, message=form.message.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('see_posts'))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date.desc()).paginate(
        page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('see_posts', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('see_posts', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template("message_board.html", title='Posts', form=form, posts=posts.items,
                          next_url=next_url, prev_url=prev_url)
  




@app.route('/posts/<post_id>/edit', methods=['PUT'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.user_id != current_user.id:
        abort(403)  

    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.message = form.message.data
        db.session.commit()
        flash('Your post has been updated!')
        return redirect(url_for('see_posts'))

    form.title.data = post.title
    form.message.data = post.message

    return render_template('edit_post.html', title='Edit Post', form=form)





@app.route('/posts/<post_id>/delete', methods=['DELETE'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.user_id != current_user.id:
        abort(403)  

    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!')
    return redirect(url_for('see_posts'))

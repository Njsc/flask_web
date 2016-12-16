from . import bp
from forms import UserForm, EditProfileForm, PostForm
from flask import render_template, redirect, session, url_for, current_app, abort, flash, request, make_response
from ..models import db, User, Permission, Post
from datetime import datetime
from ..email import send_email
from flask_login import login_required, current_user
from ..decorators import permission_required


@bp.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query
    pagination = query.order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config[
        'FLASKY_POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    return render_template('index.html', form=form, posts=posts, pagination=pagination, current_time=datetime.utcnow(),
                           show_followed=show_followed)


@bp.route('/all')
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed','',max_age=30*24*60*60)
    return resp
@bp.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed','1',max_age=30*24*60*60)
    return resp



    # posts = Post.query.order_by(Post.timestamp.desc()).all()
    # return render_template('index.html', form=form, posts=posts, current_time=datetime.utcnow())
    # form = UserForm()
    # if form.validate_on_submit():
    #     user = User.query.filter_by(username=form.name.data).first()
    #     if user is None:
    #         user = User(username=form.name.data)
    #         db.session.add(user)
    #         session['know'] = False
    #         if current_app.config['FLASK_ADMIN']:
    #             send_email(current_app.config['FLASK_ADMIN'], 'New User',
    #                        'mail/new_user', user=user)
    #     else:
    #         session['know'] = True
    #     session['name'] = form.name.data
    #     form.name.data = ''
    #     return redirect(url_for('blog.index'))
    # return render_template('index.html', form=form, current_time=datetime.utcnow(),
    #                        know=session.get('know', False),
    #                        name=session.get('name'), title='Index')


@bp.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config[
        'FLASKY_POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    return render_template('user.html', user=user, posts=posts, pagination=pagination)
    # posts = user.posts.order_by(Post.timestamp.desc()).all()
    # return render_template('user.html', user=user, posts=posts)


@bp.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash("You have change your profile")
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.username
    form.location.data = current_user.location
    current_user.about_me = current_user.about_me
    return render_template('edit_profile.html', form=form)


@bp.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', posts=[post])


@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.add(post)
        flash("Post has been update")
        return redirect(url_for('.post', id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    return render_template('edit_post.html', form=form)


@bp.route('/follow/<string:username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid error')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash("You are already followed this user")
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    flash("You have followed this user")
    return redirect(url_for('.user', username=username))


@bp.route('/unfollow/<string:username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash("Invalid error")
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash("You are not followed this user")
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    flash("You have unfollowed this user")
    return redirect(url_for('.user', username=username))


@bp.route('/followers/<string:username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash("Invalid user")
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp} for item in pagination.items]
    return render_template('followers.html', user=user, title='Followers of ', endpoint='.followers',
                           pagination=pagination, follows=follows)


@bp.route('/following/<string:username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash("Invalid user")
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp} for item in pagination.items]
    return render_template('followers.html', user=user, title='Followed By ', endpoint='.followers',
                           pagination=pagination, follows=follows)

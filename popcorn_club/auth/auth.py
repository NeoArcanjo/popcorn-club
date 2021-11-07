from functools import wraps
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flask import current_app as app
from werkzeug.security import check_password_hash, generate_password_hash
from popcorn_club import oauth
from popcorn_club.db import get_db
import time 

oauth = oauth.init_app(app)
bp = Blueprint('auth', __name__, url_prefix='/auth',
               template_folder='templates', static_folder='static')


@bp.route('/disqus')
def disqus():
    disqus = oauth.create_client('disqus')  # create the disqus oauth client
    redirect_uri = url_for('auth.authorize_disqus', _external=True)
    return disqus.authorize_redirect(redirect_uri)


@bp.route('/google')
def google():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('auth.authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@bp.route('/spotify')
def spotify():
    spotify = oauth.create_client('spotify')  # create the spotify oauth client
    redirect_uri = url_for('auth.authorize_spotify', _external=True)
    return spotify.authorize_redirect(redirect_uri)


@bp.route('/facebook')
def facebook():
    # create the facebook oauth client
    facebook = oauth.create_client('facebook')
    redirect_uri = url_for('auth.authorize_facebook', _external=True)
    return facebook.authorize_redirect(redirect_uri)


@bp.route('/facebook/callback')
def authorize_facebook():
    # create the facebook oauth client
    facebook = oauth.create_client('facebook')
    # Access token from facebook (needed to get user info)
    token = facebook.authorize_access_token(client_id=facebook.client_id,
                                            client_secret=facebook.client_secret)
    # userinfo contains stuff u specificed in the scrope
    user_id = token['user_id']
    resp = disqus.userinfo()
    user_info = {'username': token['username'], 'given_name': token['username'],
                 'picture': f'https://disqus.com/api/users/avatars/{token["username"]}.jpg'}
    print(f'https://facebook.com/api/users/avatars/{token["username"]}.jpg')
    # user = oauth.facebook.userinfo()  # uses openid endpoint to fetch user info
    # Here you use the profile/user data that you got and query your database find/register the user
    # and set ur own data in the session not the profile from facebook
    session['profile'] = user_info
    # make the session permanant so it keeps existing after broweser gets closed
    session.permanent = False
    return redirect(url_for('club.index'))


@bp.route('/disqus/callback')
def authorize_disqus():
    disqus = oauth.create_client('disqus')  # create the disqus oauth client
    # Access token from disqus (needed to get user info)
    token = disqus.authorize_access_token(client_id=disqus.client_id,
                                          client_secret=disqus.client_secret)
    # userinfo contains stuff u specificed in the scrope
    user_id = token['user_id']
    resp = disqus.userinfo()
    # user_info = resp.json()
    user_info = {'username': token['username'], 'given_name': token['username'],
                 'picture': f'https://disqus.com/api/users/avatars/{token["username"]}.jpg'}
    print(f'https://disqus.com/api/users/avatars/{token["username"]}.jpg')
    # user = oauth.disqus.userinfo()  # uses openid endpoint to fetch user info
    # Here you use the profile/user data that you got and query your database find/register the user
    # and set ur own data in the session not the profile from disqus
    session['profile'] = user_info
    # make the session permanant so it keeps existing after broweser gets closed
    session.permanent = False
    return redirect(url_for('club.index'))


@bp.route('/spotify/callback')
def authorize_spotify():
    spotify = oauth.create_client('spotify')  # create the spotify oauth client
    # Access token from spotify (needed to get user info)
    token = spotify.authorize_access_token()
    # userinfo contains stuff u specificed in the scrope
    user = oauth.spotify.userinfo()

    session['token'] = token['access_token']
    session['refresh_token'] = token['refresh_token']
    session['token_expiration'] = time.time() + token['expires_in']
    
    user_info = {'username': user['display_name'],
                 'given_name': user['display_name'], 'picture': user['images'][0]['url']}
    # Here you use the profile/user data that you got and query your database find/register the user
    # and set ur own data in the session not the profile from spotify
    session['profile'] = user_info
    session['user_id'] = user
    # make the session permanant so it keeps existing after broweser gets closed
    session.permanent = False
    return redirect(url_for('club.index'))


@bp.route('/callback')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    # Access token from google (needed to get user info)
    token = google.authorize_access_token()
    # userinfo contains stuff u specificed in the scrope
    resp = google.get('userinfo')
    user_info = resp.json()
    user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    # Here you use the profile/user data that you got and query your database find/register the user
    # and set ur own data in the session not the profile from google
    session['profile'] = user_info
    # make the session permanant so it keeps existing after broweser gets closed
    session.permanent = True
    return redirect(url_for('club.index'))


@bp.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    session.clear()
    return redirect(url_for('auth.login'))


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('register.html')


@bp.route("/forgot-password")
def forgot_password():
    return render_template('forgot-password.html')


@bp.route('/', methods=('GET', 'POST'))
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        flash(error)
    return render_template('login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    print(user_id)
    if user_id is None:
        g.user = None
    else:
        g.user = session.get('profile')
        # g.user = get_db().execute(
        #     'SELECT * FROM user WHERE id = ?', (user_id,)
        # ).fetchone()


# # @bp.route('/logout')
# # def logout():
# #     session.clear()
# #     return redirect(url_for('index'))


# def login_required(view):
#     @wraps(view)
#     def wrapped_view(**kwargs):
#         if g.user is None:
#             return redirect(url_for('auth.login'))

#         return view(**kwargs)

#     return wrapped_view


def login_required(view):
    @wraps(view)
    def decorated_function(*args, **kwargs):
        user = dict(session).get('profile', None)
        if user:
            return view(*args, **kwargs)
        return redirect(url_for('auth.login', next=request.url))
    return decorated_function

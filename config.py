CSRF_ENABLED = True
SECRET_KEY = 'MvjhCIQhA5ZaSa32iFAr9dP8gsIdhB058IjBr3ph'
DEBUG = False

# If you find it useful, specify a prefix here and this app will use it in models.py for your database tables.
# TABLE_PREFIX = 'bestsellers' 

APP_SHORTNAME = 'bestsellers' # used in some places like defining what our log or DB is named
USER_APP_NAME = "Bestsellers Database"
LOG_DIR = '/var/log/bestsellers/logs/' # you may want to manually make sure this exists

# settings for uploading images updated 2/5/18
UPLOAD_FOLDER = '/var/www/pyapps/bestsellers/static/data/bestsellers/images/'
ALLOWED_EXTENSIONS = set(['png', 'PNG', 'jpg', 'jpeg', 'JPG', 'JPEG', 'gif', 'GIF'])

DB_NAME = 'bestsellers'
DB_HOST = 'db1.lib.virginia.edu'
DB_PASS = 'Qw6849ICvep'
DB_USER = 'bestsellers'

BINDS = {
    'dbuser': 'mysql+mysqldb://'+DB_USER+':'+DB_PASS+'@'+DB_HOST+'/'+DB_NAME
}
SQLALCHEMY_DATABASE_URI = BINDS['dbuser']
SQLALCHEMY_POOL_RECYCLE = 300


# Mail stuff
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_DEFAULT_SENDER = '"Bestsellers Database" <noreply@uva.edu>';

# Flask-User Endpoints, necessary because bestsellers doesn't live on root.
USER_AFTER_CHANGE_PASSWORD_ENDPOINT      = 'index'              # v0.5.3 and up
USER_AFTER_CHANGE_USERNAME_ENDPOINT      = 'index'              # v0.5.3 and up
USER_AFTER_CONFIRM_ENDPOINT              = 'index'              # v0.5.3 and up
USER_AFTER_FORGOT_PASSWORD_ENDPOINT      = 'index'              # v0.5.3 and up
USER_AFTER_LOGIN_ENDPOINT                = 'index'              # v0.5.3 and up
USER_AFTER_LOGOUT_ENDPOINT               = 'user.login'    # v0.5.3 and up
USER_AFTER_REGISTER_ENDPOINT             = 'index'              # v0.5.3 and up
USER_AFTER_RESEND_CONFIRM_EMAIL_ENDPOINT = 'index'              # v0.5.3 and up
USER_AFTER_RESET_PASSWORD_ENDPOINT       = 'index'              # v0.6 and up
USER_INVITE_ENDPOINT                     = 'index'              # v0.6.2 and up

# Users with an unconfirmed email trying to access a view that has been
# decorated with @confirm_email_required will be redirected to this endpoint
USER_UNCONFIRMED_EMAIL_ENDPOINT          = 'user.login'    # v0.6 and up

# Unauthenticated users trying to access a view that has been decorated
# with @login_required or @roles_required will be redirected to this endpoint
USER_UNAUTHENTICATED_ENDPOINT            = 'user.login'    # v0.5.3 and up

# Unauthorized users trying to access a view that has been decorated
# with @roles_required will be redirected to this endpoint
USER_UNAUTHORIZED_ENDPOINT               = 'index'              # v0.5.3 and up

try:
    from config_sandbox import *
except ImportError:
    pass

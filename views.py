#from flask import /var/www/pyapps/bestsellers/render_template, g, request, redirect, url_for, flash, abort
from flask import render_template, g, request, redirect, url_for, flash, abort
from flask_user import login_required, UserManager, roles_required
from flask_login import current_user

from bestsellers import app, process, db
from bestsellers.models import User, Assignments, Answers, Book, Setting, Supplement, Role

@app.route('/', methods = ['GET','POST'])
def index():
    template_data = {}

    return render_template('index.html', **template_data)


@app.route('/decade/<int:decade>', methods = ['GET'])
def decade(decade):
    valid_decades = (1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990)

    if decade not in valid_decades:
        return redirect(url_for('index'))
    
    d = process.get_decade(decade)
    y = d.keys()
    return render_template('decade.html', decade = d, years = sorted(y))
    
@app.route('/diagnostics/', methods = ['GET','POST'])
@login_required
@roles_required('Administrator')
def diagnostics():
    template_data = {}

    links = []
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
#    template_data['rules'] = [r for r in app.url_map.iter_rules()]
#    template_data['rules2'] = [(r.endpoint, url_for(r.endpoint)) for r in app.url_map.iter_rules()]
    template_data['rules'] = links
    template_data['dev_server'] = app.config.get('DEV_SERVER')
    template_data['db_uri'] = app.config.get('SQLALCHEMY_DATABASE_URI')
    
    try:
        result = db.engine.execute('SHOW TABLES;')
        db_can_connect = True
    except:
        db_can_connect = False
    
    if db_can_connect:
        tables = []
        for t in result:
            tables.append(t[0])
        
        template_data['tables'] = tables
    template_data['db_can_connect'] = db_can_connect
    
    return render_template('diagnostics.html', **template_data)

@app.route('/submissions/', methods= ['GET','POST'])
def submissions():
    users = [u for u in User.query.join(Book, User.book).order_by(Book.author).all() if u.book]
    
    return render_template('browse.html', users=users)

@app.route('/students/', methods= ['GET','POST'])
@login_required
def students():
    user = User.query.get(g.user_id)
    assignments = Assignments.query.all()

    if request.method=="POST":
        if request.values.get('anon') == 'anon':
            user.anonymous = True
        else:
            user.anonymous = False
        db.session.add(user)
        db.session.commit()
    
    if not user.book and not request.values.get('redirect') == 'false':
        return redirect(url_for('select_bestseller'))
    return render_template('portal.html', user=user, assignments=assignments)
    
@app.route('/submissions/<int:user_id>', methods= ['GET','POST'])
def view_submission(user_id):
    u = User.query.get(user_id)
    
    if request.values.get('remove') == 'remove':
        title = u.book.title
        if process.remove_book(u):
            flash('Removed '+title+' entry.','bg-info')
            return redirect(url_for('submissions'))
        else:
            flash('Failed to remove '+u.book.title+' entry.','')

    if not u.book:
        flash('User has not yet selected a book.','bg-warning')
        return redirect(url_for('submissions'))
    sub = process.get_submission(u)
    supplements = Supplement.query.filter_by(user=u).order_by(Supplement.order.desc()).all()
    
    return render_template('view_submission.html', researcher=u, sub=sub, supplements=supplements)

@app.route('/assignment/<int:assign_id>/', methods= ['GET','POST'])
@login_required
def assignment(assign_id):
    assignment = Assignments.query.get(assign_id)
    user = User.query.get(g.user_id)
    
    if request.method=="POST":
        process.process_submission(user, request)
    answers = {}
    for q in assignment.questions:
        a = Answers.query.filter_by(question_id=q.id, user_id=user.id).first()
        if a:
            answers[q.id] = a.text
    
    return render_template('assignment.html', assignment=assignment, researcher=user, answers=answers)

@app.route('/supplement/', methods= ['GET','POST'])
@login_required
def supplements():
    user = User.query.get(g.user_id)
    researcher = User.query.get(g.user_id)
    if request.method=="POST":
        process.process_supplements(user, request)
    
    supplements = Supplement.query.filter_by(user=researcher).order_by(Supplement.id).all()
    
    return render_template('supplements.html',researcher=researcher, supplements=supplements)

@app.route('/supplement/<int:supplement_id>', methods= ['GET','POST'])
@login_required
def edit_supplement(supplement_id):
    user = User.query.get(g.user_id)
    supplement = Supplement.query.get(supplement_id)
    researcher = supplement.user
    
    if user != researcher and not Role.query.filter_by(name='Administrator').first() in user.roles:
        # If they are not an admin, or the supplement owner, bump them
        flash("You are not the owner of the requested supplement.","warn")
        return redirect(url_for('index'))
    
    if request.method=="POST":
        if process.edit_supplement(user, supplement, request):
            flash('Supplement has been updated.','bg-success')
            return redirect(url_for('supplements'))
            
    return render_template('edit_supplement.html', researcher=researcher, supplement=supplement)

    
@app.route('/admin/edit/<int:user_id>/<int:assign_id>/', methods= ['GET','POST'])
@login_required
@roles_required('Administrator')
def admin_edit(user_id, assign_id):
    assignment = Assignments.query.get(assign_id)
    user = User.query.get(user_id)
    
    if request.method=="POST":
        process.process_submission(user, request)
    answers = {}
    for q in assignment.questions:
        a = Answers.query.filter_by(question_id=q.id, user_id=user.id).first()
        if a:
            answers[q.id] = a.text
    return render_template('assignment.html', assignment=assignment, researcher=user, answers=answers)

@app.route('/students/selectbestseller/', methods = ['GET','POST'])
@login_required
def select_bestseller():
    user = User.query.get(g.user_id)

    if request.method=="POST" and not user.book:
        process.select_bestseller(user, request)

    # Don't let a user select a book if they already have one selected.
    if user.book:
        return redirect(url_for('students'))

    books = Book.query.filter_by(taken_by=None).all()
    return render_template('selectbestseller.html', user=user, books=books)

@app.errorhandler(404)
def page_not_found(e):
    # If they go to a URL that doesn't exist, by default we just bounce them to the index page
    # You can replace this with an actual view function if you want to do somethin else with a 404
    return redirect(url_for('index'))


@app.route('/admin/')
@login_required
@roles_required('Administrator')
def admin():
    user = User.query.get(g.user_id)
    return render_template('admin.html', user=user, users=User.query.all(), settings=Setting.query.all())

@app.route('/submissions/search')
def search():
    text = request.args.get('text')

    # We're returning a list of users because the answers that we're searching through are tied to the user
    users = process.search(text)
    
    return render_template('search.html', users=users, text=text)

@app.route('/help/<page>/')
def help(page):
    try:
        return render_template('help/{0}.html'.format(page))
    except:
        abort(404)
    
@app.route('/ajax/<method>')
def ajax(method):
    #view to handle various ajax requests
    if method == "update_setting":
        name = request.args.get('name')
        value = request.args.get('value')
        
        msg = process.update_setting(name, value)
        
    elif method == "update_user":
        username = request.args.get('username')
        email = request.args.get('email')
        anon = request.args.get('anon') == 'true'

        msg = process.update_user(username, email, anon)
        
    return render_template('ajax.json', msg = msg)

@app.route('/<string:page_name>/')
def render_static(page_name):
    return render_template('%s' % page_name)


#Testing resend confirmation email
#@app.route('/user/resend-confirm-email')
#@login_required
#def resend_email_confirmation():
#    try:
#        send_confirmation_email(current_user.email)
#        flash('Email sent to confirm your email address.  Please check your email!', 'success')
#    except IntegrityError:
#        flash('Error!  Unable to send email to confirm your email address.', 'error')
#
#    return redirect(url_for('users.login'))


@app.before_request
def set_user():
    if current_user.is_authenticated and not current_user.is_anonymous:
        g.user = current_user.username
        g.user_id = current_user.id
        g.roles = [r.name for r in User.query.get(g.user_id).roles]
    else:
        g.user = None
        g.user_id = None
        g.roles = None
        
    # If this is running via the DEV_SERVER (etc/runserver.py) use SANDBOX_USER from config_sandbox
    # because the flask development server isn't behind Shibboleth -- that's Apache only.
    if app.config.get('DEV_SERVER') == True:
        g.user = app.config.get('SANDBOX_USER')
    # Don't return anything from an @app.before_request

@app.before_request
def get_settings():
    settings = Setting.query.all()
    g.settings = {s.name: s.value for s in settings}

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

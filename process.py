# You can put stuff in here just like perl Process files, to keep the heavy computation stuff out of views.
from bestsellers import app, db
from bestsellers.models import Book, YearList, User, Assignments, Questions, Answers, Setting, Supplement

from flask import flash

from sqlalchemy.sql.expression import and_

import os, time

def get_decade(decade):
    '''Given a decade (1900,1910,...,1990) build and return a dictionary with key year, and key book type (F/N)'''
    #yearlist = YearList.query.join(Book).filter(and_(YearList.year >= decade, YearList.year < decade+10), Book.type == "F").order_by(YearList.year.asc()).all()
    yearlist = YearList.query.join(Book).filter(and_(YearList.year >= decade, YearList.year < decade+10), Book.type == "F").order_by(YearList.year.asc()).order_by(Book.type.desc()).order_by(YearList.rank).all()
    decade = {}
    for i in yearlist:
        if i.year not in decade:
           decade[i.year] = {}
        if i.book.type not in decade[i.year]:
           decade[i.year][i.book.type] = []
        decade[i.year][i.book.type].append(i)
    return decade

def get_submission(user):
    '''Given a user object,build and return a list of their submitted assignments, along with questions and answers'''
    submission = []
    assignments = Assignments.query.order_by(Assignments.order).all()
    for assignment in assignments:
        assign = {'name': assignment.name, 'order': assignment.order, 'id': assignment.id}
        questions = []
        for q in assignment.questions:
            answer = Answers.query.filter_by(user=user).filter_by(question=q).first()
            if answer:
                answer_text = answer.text.replace('\n\n','<br />')
                questions.append({'id':q.id, 'text':q.text, 'type':q.type, 'order':q.order, 'answer':answer_text})
            else:
                questions.append({'id':q.id, 'text':q.text, 'type':q.type, 'order':q.order, 'answer':''})
        assign['questions'] = questions
        submission.append(assign)
    return submission


def process_submission(user, request):
    '''Method for processing an assignment submission'''
    form = request.form
    assignment = Assignments.query.get(form.get('assignment_id'))

    print(dir(request.files))
    for q in assignment.questions:
        # Get exsting answer or create new
        answer = Answers.query.filter_by(question_id=q.id, user_id=user.id).first()
        if not answer:
            answer = Answers(question_id=q.id, user_id=user.id)
        
        if q.type == 'text':
            response = form.get('question_{0}'.format(q.id))

            # Don't save empty responses
            if response and len(response) > 0:
                answer.text = response
            else:
                continue
            
        else:
            file = request.files['question_{0}'.format(q.id)]
            if file and allowed_file(file.filename):
                ext = file.filename.rsplit('.', 1)[1]
                # Standardize filename
                filename = 'A{0}Q{1}_{2}_{3}.{4}'.format(assignment.id, q.id, user.id, int(time.time()), ext)
                old_filepath=''
                if answer.text:
                    old_filepath = os.path.join(app.config['UPLOAD_FOLDER'], answer.text)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                
                # Replace old files
                if os.path.isfile(old_filepath):
                    os.remove(old_filepath)
                
                file.save(filepath)
                answer.text = filename
            elif file and not allowed_file(file.filename):
                flash(file.filename + ' is of an unsupported type!', 'warn')
                flash('Supported types are: {0}'.format(", ".join(app.config.get('ALLOWED_EXTENSIONS'))), 'warn')
            else:
                continue
        
        db.session.add(answer)
        db.session.commit()


def process_supplements(user, request):
    '''Method for processing supplemental text/image submissions'''
    form = request.form
    if form.get('action') == 'add_new_image':
        #print 'INFO: adding a new image!'
        # Adding a new image
        file = request.files['supplement_new_image']
        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1]
            filename = 'S{0}_{1}.{2}'.format(user.id, int(time.time()), ext)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            sup = Supplement(user_id = user.id)
            
            file.save(filepath)
            sup.type = 'image'
            sup.data = filename
            sup.description = form.get('supplement_description')
            
            db.session.add(sup)
            db.session.commit()
            
        elif file and not allowed_file(file.filename):
            flash(file.filename + ' is of an unsupported type!', 'warn')
            flash('Supported types are: {0}'.format(", ".join(app.config.get('ALLOWED_EXTENSIONS'))), 'warn')
            return False
        
    elif form.get('action') == 'add_new_text':
        # Adding new text
        text = form.get('supplement_new_text')
        
        sup = Supplement(user_id = user.id)
        sup.type = 'text'
        sup.data = text
        sup.description = form.get('supplement_description')
        
        # Don't save empty responses
        if text and len(text) > 0:
            print("INFO: text is good!")
            db.session.add(sup)
            db.session.commit()
        else:
            flash("Text can't be empty.", "warn")
            return False

    elif form.get('action') == 'edit_supplement':
        # Editting existing supplement
        sup = Supplement.query.get(form.get("supplement_id"))
        if sup.user != user:
            flash("You do not own this supplement.","warn")
            return False
            
        if form.get('update_supplement'):
            pass
        elif form.get('delete_supplement'):
            db.session.delete(sup)
            db.session.commit()
    else:
        print("ERROR: This shouldn't happen, but the action was: ",form.get('action'))
    return True

def edit_supplement(user, sup, request):
    form = request.form
    if form.get('delete_supplement'):
        db.session.delete(sup)
        db.session.commit()
        return True
    sup.description = form.get('supplement_description')
    if sup.type == 'image':
        file = request.files['supplement_image']
        if file:
            if not allowed_file(file.filename):
                flash(file.filename + ' is of an unsupported type!', 'warn')
                flash('Supported types are: {0}'.format(", ".join(app.config.get('ALLOWED_EXTENSIONS'))), 'warn')
                return False
            ext = file.filename.rsplit('.', 1)[1]
            filename = 'S{0}_{1}.{2}'.format(user.id, int(time.time()), ext)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            file.save(filepath)
            sup.data = filename
    else:
        sup.data = form.get('supplement_text')
    db.session.add(sup)
    db.session.commit()
    return True
    
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in app.config.get('ALLOWED_EXTENSIONS')

def select_bestseller(user, request):
    '''Method for allowing a user to select a book'''
    form = request.form
    book = Book.query.get(form.get('book_id'))
    
    user.book = book
    book.taken_by = user.id

    db.session.add(user)
    db.session.add(book)
    db.session.commit()

def remove_book(user):
    # Delete a user's submissions and release the book to be claimed again

    # Clear book taken flag
    user.book.taken_by = None
    
    # Clear user's answers
    answers = Answers.query.filter_by(user=user).all()
    for a in answers:
        db.session.delete(a)
    
    db.session.add(user.book)
    db.session.commit()
    
    return True
    
def update_setting(name, value):
    '''Method for updating Settings objects by administrators'''
    #print "updating",name," with val ",value
    setting = Setting.query.get(name)
    setting.value = value
    db.session.add(setting)
    db.session.commit()
    
    return "success"

def update_user(username, email, anon):
    '''Method for updating a users email or anonymous status by administrators'''
    #print "fake updating ",username," with email ",email," and anon=",anon,"=>",bool(anon)
    user = User.query.filter_by(username=username).first()
    #print "found ",user.email
    user.email = email
    user.anonymous = anon
    db.session.add(user)
    db.session.commit()
    
    return "success"
    
def search(text):
    '''Return list of users whose submitted answers include the supplied text'''
    # Use regexp to search for whole words only, aka match 'test' but not 'greatest'
    answers = Answers.query.filter(Answers.text.op('regexp')(r'([[[:blank:][:punct:]]|^)'+text+'([[:blank:][:punct:]]|$)')).all()
    return set([a.user for a in answers])

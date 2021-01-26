from . import db
from flask import render_template , Blueprint , url_for , redirect , session , request , flash
from flask_login import login_required , current_user
from datetime import datetime
from .models import User , Assignment
# from flask_sqlalchemy import desc


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template("index.html")


@main.route('/about')
def about():
    return render_template("about.html")




@main.route('/profile')
@login_required
def profile():
    # n_assignments = 
    user = User.query.filter_by(email = current_user.email).first()
    assignments = Assignment.query.filter_by(author = user).all()
    false = 0
    for assignment in assignments:
        if assignment.completion == False:
            false+=1
    print(false)
    values = {"Total Assignments : ": len(assignments),
              "Completed Assignments : ":(len(assignments) - false),
              "Pending Assignments : ": false  
    }



    return render_template("profile.html" , name = current_user.name , values = values)




@main.route('/create_assignment')
@login_required
def new_assignment():
    return render_template("create_assignment.html" , date = datetime.now())







@main.route('/assignment' , methods = ['GET' , 'POST'])
@login_required
def new_assignment_post():

    assignment = request.form.get('assignment')
    comment = request.form.get('comment')
    date_posted = datetime.strptime(request.form.get('date_posted') , '%Y-%m-%d')

    due_date = datetime.strptime(request.form.get('due_date') , '%Y-%m-%d')

    completion = True if request.form.get('completion') else False



    work = Assignment(assignment = assignment , comment = comment , date_posted = date_posted , due_date = due_date , completion = completion, author = current_user)
    db.session.add(work)
    db.session.commit() 
    
    flash("New Assignment has been added")

    return redirect(url_for("main.user_assignment"))






@main.route('/assignments')
@login_required
def user_assignment():

    page = request.args.get('page' , 1 , type = int)
    user = User.query.filter_by(email = current_user.email).first_or_404()
    
    assignments = Assignment.query.filter_by(author = user).order_by(Assignment.id.desc()).paginate(page = page , per_page = 9) ## This is an object ... print(dir(assignments)) to list all the methods associated with it 
    # session['user'] = user
    # session['assignments'] = assignments
    return render_template('all_assignments.html' , user = user , assignments = assignments)






@main.route('/assignments/<int:assignment_id>/update' , methods = ['GET' , 'POST'])
@login_required
def update_assignment(assignment_id):

    assignment = Assignment.query.get_or_404(assignment_id)

    if request.method == 'POST':
        assignment.assignment = request.form.get('assignment')
        assignment.date_posted = datetime.strptime(request.form.get('date_posted') , '%Y-%m-%d')
        assignment.due_date = datetime.strptime(request.form.get('due_date') , '%Y-%m-%d')
        assignment.comment = request.form.get('comment')
        assignment.completion = True if request.form.get('completion') else False
        db.session.commit()
        flash("Assignment Updated")
        return redirect(url_for('main.user_assignment'))

    return render_template('update.html' , assignment = assignment , date = datetime.now())




@main.route('/assignments/<int:assignment_id>' , methods = ['GET' , 'POST'])
@login_required
def delete(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    db.session.delete(assignment)
    db.session.commit()
    flash("Assignment deleted")
    return redirect(url_for('main.user_assignment'))

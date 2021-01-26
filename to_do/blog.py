from flask import render_template , url_for , Blueprint

blog = Blueprint('blog' , __name__ )


@blog.route('/view')
def view():
    return render_template('blogs.html')


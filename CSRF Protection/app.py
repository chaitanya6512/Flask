from flask import Flask, request, render_template, flash
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

# Required for CSRF Protection
app.secret_key = 'your_secret_key'

# Enable CSRF Protection
csrf = CSRFProtect(app)

# Creating a FlaskForm to manage CSRF Properly
class NameForm(FlaskForm):
    name = StringField('Name', validatiors=[DataRequired()])
    submit = SubmitField('Submit')

@app.route("/", methods=["GET","POST"])
def index():
    form = NameForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            name = form.name.data
            flash(f'Hello {name} from Protected Form!', 'success')
            return render_template('index.html', form=form)
        else:
            flash('CSRF Token Missing or Invalid!', 'danger')
    return render_template('index.html', form=form)


@app.route("/unprotected_form", methods=['POST'])
def unprotected_form():
    name = request.form.get('Name',' ').strip()
    if not name:
        return "Error: Name is required!", 400
    return f'Hello {name} from Unprotected Form!'

if __name__ == '__main__':
    app.run(debug=True)
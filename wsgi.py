import os
import secrets
from flask import (
    flash,
    Flask,
    request,
    render_template
)
from flask_wtf import FlaskForm
from wtforms.validators import Email, DataRequired
from wtforms import (
    EmailField,
    StringField,
    TextAreaField,
    SubmitField,
    DateField
)

class MailTo(FlaskForm):
    timestamp = DateField('Future time', validators=[DataRequired()])
    email = EmailField('Email', validators=[Email(), DataRequired()])
    subject = StringField('Mail subject', validators=[DataRequired()])
    body = TextAreaField('Mail body', validators=[DataRequired()])
    submit = SubmitField('Send mail')

app = Flask(__name__)

# configuration
app.config['SECRET_KEY'] = secrets.token_hex(16).upper()
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = MailTo()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            subject = form.subject.data
            body = form.body.data
            # todo: schedule mail
            flash("Mail sent!")
    return render_template('index.html', form=form)

if __name__ == '__main__':
    dl_folder = app.config['UPLOAD_FOLDER']
    if not os.path.exists(dl_folder):
        os.mkdir(dl_folder)
    app.run(debug=True, port=8000)


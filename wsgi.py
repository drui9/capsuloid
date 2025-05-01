import os
import secrets
from flask import (
    flash,
    Flask,
    request,
    render_template
)
from flask_wtf import FlaskForm
from flask_mail import Mail, Message
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

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'ngaira14nelson@gmail.com'
app.config['MAIL_PASSWORD'] = 'tqie qfqn gfgq drpn '
app.config['MAIL_DEFAULT_SENDER'] = 'ngaira14nelson@gmail.com'

# configuration
app.config['SECRET_KEY'] = secrets.token_hex(16).upper()
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')

# configuration
mail = Mail(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = MailTo()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            subject = form.subject.data
            body = form.body.data
            # todo: schedule mail
            msg = Message(
              subject,
              recipients=[email],
              body=body
            )
            mail.send(msg)
            flash("Mail sent!")
    return render_template('index.html', form=form)

if __name__ == '__main__':
    dl_folder = app.config['UPLOAD_FOLDER']
    if not os.path.exists(dl_folder):
        os.mkdir(dl_folder)
    app.run(debug=True, port=8000)


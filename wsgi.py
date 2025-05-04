import os
from flask import (
    flash,
    Flask,
    request,
    render_template,
    render_template_string
)
from loguru import logger
from datetime import datetime
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
from flask_sqlalchemy import SQLAlchemy

class MailTo(FlaskForm):
    timestamp = DateField('Future time', validators=[DataRequired()])
    email = EmailField('Email', validators=[Email(), DataRequired()])
    subject = StringField('Mail subject', validators=[DataRequired()])
    body = TextAreaField('Mail body', validators=[DataRequired()])
    submit = SubmitField('Send mail')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI','sqlite:///:memory:')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'ngaira14nelson@gmail.com'
app.config['MAIL_PASSWORD'] = 'tqieqfqngfgqdrpn'
app.config['MAIL_DEFAULT_SENDER'] = 'ngaira14nelson@gmail.com'

# configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY','s3cret1ve')
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')

# configuration
mail = Mail(app)
db = SQLAlchemy(app)
# ------------------
template_str = '''
<h1> {{ title }} </h1>

<p>{{ body }} </p>
'''
# ***
autofill_tpl = '''
'''
# <>---------------
class Model:
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            print('Exception', e)
            db.session.rollback()
        return False
#</>
class EmailModel(Model, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    due_date = db.Column(db.DateTime, default=datetime.now)
    email_addr = db.Column(db.String(256), nullable=False)
    subject = db.Column(db.String(256), nullable=False)
    body = db.Column(db.String(1024), nullable=False)
    done = db.Column(db.Boolean, default=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = MailTo()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = EmailModel()
            email.email_addr = form.email.data
            email.subject = form.subject.data
            email.body = form.body.data
            email.due_date = form.timestamp.data
            if email.due_date < datetime.date(datetime.now()):
                logger.warning('Invalid mail time!')
                email.due_date = datetime.date(datetime.now())
            message = "Mail scheduled."
            if not email.save():
                message = "Mail scheduling failed!"
            flash(message)
            logger.debug(message)
    return render_template('index.html', form=form)

@app.route('/list')
def list_mails():
    if api_key := request.headers.get('Api-key'):
        if api_key == app.config['SECRET_KEY']:
            mails = EmailModel.query.filter_by(done=False).all()
            return {
                'ok': True,
                'scheduled': [
                    {i.id: i.due_date.timestamp()} for i in mails
                ]
            }
    return {'ok': False}, 401

@app.route('/send')
def send_email():
    if api_key := request.headers.get('Api-key'):
        if api_key == app.config['SECRET_KEY']:
            mail_id = request.args.get('id')
            if (email := EmailModel.query.get(mail_id)) and (not email.done):
                msg = Message(
                    email.subject,
                    recipients=[email.email_addr],
                    html=render_template_string(template_str, title=email.subject, body=email.body)
                )
                mail.send(msg)
                email.done = True
                email.save()
                return {'ok': True}
    return {'ok': False}

with app.app_context():
    db.create_all()


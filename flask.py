from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class UserForm(FlaskForm):
    first_name = StringField('Informe o seu nome', validators=[DataRequired()])
    last_name = StringField('Informe o seu sobrenome', validators=[DataRequired()])
    institution = StringField('Informe a sua instituição de ensino', validators=[DataRequired()])
    subject = SelectField('Informe a sua disciplina',
        choices=[('DSWA5','DSWA5'),('DWBA4','DWBA4'),('Gestão de projetos','Gestão de projetos')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Enviar')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MY_S3CR37_K3Y'

bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/', methods=['GET','POST'])
def index():
    form = UserForm()
    if form.validate_on_submit():
        session['name'] = f"{form.first_name.data} {form.last_name.data}"
        session['institution'] = form.institution.data
        session['subject'] = form.subject.data
        flash('Dados salvos com sucesso!', 'success')
        return redirect(url_for('index'))

    return render_template(
        'index.html',
        form=form,
        name=session.get('name'),
        institution=session.get('institution'),
        subject=session.get('subject'),
        remote_ip=request.remote_addr,
        application_host=request.host,
        current_time=datetime.utcnow()
    )

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()


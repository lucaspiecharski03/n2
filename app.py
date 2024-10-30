from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# Usuário de exemplo
class User(UserMixin):
    def __init__(self, id):
        self.id = id


# Usuários e senhas fictícias (em um projeto real, use um banco de dados)
users = {'admin': {'password': '1234'}}


@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Usuário ou senha incorretos.', 'danger')

    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)

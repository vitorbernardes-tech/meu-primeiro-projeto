from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os # Adicione isso lá no topo do arquivo junto com os outros imports


app = Flask(__name__)


# Troque a linha do sqlite por esta:
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///meubanco.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


# 1. Criando a "Tabela" do Banco de Dados
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)


# Comando para criar o banco de dados caso ele não exista
with app.app_context():
    db.create_all()


# 2. Rota principal (Homepage)
@app.route('/')
def index():
    # Puxa todos os usuários do banco para mostrar na tela, se quiser
    usuarios_salvos = Usuario.query.all()
    return render_template('homepage.html', usuarios=usuarios_salvos)


# 3. Rota para receber os dados do formulário
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome_digitado = request.form.get('nome')
    email_digitado = request.form.get('email')

    # Cria um novo registro no banco
    novo_usuario = Usuario(nome=nome_digitado, email=email_digitado)

    # Salva no banco de dados (substituindo o antigo .txt)
    db.session.add(novo_usuario)
    db.session.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)

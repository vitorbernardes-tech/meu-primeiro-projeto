# About my first project on GitHub
Estou criando um sistema de cadastro de novos usuários
from flask import Flask, request, render_template_string

app = Flask(__name__)

# --- LAYOUTS (HTML) ---
PAGINA_PRINCIPAL = '''
    <h2>Sistema de Cadastro</h2>
    <form method="POST" action="/confirmar">
        <input type="text" name="nome" placeholder="Nome" required> <br><br>
        <input type="email" name="email" placeholder="E-mail" required> <br><br>
        <button type="submit">Cadastrar e Salvar</button>
    </form>
    <br>
    <a href="/lista">Ver quem já se cadastrou</a>
'''

# --- ROTAS (LÓGICA) ---

@app.route('/')
def inicial():
    return render_template_string(PAGINA_PRINCIPAL)

@app.route('/confirmar', methods=['POST'])
def confirmar():
    nome = request.form.get('nome')
    email = request.form.get('email')

    # Salva os dados no arquivo TXT
    with open("cadastros.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(f"Nome: {nome} | E-mail: {email}\n")

    return f"<h1>Sucesso!</h1><p>{nome} foi salvo.</p><a href='/'>Voltar</a>"

@app.route('/lista')
def lista():
    try:
        with open("cadastros.txt", "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()
        
        resultado = "<h2>Lista de Cadastrados</h2><ul>"
        for linha in linhas:
            resultado += f"<li>{linha}</li>"
        resultado += "</ul><br><a href='/'>Voltar</a>"
        return resultado
    except FileNotFoundError:
        return "<h1>Ninguém cadastrado ainda.</h1><a href='/'>Voltar</a>"

# --- INICIALIZAÇÃO ---
if __name__ == '__main__':
    # Usando a porta 5001 que funcionou para você
    app.run(debug=True, port=5001)

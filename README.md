# Importamos o 'render_template' em vez do antigo 'render_template_string'
from flask import Flask, request, render_template

app = Flask(__name__)

# --- ROTAS (LÓGICA) ---

@app.route('/')
def inicial():
    # Agora o Flask vai AUTOMATICAMENTE dentro da pasta 'templates' procurar o arquivo
    return render_template('homepage.html')


@app.route('/confirmar', methods=['POST'])
def confirmar():
    nome = request.form.get('nome')
    sobrenome = request.form.get('sobrenome')
    idade_texto = request.form.get('idade')
    local = request.form.get('local')
    email = request.form.get('email')
    senha = request.form.get('senha')
    confirmacao = request.form.get('confirmacao')

    idade = int(idade_texto)

    # 1º Teste: Verifica a idade
    if idade < 18 or idade > 120:
        return f"<h1>Erro!</h1><p>Você precisa ter entre 18 e 120 anos para se cadastrar.</p><a href='/'>Voltar</a>"

    # 2º Teste: Verifica se a senha tem pelo menos 8 caracteres
    elif len(senha) < 8:
        return f"<h1>Erro!</h1><p>Sua senha é muito curta. Ela precisa ter no mínimo 8 caracteres.</p><a href='/'>Voltar</a>"

    # 3º Teste: Verifica se a senha e a confirmação são iguais
    elif senha != confirmacao:
        return f"<h1>Erro!</h1><p>As senhas não conferem. Volte e tente novamente.</p><a href='/'>Voltar</a>"

    # 4º Passo: Se passou em todos os testes acima, salva os dados!
    else:
        with open("cadastros.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(
                f"Nome: {nome} {sobrenome} | Idade: {idade} | Local: {local} | E-mail: {email} | Senha: {senha}\n")

        return f"<h1>Sucesso!</h1><p>{nome} {sobrenome} foi salvo com sucesso.</p><a href='/'>Voltar</a>"

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

if __name__ == '__main__':
    app.run(debug=True, port=5001)

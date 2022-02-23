from flask import Flask, render_template, request, redirect, session, flash, url_for

# Padrão Flask para execurção, o __name__ indica que é o arquivo atual.
app = Flask(__name__)

# para poder mandar informações entre requests e mostrar as mensagens com a
# função FLASH é necessário defirni uma secret key que nada mais é qualquer palavra
# que será usada para criptografar as informações que transitam entre requests
app.secret_key = "atilio"


# Criando uma classe usuário para apenas quem tiver cadastro fazer o login
class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha


# Criando usuarios para login e senha
user_1 = Usuario('atiliog', 'Atilio', '123321')
user_2 = Usuario('mixto', 'Thiago', 'rje10')
user_3 = Usuario('cris', 'Cristiano', 'jaera')

# minha chave é a id do usuário, e o valor é o próprio objeto usuário
usuarios = {user_1.id: user_1, user_2.id: user_2, user_3.id: user_3}


# Criando uma classe para os jogos
class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console


# Criando os objetos jogo, no lugar de lista
# lista = ['Tetris', 'Super Mario', 'Pokemon']
jogo1 = Jogo('Super Mario', 'Ação', 'Snes')
jogo2 = Jogo('Zelda', 'Ação', 'Nintendo 64')
jogo3 = Jogo('MGS', 'Ação', 'PS1')
lista = [jogo1, jogo2, jogo3]


# Aqui se indica o caminho, se deixar só o '/' ele vai direto para o
# http://127.0.0.1:5000/ e colocando '/inicio' ele vai para o
# http://127.0.0.1:5000/inicio
@app.route('/')
def index():

    # Retorna olá na página
    # return '<h1>Olá</h1>'
    #
    # Retorna a pagina lista.html com a variável titulo
    return render_template('lista.html', titulo = 'JOGOS', jogos = lista)


# esta rota LEVA para o http://127.0.0.1:5000/novo que é a página de incluir
# um jogo
@app.route('/novo')
def novo():

    # o usuario entra na pagina e segue para o login, no login ele preenche os
    # dados e a página envia o request para autenticar, se a autenticação falha
    # ou foi feito o logout então temos:
    if 'usuario_logado' not in session or session['usuario_logado'] is None:

        # redirecionando para a página login, porém inicialmente queriamos ir para '/novo'
        # return redirect('/login')
        #
        # porem queremos que a pagina de login guarde a informação de onde estávamos
        # querendo ir, que era '/novo', para guardar essa informação usaremos o
        # query string (pois não é uma informação secreta)
        # return redirect('/login?proxima=novo')
        #
        # Usando o url_for e passando apenas o nome da função e na sequencia
        # passando a variável que vai transitar entre requests
        return redirect(url_for('login', proxima = url_for('novo')))

    # caso passe no login e tenha um usuario logado faz:
    return render_template('novo.html', titulo = 'Novo Jogo')


# esta rota TRÁS para o http://127.0.0.1:5000/criar a partir do local "novo.html"
# na linha <form action="/criar" method="post">, neste caso quando o caminho
# "/novo" é executado ele envia dados via POST para a função "criar"
@app.route('/criar', methods=['POST', ])
def criar():

    # Aqui vamos pegar a informação enviada (via request) as informações vindas
    # no form, neste caso o form tem
    # <input type="text" id="nome" name="nome" class="form-control"> onde podemos
    # pegar o nome usando o dicionario vindo e a chave "nome"
    nome = request.form['nome']
    # agora para a categoria
    categoria = request.form['categoria']
    # agora para o console
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)

    # Renderiza o template de lista mas não rediceciona para o
    # http://127.0.0.1:5000/ apenas renderiza a página lista.html e fica no
    # http://127.0.0.1:5000/criar, nas próximas linhas vamos corrigir isso e
    # fazer, ao incluir um jogo, redirecionar para o http://127.0.0.1:5000/
    # return render_template('lista.html', titulo="JOGOS", jogos=lista)
    #
    # Usando o url_for
    # return redirect('/')
    return redirect(url_for('index'))


@app.route('/login')
def login():

    # pegando a informação passada via query string
    proxima = request.args.get('proxima')

    # passando a informação próxima adiante
    return render_template('login.html', proxima=proxima)


# Ao entrar na pagina de login e fazer o login a action do login.html retorna
# as informações dia método POST para a função autenticar que está na rota
# "/autenticar" e esta coleta a informação de login e senha e verifica, caso
# caso positivo redireciona para tela inicial "/" caso negativo redireciona para
# "/login"
@app.route('/autenticar', methods=['POST', ])
def autenticar():

    # ######################### TRECHO PARA MULTIPLOS USUARIOS ################
    # Verificando se o usuário está dentro da lista de objetos usuarios cadastrados
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + " logado com sucesso.")
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)

    # ######################## TRECHO PARA 1 UNICO USUARIO ####################
    # # busca e verifica se a senha do usuário é igual a "mestra" recuperando o
    # # valor na variável name="usuario" em
    # # <p><label>Senha:</label> <input class="form-control" type="password" name="senha" required></p>
    # if request.form['senha'] == "mestra":

    #     # o session permite passar informações entre requisições, uma vez que as
    #     # requisições são statless (não guardam informações entre requisições)
    #     # o session é um dicionário que guarda chave e valor e passa entre as
    #     # requisições, neste caso session['usuario_logado'] = request.form['usuario']
    #     # que está em "/login" na variável name="usuario" em
    #     # <p><label>Nome de usuário:</label> <input class="form-control" type="text" name="usuario" required></p>
    #     session['usuario_logado'] = request.form['usuario']

    #     # A função flash mostra uma mensagem rápida que será usada para informar
    #     # o estado do login, se feito ou não.
    #     flash(request.form['usuario'] + " logado com sucesso.")

    #     # aqui vamos recuperar a informação passada adiante sobre qual é a próxima
    #     # página vinda da rota '/novo'
    #     proxima_pagina = request.form['proxima']

    #     # usando o url_for e só passar direto o proxima_pagina neste caso
    #     # return redirect('/{}'.format(proxima_pagina))
    #     return redirect(proxima_pagina)
    ###########################################################################
    else:
        flash("Login não efetuado.")
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash("Nenhum usuario logado.")
    return redirect(url_for('index'))


# Aqui fazemos o start da aplicação, e o debug=True restart a aplicação quando
# se fizer um refresh
app.run(debug=True)

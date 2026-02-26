from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from datetime import datetime
import secrets

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

app.config['MAIL_SERVER'] = 'smtp.seu_email.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'seu_email@dominio.com'
app.config['MAIL_PASSWORD'] = 'sua_senha'
mail = Mail(app)

DB_NAME = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def criar_banco():
    if not os.path.exists(DB_NAME):
        conn = get_db_connection()
        conn.execute("""
            CREATE TABLE usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                reset_token TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                nome TEXT NOT NULL,
                email TEXT,
                telefone TEXT,
                observacoes TEXT,
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
            )
        """)
        conn.execute("""
            CREATE TABLE agendamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                cliente_id INTEGER,
                titulo TEXT NOT NULL,
                data TEXT NOT NULL,
                hora TEXT NOT NULL,
                descricao TEXT,
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
                FOREIGN KEY(cliente_id) REFERENCES clientes(id)
            )
        """)
        conn.commit()
        conn.close()
        print("Banco e tabelas criados com sucesso!")
    else:
        conn = get_db_connection()
        c = conn.cursor()
        try:
            c.execute("ALTER TABLE clientes ADD COLUMN observacoes TEXT")
            conn.commit()
            print("Coluna 'observacoes' adicionada com sucesso!")
        except sqlite3.OperationalError:
            pass
        conn.close()

criar_banco()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM usuarios WHERE email = ?", (email,)).fetchone()
        conn.close()
        if user and check_password_hash(user['senha'], senha):
            session['user_id'] = user['id']
            session['user_nome'] = user['nome']
            return redirect(url_for('index'))
        else:
            flash('E-mail ou senha incorretos.', 'danger')
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = generate_password_hash(request.form['senha'])
        conn = get_db_connection()
        conn.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha))
        conn.commit()
        conn.close()
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('login'))
    return render_template('registro.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', user_nome=session.get('user_nome'))


@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        observacoes = request.form.get('observacoes')
        conn.execute(
            "INSERT INTO clientes (usuario_id, nome, email, telefone, observacoes) VALUES (?, ?, ?, ?, ?)",
            (session['user_id'], nome, email, telefone, observacoes)
        )
        conn.commit()
    clientes_list = conn.execute(
        "SELECT * FROM clientes WHERE usuario_id = ?",
        (session['user_id'],)
    ).fetchall()
    conn.close()
    return render_template('clientes.html', clientes=clientes_list)

@app.route('/editar_cliente/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    cliente = conn.execute(
        "SELECT * FROM clientes WHERE id = ? AND usuario_id = ?",
        (id, session['user_id'])
    ).fetchone()
    if not cliente:
        conn.close()
        flash('Cliente não encontrado.', 'danger')
        return redirect(url_for('clientes'))
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        observacoes = request.form.get('observacoes', '')
        conn.execute(
            "UPDATE clientes SET nome = ?, email = ?, telefone = ?, observacoes = ? WHERE id = ?",
            (nome, email, telefone, observacoes, id)
        )
        conn.commit()
        conn.close()
        flash('Cliente atualizado com sucesso!', 'success')
        return redirect(url_for('clientes'))
    conn.close()
    return render_template('editar_cliente.html', cliente=cliente)

@app.route('/deletar_cliente/<int:id>')
def deletar_cliente(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    conn.execute(
        "DELETE FROM clientes WHERE id = ? AND usuario_id = ?",
        (id, session['user_id'])
    )
    conn.commit()
    conn.close()
    flash('Cliente deletado com sucesso!', 'success')
    return redirect(url_for('clientes'))


@app.route('/agendar', methods=['GET', 'POST'])
def agendar():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    clientes_list = conn.execute("SELECT * FROM clientes WHERE usuario_id = ?", (session['user_id'],)).fetchall()
    conn.close()
    if request.method == 'POST':
        cliente_id = request.form.get('cliente_id')
        titulo = request.form.get('titulo')
        data = request.form.get('data')
        hora = request.form.get('hora')
        descricao = request.form.get('descricao')
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO agendamentos (usuario_id, cliente_id, titulo, data, hora, descricao) VALUES (?, ?, ?, ?, ?, ?)",
            (session['user_id'], cliente_id, titulo, data, hora, descricao)
        )
        conn.commit()
        conn.close()
        flash('Agendamento adicionado com sucesso!', 'success')
        return redirect(url_for('lista_agendamentos'))
    return render_template('agendar.html', clientes=clientes_list)

@app.route('/lista_agendamentos')
def lista_agendamentos():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    agendamentos = conn.execute(
        "SELECT a.*, c.nome AS cliente_nome FROM agendamentos a LEFT JOIN clientes c ON a.cliente_id = c.id WHERE a.usuario_id = ? ORDER BY a.data, a.hora",
        (session['user_id'],)
    ).fetchall()
    conn.close()
    return render_template('lista_agendamentos.html', agendamentos=agendamentos)

@app.route('/editar_agendamento/<int:id>', methods=['GET', 'POST'])
def editar_agendamento(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    agendamento = conn.execute(
        "SELECT * FROM agendamentos WHERE id = ? AND usuario_id = ?",
        (id, session['user_id'])
    ).fetchone()
    clientes_list = conn.execute("SELECT * FROM clientes WHERE usuario_id = ?", (session['user_id'],)).fetchall()
    if not agendamento:
        conn.close()
        flash('Agendamento não encontrado.', 'danger')
        return redirect(url_for('lista_agendamentos'))
    if request.method == 'POST':
        titulo = request.form['titulo']
        data = request.form['data']
        hora = request.form['hora']
        descricao = request.form['descricao']
        cliente_id = request.form['cliente_id']
        conn.execute(
            "UPDATE agendamentos SET titulo = ?, data = ?, hora = ?, descricao = ?, cliente_id = ? WHERE id = ?",
            (titulo, data, hora, descricao, cliente_id, id)
        )
        conn.commit()
        conn.close()
        flash('Agendamento atualizado com sucesso!', 'success')
        return redirect(url_for('lista_agendamentos'))
    conn.close()
    return render_template('editar_agendamento.html', agendamento=agendamento, clientes=clientes_list)

@app.route('/deletar_agendamento/<int:id>')
def deletar_agendamento(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    conn.execute(
        "DELETE FROM agendamentos WHERE id = ? AND usuario_id = ?",
        (id, session['user_id'])
    )
    conn.commit()
    conn.close()
    flash('Agendamento deletado com sucesso!', 'success')
    return redirect(url_for('lista_agendamentos'))

@app.route('/get_events')
def get_events():
    if 'user_id' not in session:
        return jsonify([])
    conn = get_db_connection()
    events = conn.execute(
        "SELECT id, titulo AS title, data || 'T' || hora AS start FROM agendamentos WHERE usuario_id = ?",
        (session['user_id'],)
    ).fetchall()
    conn.close()
    eventos = [{"id": e["id"], "title": e["title"], "start": e["start"], "allDay": False} for e in events]
    return jsonify(eventos)


@app.route('/suporte', methods=['GET', 'POST'])
def suporte():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        assunto = request.form['assunto']
        mensagem = request.form['mensagem']
        msg = Message(subject=f"Suporte: {assunto}",
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[app.config['MAIL_USERNAME']],
                      body=f"Nome: {nome}\nEmail: {email}\nMensagem: {mensagem}")
        mail.send(msg)
        flash('Solicitação enviada com sucesso!', 'success')
        return redirect(url_for('suporte'))
    return render_template('suporte.html')

@app.route('/treinamento')
def treinamento():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('treinamento.html')



@app.route('/buscar')
def buscar():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    termo = request.args.get('q', '').strip().lower()
    if not termo:
        return redirect(url_for('index'))

    conn = get_db_connection()
    clientes_result = conn.execute(
        "SELECT * FROM clientes WHERE usuario_id = ? AND LOWER(nome) LIKE ?",
        (session['user_id'], f"%{termo}%")
    ).fetchall()
    agendamentos_result = conn.execute(
        """SELECT a.*, c.nome AS cliente_nome
           FROM agendamentos a
           LEFT JOIN clientes c ON a.cliente_id = c.id
           WHERE a.usuario_id = ? AND 
           (LOWER(a.titulo) LIKE ? OR LOWER(a.descricao) LIKE ?)""",
        (session['user_id'], f"%{termo}%", f"%{termo}%")
    ).fetchall()
    conn.close()

    if any(k in termo for k in ['agendamento', 'agendamentos', 'novo agendamento']):
        return redirect(url_for('agendar'))
    elif 'suporte' in termo:
        return redirect(url_for('suporte'))
    elif 'treinamento' in termo:
        return redirect(url_for('treinamento'))
    elif any(k in termo for k in ['cliente', 'clientes']):
        return redirect(url_for('clientes'))

    return render_template('buscar.html', termo=termo, clientes=clientes_result, agendamentos=agendamentos_result)


@app.route('/redefinir_senha', methods=['GET', 'POST'])
def redefinir_senha():
    if request.method == 'POST':
        email = request.form['email']
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM usuarios WHERE email = ?", (email,)).fetchone()
        if user:
            token = secrets.token_urlsafe(16)
            conn.execute("UPDATE usuarios SET reset_token = ? WHERE id = ?", (token, user['id']))
            conn.commit()
            msg = Message(subject="Redefinir Senha",
                          sender=app.config['MAIL_USERNAME'],
                          recipients=[email],
                          body=f"Acesse o link para redefinir sua senha: {request.url_root}redefinir_senha/{token}")
            mail.send(msg)
            flash('E-mail enviado com instruções!', 'success')
        else:
            flash('E-mail não encontrado.', 'danger')
        conn.close()
    return render_template('redefinir_senha.html')

@app.route('/redefinir_senha/<token>', methods=['GET', 'POST'])
def redefinir_senha_token(token):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM usuarios WHERE reset_token = ?", (token,)).fetchone()
    if not user:
        flash('Token inválido ou expirado.', 'danger')
        return redirect(url_for('login'))
    if request.method == 'POST':
        nova_senha = generate_password_hash(request.form['senha'])
        conn.execute("UPDATE usuarios SET senha = ?, reset_token = NULL WHERE id = ?", (nova_senha, user['id']))
        conn.commit()
        conn.close()
        flash('Senha redefinida com sucesso!', 'success')
        return redirect(url_for('login'))
    conn.close()
    return render_template('redefinir_senha_token.html', token=token)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

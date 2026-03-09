import datetime

from flask_bcrypt import generate_password_hash, check_password_hash
import threading
import smtplib
from email.mime.text import MIMEText
import jwt #pip install pyjwt
import datetime
from main import app

senha_secreta = app.config['SECRET_KEY']

def gerar_token(id_usuario):
    payload = {
        'id_usuario': id_usuario,
        'timestamp': datetime.datetime.utcnow().isoformat()
    }

    token = jwt.encode(payload, senha_secreta, algorithm='HS256')

    return token

def remover_bearer(token):
    if token.startswith('Bearer '):
        return token[len('Bearer '):]
    else:
        return token

def valida_senha(senha):
    qtdCaracteres = False
    maiuscula = False
    caracterePcd = False
    numero = False
    minuscula = False

    if len(senha) >= 8:
        qtdCaracteres = True

    for c in senha:
        if c.isupper():
            maiuscula = True
        elif c.islower():
            minuscula = True
        elif c.isdigit():
            numero = True
        elif not c.isalnum():
            caracterePcd = True

    if qtdCaracteres and maiuscula and caracterePcd and numero and minuscula:
        senha_criptografada = generate_password_hash(senha).decode('utf-8')
        return senha_criptografada
    else:
        return False

def enviando_email(destinatario, assunto, mensagem):
    user = "rafaelmelin50@gmail.com"
    senha = "axap frrt riir zklo"
    msg = MIMEText(mensagem)
    msg['Subject'] = assunto
    msg['From'] = user
    msg['To'] = destinatario

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(user, senha)
    server.send_message(msg)
    server.quit()
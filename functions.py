from flask_bcrypt import generate_password_hash, check_password_hash
import threading
import smtplib
from email.mime.text import MIMEText

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
    user = "laisrscurso@gmail.com"
    senha = "fkvh zoyg pujv zpdp"
    msg = MIMEText(mensagem)
    msg['Subject'] = assunto
    msg['From'] = user
    msg['To'] = destinatario

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(user, senha)
    server.send_message(msg)
    server.quit()
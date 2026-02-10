from flask_bcrypt import generate_password_hash, check_password_hash

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
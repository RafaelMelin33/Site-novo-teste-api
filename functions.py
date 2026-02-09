import bcrypt

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
        elif c.isdown():
            minuscula = True
        elif c.isdigit():
            numero = True
        elif not c.isalnum():
            caracterePcd = True

    if qtdCaracteres and maiuscula and caracterePcd and numero:
        #return alguma coisa, ou um json para retornar quais faltam
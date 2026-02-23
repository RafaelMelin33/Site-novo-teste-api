from flask import Flask, jsonify, request, send_file
from main import app, con
import fpdf
from flask_bcrypt import generate_password_hash, check_password_hash

from functions import *

@app.route('/listar_livro', methods=['GET'])
def listar_livro():
    try:
        cur = con.cursor()
        cur.execute('SELECT ID_LIVRO, TITULO, AUTOR, ANO_PUBLICACAO FROM LIVROS')
        livros = cur.fetchall()
        livros_lista = []
        for livro in livros:
            livros_lista.append({
                'id_livro': livro[0],
                'titulo': livro[1],
                'autor': livro[2],
                'ano_publicacao': livro[3]
            })
        return jsonify(mensagem = 'Lista de livros', livros = livros_lista)
    except Exception as e:
        return jsonify({'message': 'Erro ao consultar o banco de dados'}), 500
    finally:
        cur.close()

@app.route('/criar_livro', methods=['POST'])
def criar_livro():
    try:
        data = request.get_json()
        titulo = data.get('titulo')
        autor = data.get('autor')
        ano_publicacao = data.get('ano_publicacao')
        cur = con.cursor()
        cur.execute('SELECT 1 FROM LIVROS WHERE TITULO = ?', (titulo,))
        if cur.fetchone():
            return jsonify({'error': 'Livro já cadastrado'}), 400
        else:
            cur.execute("""INSERT INTO LIVROS (TITULO, AUTOR, ANO_PUBLICACAO)
                        VALUES (?, ?, ?)""", (titulo, autor, ano_publicacao))
            con.commit()
        return jsonify({
            'message': 'Livro criado com sucesso',
            'livro': {
            'titulo': titulo,
            'autor': autor,
            'ano_publicacao': ano_publicacao
            }
        }), 201
    except Exception as e:

        return jsonify({'message': 'Erro ao criar o livro'}), 500
    finally:
        cur.close()

@app.route('/deletar_livro/<int:id_livro>', methods=['DELETE'])
def deletar_livro(id_livro):
    try:
        cur = con.cursor()
        cur.execute('SELECT 1 FROM LIVROS WHERE ID_LIVRO = ?', (id_livro,))
        if cur.fetchone():
            cur.execute('DELETE FROM LIVROS WHERE ID_LIVRO = ?', (id_livro,))
            con.commit()
        else:
            return jsonify({'error': 'Livro não encontrado'}), 404
        return jsonify({'message': 'Livro deletado com sucesso'}), 200
    except Exception as e:
        return jsonify({'message': 'Erro ao deletar o livro'}), 500
    finally:
        cur.close()

@app.route('/editar_livro/<int:id_livro>', methods=['PUT'])
def editar_livro(id_livro):
    try:
        data = request.get_json()
        titulo = data.get('titulo')
        autor = data.get('autor')
        ano_publicacao = data.get('ano_publicacao')
        cur = con.cursor()
        cur.execute('SELECT 1 FROM LIVROS WHERE ID_LIVRO = ?', (id_livro,))
        if cur.fetchone():
            cur.execute("""UPDATE LIVROS SET TITULO = ?, AUTOR = ?, ANO_PUBLICACAO = ?
                        WHERE ID_LIVRO = ?""", (titulo, autor, ano_publicacao, id_livro))
            con.commit()
        else:
            return jsonify({'error': 'Livro não encontrado'}), 404
        return jsonify({
            'message': 'Livro atualizado com sucesso',
            'livro': {
            'id_livro': id_livro,
            'titulo': titulo,
            'autor': autor,
            'ano_publicacao': ano_publicacao
            }
        }), 200
    except Exception as e:
        return jsonify({'message': 'Erro ao atualizar o livro'}), 500
    finally:
        cur.close()

@app.route('/cadastro', methods=['POST'])
def cadastro():
    try:
        data = request.get_json()
        nome = data.get('nome')
        email = data.get('email')
        senha = data.get('senha')

        senha_valida = valida_senha(senha)

        if senha_valida == False:
            return jsonify({'error': 'Senha inválida. A senha deve conter pelo menos 8 caracteres, incluindo letras maiúsculas, minúsculas, números e caracteres especiais.'}), 400
        else:
            senha_criptografada = senha_valida
            cur = con.cursor()
            cur.execute('SELECT 1 FROM USUARIOS WHERE EMAIL = ?', (email,))
            if cur.fetchone():
                return jsonify({'error': 'Email já cadastrado'}), 400
            else:
                cur.execute("""INSERT INTO USUARIOS (NOME, EMAIL, SENHA, TENTATIVAS)
                            VALUES (?, ?, ?, 0)""", (nome, email, senha_criptografada))
                con.commit()
            return jsonify({
                'message': 'Usuário cadastrado com sucesso',
                'usuario': {
                'nome': nome,
                'email': email
                }
            }), 201
        return jsonify({'message': 'Usuario deletado com sucesso'}), 200
    except Exception as e:
        return jsonify({'message': 'Erro ao cadastrar'}), 500
    finally:
        cur.close()

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        senha = data.get('senha')

        cur = con.cursor()

        cur.execute('SELECT 1 FROM USUARIOS WHERE EMAIL = ?', (email,))
        if cur.fetchone():
            cur.execute('SELECT SENHA FROM USUARIOS WHERE EMAIL = ?', (email,))
            senha_armazenada = cur.fetchone()[0]
            if check_password_hash(senha_armazenada, senha):
                return jsonify({'message': 'Login bem-sucedido'}), 200
            else:
                cur.execute('SELECT TENTATIVAS FROM USUARIOS WHERE EMAIL = ?', (email,))
                tentativas = cur.fetchone()[0]
                print(tentativas)
                if tentativas == 3:
                    return jsonify({'message': 'Sua conta está inativada'})
                tentativas += 1
                cur.execute('UPDATE USUARIOS SET TENTATIVAS = ? WHERE EMAIL = ?', (tentativas, email))
                con.commit()
                return jsonify({'error': 'Senha ou email incorreto(s)'}), 401
        else:
            return jsonify({'error': 'Usuário não encontrado'}), 404
    except Exception as e:
        return jsonify({'message': 'Erro ao realizar o login'}), 500
    finally:
        cur.close()

@app.route('/editar_usuario/<int:id_usuario>', methods=['PUT'])
def editar_usuario(id_usuario):
    try:
        data = request.get_json()
        nome = data.get('nome')
        email = data.get('email')
        senha = data.get('senha')

        senha_valida = valida_senha(senha)

        if senha_valida == False:
            return jsonify({'error': 'Senha inválida. A senha deve conter pelo menos 8 caracteres, incluindo letras maiúsculas, minúsculas, números e caracteres especiais.'}), 400
        else:
            senha_criptografada = senha_valida
            cur = con.cursor()
            cur.execute('SELECT 1 FROM USUARIOS WHERE ID_USUARIO = ?', (id_usuario,))
            if cur.fetchone():
                cur.execute("""UPDATE USUARIOS SET NOME = ?, EMAIL = ?, SENHA = ?
                            WHERE ID_USUARIO = ?""", (nome, email, senha_criptografada, id_usuario))
                con.commit()
            else:
                return jsonify({'error': 'Usuário não encontrado'}), 404
            return jsonify({
                'message': 'Usuário atualizado com sucesso',
                'usuario': {
                'id_usuario': id_usuario,
                'nome': nome,
                'email': email
                }
            }), 200

    except Exception as e:
        return jsonify({'message': 'Erro ao atualizar o usuário'}), 500
    finally:
        cur.close()

@app.route('/deletar_usuario/<int:id_usuario>', methods=['DELETE'])
def deletar_usuario(id_usuario):
    cur = con.cursor()
    try:
        cur.execute('SELECT 1 FROM USUARIOS WHERE ID_USUARIO = ?', (id_usuario,))
        if cur.fetchone():
            cur.execute('DELETE FROM USUARIOS WHERE ID_USUARIO = ?', (id_usuario,))
            con.commit()
            return jsonify({'message': 'Usuário deletado com sucesso'}), 200
        else:
            return jsonify({'message': 'Usuário não encontrado'}), 404
    except Exception as e:
        cur.rollback()
        return jsonify({'message': 'Erro ao deletar usuário'}), 500
    finally:
        cur.close()

@app.route('/ativar_conta/<int:id_usuario>', methods=['PUT'])
def ativar_conta(id_usuario):
    try:
        cur = con.cursor()
        cur.execute('SELECT 1 FROM USUARIOS WHERE ID_USUARIO = ?', (id_usuario,))
        if cur.fetchone():
            cur.execute('UPDATE USUARIOS SET TENTATIVAS = 0 WHERE ID_USUARIO = ?', (id_usuario,))
            con.commit()
            return jsonify({'message': 'Tentativas resetadas com sucesso'}), 200
        else:
            return jsonify({'message': 'Usuário não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': 'Erro ao resetar tentativas'}), 500
    finally:
        cur.close()

@app.route('/gerar_pdf', methods=['GET'])
def gerar_pdf():
    try:
        pdf = fpdf.FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=15, style='B')
        pdf.cell(200, 20, txt="Meus livros", ln=True)

        cur = con.cursor()
        cur.execute('SELECT TITULO, AUTOR, ANO_PUBLICACAO FROM LIVROS')
        livros = cur.fetchall()

        pdf.set_font("Arial", size=12)

        for livros in livros:
            pdf.set_font("Arial", size=12, style='B')
            pdf.cell(200, 10, txt=f"Título: {livros[0]}", ln=True)
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Autor: {livros[1]}", ln=True)
            pdf.cell(200, 10, txt=f"Ano de Publicação: {livros[2]}", ln=True)
            pdf.y += 10

        pdf.output("livro.pdf")
        
        return send_file("livro.pdf", as_attachment=True)
    except Exception as e:

        return jsonify({'message': 'Erro ao gerar o PDF'}), 500

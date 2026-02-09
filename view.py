from flask import Flask, jsonify, request
from main import app, con

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
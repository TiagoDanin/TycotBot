import sqlite3
import sys
db = 'banco.db'


def refazer(table):
	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	try:
		cursor.execute('DROP TABLE {};'.format(table))
		conn.commit()
		return 'restaurado'
	except BaseException:
		return 'erro ao refazer'


def criar_table(table):
	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	try:
		cursor.execute(
			"""CREATE TABLE IF NOT EXISTS {}(nome VARCHAR(50) NOT NULL, advs INT NOT NULL DEFAULT 0, Id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INT, alert INT DEFAULT 0);""".format(
				str(table).replace(
					'-',
					'T')))
		conn.commit()
		return 'Table {} criado'.format(str(table).replace('-', 'T'))
	except BaseException:
		return 'erro ao criar table {}'.format(table)
		exit()
	conn.close()


def alterar_table(table):
	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	try:
		cursor.execute(
			"ALTER TABLE {} RENAME TO sqlitestudio_temp_table;".format(
				str(table)))
		conn.commit()
		cursor.execute(
			"CREATE TABLE {} (nome VARCHAR (50) NOT NULL, advs INT NOT NULL DEFAULT 0, Id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INT, alert INT DEFAULT 0);".format(
				str(table)))
		conn.commit()
		cursor.execute(
			"INSERT INTO {} (nome, advs) SELECT nome, advs FROM sqlitestudio_temp_table;".format(
				str(table)))
		conn.commit()
		cursor.execute("DROP TABLE sqlitestudio_temp_table;")
		conn.commit()
		print('banco alterado com sucesso')
		conn.close()
	except BaseException:
		print('erro')


def inserir(table, nome, user_id):
	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	try:
		cursor.execute(
			"INSERT INTO {} (nome, user_id) VALUES ('{}','{}');".format(
				str(table).replace(
					'-', 'T'), str(nome), str(user_id)))
		conn.commit()
		return 'inserido'
	except BaseException:
		retorno = 'erro ao inserir'
		try:
			alterar_table(format(str(table).replace('-', 'T')))
			cursor.execute(
				"INSERT INTO {} (nome, user_id) VALUES ('{}','{}');".format(
					str(table).replace(
						'-', 'T'), str(nome), str(user_id)))
			conn.commit()
			retorno = 'Tabela alterada. Dados inseridos'
		except BaseException:
			retorno = 'não foi possível alterar tabela'
		return retorno
	conn.close()

def mostrar(table):
	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	resposta = ''
	try:
		cursor.execute('SELECT * FROM {} ORDER BY nome;'.format(table))
		for user in cursor.fetchall():
			nome = user[0]
			resposta += '\n|--{}'.format(nome)
		resposta += '\n'
		return resposta
	except BaseException:
		return 'erro ao buscar.'
	conn.close()


def delete(table, user_id):

	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	try:
		cursor.execute(
			"DELETE FROM {} WHERE user_id = {};".format(
				str(table).replace(
					'-', 'T'), user_id))
		conn.commit()
		return 'deletado'
	except BaseException:
		return 'erro ao deletar'
	conn.close()


def procurarUserNome(table, nome):

	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	try:
		cursor.execute(
			"SELECT * FROM {} WHERE nome = '{}';".format(str(table).replace('-', 'T'), nome))
		for busca in cursor.fetchall():
			user = busca[0]
			advs = busca[1]
			user_id = busca[3]
			alerta = busca[4]
		cadastro = [user, advs, user_id, alerta]
		return cadastro
	except BaseException:
		return('erro ao procurar')
	conn.close()


def procurar(table, user_id):

	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	try:
		cursor.execute(
			"SELECT * FROM {} WHERE user_id = '{}';".format(str(table).replace('-', 'T'), user_id))
		for busca in cursor.fetchall():
			user = busca[0]
			advs = busca[1]
			user_id = busca[3]
			alerta = busca[4]
		cadastro = [user, advs, user_id, alerta]
		return cadastro
	except BaseException:
		return('erro ao procurar')
	conn.close()


def alerta(table, user_id):
	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	try:
		cursor.execute(
			"UPDATE {} SET alert=1 WHERE user_id={}".format(
				str(table).replace(
					'-', 'T'), user_id))
		conn.commit()
		conn.close()
	except BaseException:
		return 'erro ao inserir alerta'


def remAlerta(table, user_id):
	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	try:
		cursor.execute(
			"UPDATE {} SET alert=0 WHERE user_id={}".format(
				str(table).replace(
					'-', 'T'), user_id))
		conn.commit()
		conn.close()
	except BaseException:
		return 'erro ao remover alerta'


def advertir(table, user_id):

	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	try:
		advs = procurar(table, user_id)[1]
		advs += 1
		cursor.execute(
			"""UPDATE {} SET advs = {} WHERE user_id = {};""".format(
				str(table).replace(
					'-', 'T'), advs, user_id))
		conn.commit()
		return 'alterado'
	except BaseException:
		return 'erro ao alterar'
	conn.close


def desadvertir(table, user_id, quantidade):

	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	try:
		advs = procurar(table, user_id)[1]
		advs -= quantidade
		cursor.execute(
			"""UPDATE {} SET advs = {} WHERE user_id = {};""".format(
				str(table).replace(
					'-', 'T'), advs, user_id))
		conn.commit()
		return 'alterado'
	except BaseException:
		return 'erro ao alterar'
	conn.close()


def tabelas():

	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	tabelas = ''
	try:
		cursor.execute('SELECT name FROM sqlite_master;')
		for tabela in cursor.fetchall():
			tabelas += '\n--' + tabela[0]
		tabelas += '\n'
		return tabelas
	except BaseException:
		return 'erro ao achar tabelas'
	conn.close()

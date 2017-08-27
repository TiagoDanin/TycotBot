import sqlite3, sys
db = 'banco.db'

def refazer(table):

	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	try:
		cursor.execute('DROP TABLE {};'.format(table))
		conn.commit()
		return 'restaurado'
	except:
		return 'erro ao refazer'

def criar_table(table):
	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	try:
		cursor.execute("""CREATE TABLE IF NOT EXISTS {}(Id INTEGER PRIMARY KEY AUTOINCREMENT, nome VARCHAR(50) NOT NULL, user_id INT, advs INT NOT NULL DEFAULT 0, alert INT DEFAULT 0);""".format(str(table).replace('-', 'T')))
		conn.commit()
		return 'Table {} criado'.format(str(table).replace('-', 'T'))
	except:
		return 'erro ao criar table {}'.format(table)
		exit()
	conn.close()


def inserir(table, nome, user_id):
	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	try:
		cursor.execute("INSERT INTO {} (nome, user_id) VALUES ('{}','{}')".format(str(table).replace('-','T'),str(nome), str(user_id)))
		conn.commit()
		return 'inserido'
	except:
		return 'erro ao inserir'
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
	except:
		return 'erro ao buscar.'
	conn.close()

def delete(table, nome):

	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	try:
		cursor.execute("DELETE FROM {} WHERE nome = '{}';".format(str(table).replace('-', 'T'), nome))
		conn.commit()
		return 'deletado'
	except:
		return 'erro ao deletar'
	conn.close()

def procurar(table, nome):

	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	try:
		cursor.execute("SELECT * FROM {} WHERE nome = '{}';".format(str(table).replace('-', 'T'), nome))
		for busca in cursor.fetchall():
			print(busca)
			user = busca[0]
			user_id = busca[1]
			advs = busca[2]
			alerta = busca[3]
		cadastro = [user, user_id, advs, alerta]
		return cadastro
	except:
		return('erro ao procurar')
	conn.close()

def alerta(table, user_id):
	conn = sqlite3.connect(db)
	cursor=conn.cursor()
	try:
		cursor.execute("UPDATE {} SET alert=1 WHERE user_id={}".format(str(table).replace('-','T'),user_id))
		conn.commit()
	except:
		return 'erro ao inserir alerta'

def advertir(table, nome):

	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	try:
		advs = procurar(table, nome)[1]
		cursor.execute("""UPDATE {table}
SET nome = '{nome}',
advs = {advs}
WHERE nome = '{nome}';
""".format(table=str(table).replace('-', 'T'), nome=nome, advs=advs+1))
		conn.commit()
		return 'alterado'
	except:
		return 'erro ao alterar'
	conn.close()

def desadvertir(table, nome, quantidade):

	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	try:
		advs = procurar(table, nome)[1]
		cursor.execute("""UPDATE {table}
SET nome = '{nome}',
advs = {advs} 
WHERE nome = '{nome}'; """.format(table=str(table).replace('-', 'T'), nome=nome, advs=advs-quantidade))
		conn.commit()
		return 'alterado'
	except:
		return 'erro ao alterar'
	conn.close()


def tabelas():

	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	tabelas = ''
	try:
		cursor.execute('SELECT name FROM sqlite_master;')
		for tabela in cursor.fetchall():
			tabelas+='\n--'+tabela[0]
		tabelas+='\n'
		return tabelas
	except:
		return 'erro ao achar tabelas'
	conn.close()


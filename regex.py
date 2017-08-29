import re  # importa regex
Exp = ['python', 'Python', 'javascript', '.js', 'react.js', '.py', 'db']  # Expressoes a serem comparadas
for i in range(len(Exp)):  # laco pra correr por tudo
	# compilando a regex e ignorando o caso (maiusculas e minusculas)
	pythonregex = re.compile('.js|.py|python|javascript', re.I)
	# se ele achar, tanto no meio, quanto no fim...
	if pythonregex.search(Exp[i]):
		print('Achou')  # printa que achou
	else:  # senao...
		print('Não achou')  # printa que nao...

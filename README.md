# TycotBot
----
[![PyPI](https://img.shields.io/badge/python-3.6-blue.svg)]()
[![license](https://img.shields.io/github/license/mashape/apistatus.svg)]()


### Introdução
Bot para funções administrativas de grupos sobre programação do Telegram.

### Como contribuir
Crie um fork do repositório e ajude nas issues propostas.

Use o plugin [EditorCofig](http://editorconfig.org/#download) no seu editor de texto preferido para fazer as modificações.

### Dependencias
```sh
$ pip3 install -r requirements.txt
```
- Arch linux:
```sh
$ sudo pacman -S postgresql
```
- Debian/Ubuntu:
```sh
$ sudo apt-get install postgresql
```

### Executando o bot
```sh
$ python3 bot.py SEU:TOKEN
```

### Lista de Comandos do Bot
- Usuário:
    - `/info`   Mostra informações do grupo e usuário.
    - `/ajuda`  Mostra a ajuda.
    - `/regras` Mostra as regras do grupo.
    - `/link`   Mostra o link do grupo.
- Admin:
    - `/start`      Adiciona o grupo ao banco de dados do tycot, só pode ser usado uma vez.
    - `/defwelcome` Define a mensagem de boas-vindas do grupo.
    - `/defmaxwarn` Define a quantidade maxima de advertencias que um usúario pode levar.
    - `/defregras`  Define as regras do grupo.
    - `/deflink`    Define o link do grupo, se o grupo for um supergrupo o link é definido automaticamente.
    - `/ban`        Bani o usúario do grupo.
    - `/warn`       Adverte o usúario.
    - `/unwarn`     Desadverte o usúario.


### Contribuidores
[![Danrley](https://s.gravatar.com/avatar/6854dd9f3f8fc5f363ef5d5f9db1da8c?s=80)](https://github.com/dansenpir)  
[Danrley](https://github.com/dansenpir)

[![Carlos](https://s.gravatar.com/avatar/b29f6fb12e1e61f1d2a46e1ec2834696?s=80)](https://github.com/chcdc)  
[Carlos](https://github.com/chcdc)

[![LaBatata101](https://avatars2.githubusercontent.com/u/20308796?s=80&v=4)](https://github.com/LaBatata101)  
[LaBatata101](https://github.com/LaBatata101)

[![Tiago Danin](https://avatars2.githubusercontent.com/u/5731176?s=80&v=4)](https://github.com/TiagoDanin)  
[Tiago Danin](https://github.com/TiagoDanin)

# PROJETO DE SISTEMAS WEB: Portfólio + Microsserviço de Notificações

Este projeto é composto por dois projetos Django que se comunicam via API (REST). Para que o sistema funcione corretamente, é necessário clonar e executar ambos os repositórios em portas diferentes.

## Links:
- **Portfólio:** https://github.com/JonasGabSI/my_web_portfolio
- **Microsserviço de Notificações:** https://github.com/JonasGabSI/microsservi-o-notifica-o

## Passo a Passo para Execução

### 1. Clonando os Repositórios
Abra o terminal na pasta onde deseja testar os projetos e clone ambos:
```bash
git clone https://github.com/JonasGabSI/my_web_portfolio
git clone https://github.com/JonasGabSI/microsservi-o-notifica-o
```

### 2. Configurando o Microsserviço (Obrigatório rodar na porta 8001)
Abra um terminal, acesse a pasta do microsserviço e execute os comandos abaixo para criar o ambiente virtual, instalar dependências e ligar o servidor:

No Windows:
```bash
cd microsservi-o-notifica-o
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8001
```

No Linux/Mac:
```bash
cd microsservi-o-notifica-o
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver 8001
```

### 3. Configurando o Portfólio (Rodar na porta 8000)
Abra um **segundo terminal**, acesse a pasta do portfólio principal e execute os comandos:

No Windows:
```bash
cd my_web_portfolio
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8000
```

No Linux/Mac:
```bash
cd my_web_portfolio
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver 8000
```

## Como Testar a Integração
Com os **dois servidores rodando simultaneamente** (um no terminal na porta 8000 e outro no terminal na porta 8001), siga os passos:

1. Acesse o admin do microsserviço em `http://127.0.0.1:8001/admin/`.
2. Verifique se a empresa cadastrada (ex.: "Portfólio UAST") possui a `API_KEY` que está configurada no `settings.py` do projeto principal.
3. Acesse o portfólio principal em `http://127.0.0.1:8000/portfolio/` ou `http://127.0.0.1:8000/`.
4. O sino de notificações fará requisições automáticas (polling) para o microsserviço a cada 5 segundos.
5. **Teste Automatizado:** Na raiz do microsserviço existe um script chamado `enviar_notificacao.py`. Abra um terceiro terminal com o ambiente ativado e rode `python enviar_notificacao.py`. O sino no navegador do portfólio acenderá sozinho demonstrando o funcionamento em tempo real da API.
___
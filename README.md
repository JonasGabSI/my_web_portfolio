# Portfólio + Microsserviço de Notificações

Sistema web composto por dois projetos Django que se comunicam via API REST. O **Portfólio** exibe informações pessoais e gerencia tarefas autenticadas via JWT. O **Microsserviço de Notificações** é um serviço independente que recebe notificações de sistemas externos e as entrega para usuários cadastrados — o portfólio consulta esse serviço a cada 5 segundos e acende um sino no navegador quando há notificações não lidas.

```
[Sistema Externo / enviar_notificacao.py]
        │  POST /api/notificacoes/criar/
        │  Header: X-Api-Key
        ▼
[Microsserviço :8001] ◄──── polling a cada 5s ────► [Portfólio :8000]
                              GET /api/notificacoes/       (sino no front)
                              Header: X-Api-Key + X-User-Id
```

---

## Pré-requisitos

- **Python 3.12+** (obrigatório — Django 6.0 não roda em versões anteriores)
- **Git**
- **pip**

Verifique sua versão antes de começar:
```bash
python --version   # ou python3 --version
```

---

## Links dos Repositórios

- **Portfólio:** https://github.com/JonasGabSI/my_web_portfolio
- **Microsserviço:** https://github.com/JonasGabSI/microsservi-o-notifica-o

---

## Passo a Passo para Execução

### 1. Clonar os repositórios

```bash
git clone https://github.com/JonasGabSI/my_web_portfolio
git clone https://github.com/JonasGabSI/microsservi-o-notifica-o
```

---

### 2. Configurar e subir o Microsserviço (porta 8001)

> ⚠️ O microsserviço **precisa estar rodando antes** de iniciar o portfólio.

**Windows:**
```bash
cd microsservi-o-notifica-o
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8001
```

**Linux/Mac:**
```bash
cd microsservi-o-notifica-o
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver 8001
```

---

### 3. Configurar e subir o Portfólio (porta 8000)

Abra um **segundo terminal**:

**Windows:**
```bash
cd my_web_portfolio
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8000
```

**Linux/Mac:**
```bash
cd my_web_portfolio
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver 8000
```

---

### 4. Integrar os dois serviços (API Key)

Com os dois servidores rodando:

1. Acesse o admin do microsserviço: `http://127.0.0.1:8001/admin/`
2. Faça login com o superusuário criado no passo 2.
3. Cadastre uma nova **Empresa** (ex.: `"Portfólio UAST"`).
4. Após salvar, copie o campo **`hash`** gerado automaticamente — essa é a `API_KEY`.
5. Cole esse valor em dois arquivos:
   - `my_web_portfolio/mysite/settings.py` → variável `NOTIFICACAO_MS_API_KEY`
   - `microsservi-o-notifica-o/enviar_notificacao.py` → variável `API_KEY`
6. Ainda no admin do microsserviço, cadastre um **Target** vinculando essa Empresa ao `user_id: 1` (ID do superusuário do portfólio).

> ℹ️ O `user_id: 1` corresponde ao primeiro superusuário criado no portfólio. Se quiser testar com outro usuário, use o ID correspondente.

---

### 5. Testar a integração

Com **ambos os servidores rodando**, abra um **terceiro terminal** com a venv do microsserviço ativada e execute:

```bash
python enviar_notificacao.py
```

Acesse `http://127.0.0.1:8000/portfolio/` no navegador (logado) e observe o sino acender em tempo real.

---

## Estrutura dos Projetos

```
my_web_portfolio/
├── core/               # App de perfil pessoal
│   └── context_processors.py  # Injeta NOTIFICACAO_MS_URL, NOTIFICACAO_MS_API_KEY e
│                               # NOTIFICACAO_USER_ID em todos os templates,
│                               # tornando-os acessíveis ao JavaScript do sino
├── mysite/
│   ├── settings.py     # NOTIFICACAO_MS_URL e NOTIFICACAO_MS_API_KEY ficam aqui
│   └── urls.py         # Inclui rotas JWT (/api/token/)
├── portfolio/          # App de exibição do portfólio
├── tarefas/            # App de gerenciamento de tarefas (CRUD via API)
└── requirements.txt

microsservi-o-notifica-o/
├── notificacoes/
│   ├── authentication.py  # Valida X-Api-Key e X-User-Id
│   ├── models.py          # Empresa, Target, Notification
│   ├── views.py           # Endpoints da API
│   └── urls.py            # Mapeamento das rotas
├── enviar_notificacao.py  # Script de teste para disparar notificações
└── requirements.txt
```

---

## Testes via API com cURL
> **Windows (Git Bash):** use `python` nos comandos abaixo. **Linux/Mac:** use `python3`. O `| python -m json.tool` é opcional — apenas formata o JSON. Se preferir, remova essa parte e o resultado aparece em linha única.


### Portfólio (porta 8000)

#### Obter token JWT
```bash
curl -s -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "sua_senha"}' | python -m json.tool
```

Salve o `access` token retornado para usar nas próximas requisições:
```bash
TOKEN="cole_o_access_token_aqui"
```

#### Renovar token
```bash
curl -s -X POST http://127.0.0.1:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "cole_o_refresh_token_aqui"}' | python -m json.tool
```

#### Consultar perfil
```bash
curl -s http://127.0.0.1:8000/api/perfil/ \
  -H "Authorization: Bearer $TOKEN" | python -m json.tool
```

#### Listar tarefas (v3 — exige autenticação e filtra por usuário logado)
```bash
curl -s http://127.0.0.1:8000/api/tarefas/v3/ \
  -H "Authorization: Bearer $TOKEN" | python -m json.tool
```

#### Criar tarefa
```bash
curl -s -X POST http://127.0.0.1:8000/api/tarefas/v3/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Tarefa de teste", "concluida": false}' | python -m json.tool
```

#### Atualizar tarefa (substitua `1` pelo ID retornado)
```bash
curl -s -X PUT http://127.0.0.1:8000/api/tarefas/v3/1/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Tarefa atualizada", "concluida": true}' | python -m json.tool
```

#### Deletar tarefa
```bash
curl -s -X DELETE http://127.0.0.1:8000/api/tarefas/v3/1/ \
  -H "Authorization: Bearer $TOKEN"
```

---

### Microsserviço de Notificações (porta 8001)

> Substitua `74fb8f2fcbeb69f5` pela API Key da Empresa cadastrada no admin.

```bash
API_KEY="74fb8f2fcbeb69f5"
```

#### Enviar uma notificação (usado por sistemas externos)
```bash
curl -s -X POST http://127.0.0.1:8001/api/notificacoes/criar/ \
  -H "X-Api-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "titulo": "Teste cURL", "mensagem": "Notificação enviada via terminal!"}' \
  | python -m json.tool
```

#### Contar notificações não lidas
```bash
curl -s http://127.0.0.1:8001/api/notificacoes/nao-lidas/ \
  -H "X-Api-Key: $API_KEY" \
  -H "X-User-Id: 1" | python -m json.tool
```

#### Listar todas as notificações
```bash
curl -s http://127.0.0.1:8001/api/notificacoes/ \
  -H "X-Api-Key: $API_KEY" \
  -H "X-User-Id: 1" | python -m json.tool
```

#### Filtrar apenas não lidas
```bash
curl -s "http://127.0.0.1:8001/api/notificacoes/?is_read=false" \
  -H "X-Api-Key: $API_KEY" \
  -H "X-User-Id: 1" | python -m json.tool
```

#### Marcar uma notificação como lida (substitua `1` pelo ID)
```bash
curl -s -X PATCH http://127.0.0.1:8001/api/notificacoes/1/lida/ \
  -H "X-Api-Key: $API_KEY" \
  -H "X-User-Id: 1" | python -m json.tool
```

#### Marcar todas as notificações como lidas
```bash
curl -s -X PATCH http://127.0.0.1:8001/api/notificacoes/marcar-todas-lidas/ \
  -H "X-Api-Key: $API_KEY" \
  -H "X-User-Id: 1" | python -m json.tool
```

---

## Teste de Isolamento entre Empresas

Este teste demonstra que o microsserviço isola completamente as notificações por empresa — uma empresa nunca consegue ler notificações de outra, mesmo que ambas apontem para o mesmo `user_id`.

### 1. Cadastrar uma segunda empresa no admin

Acesse `http://127.0.0.1:8001/admin/` e crie mais uma Empresa (ex.: `"Sistema B"`). Copie o `hash` gerado — ele será a `API_KEY_B`.

```bash
API_KEY_A="chave_da_empresa_portfolio"   # cadastrada anteriormente
API_KEY_B="chave_da_empresa_sistema_b"   # recém cadastrada
```

### 2. Enviar uma notificação para cada empresa, ambas para o user_id 1

```bash
# Notificação da Empresa A
curl -s -X POST http://127.0.0.1:8001/api/notificacoes/criar/ \
  -H "X-Api-Key: $API_KEY_A" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "titulo": "Aviso A", "mensagem": "Mensagem exclusiva da Empresa A"}' \
  | python -m json.tool

# Notificação da Empresa B
curl -s -X POST http://127.0.0.1:8001/api/notificacoes/criar/ \
  -H "X-Api-Key: $API_KEY_B" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "titulo": "Aviso B", "mensagem": "Mensagem exclusiva da Empresa B"}' \
  | python -m json.tool
```

### 3. Consultar as notificações de cada empresa separadamente

```bash
# Empresa A só vê a própria notificação
curl -s http://127.0.0.1:8001/api/notificacoes/ \
  -H "X-Api-Key: $API_KEY_A" \
  -H "X-User-Id: 1" | python -m json.tool

# Empresa B só vê a própria notificação
curl -s http://127.0.0.1:8001/api/notificacoes/ \
  -H "X-Api-Key: $API_KEY_B" \
  -H "X-User-Id: 1" | python -m json.tool
```

**Resultado esperado:** cada resposta retorna apenas 1 notificação — a da própria empresa. Mesmo apontando para o mesmo `user_id: 1`, os dados são completamente separados porque o microsserviço vincula cada notificação a um **Target** (`empresa + user_id`), não apenas ao `user_id`.

### 4. Confirmar no admin

No admin (`http://127.0.0.1:8001/admin/`), acesse **Targets** e veja que foram criados dois registros distintos para o mesmo `user_id: 1` — um para cada empresa. Em **Notificacoes**, cada notificação estará vinculada ao seu Target correspondente, sem cruzamento entre elas.

---
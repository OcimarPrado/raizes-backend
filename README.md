# Raízes do Nordeste — Backend API

Sistema de gerenciamento de rede de lanchonetes nordestina com suporte a múltiplos canais (APP, TOTEM, BALCAO, PICKUP, WEB).

Projeto acadêmico — ADS UNINTER | Prof. Me. Luciane Yanase Kanashiro

---

## Tecnologias

- Python 3.12+ / FastAPI
- PostgreSQL + SQLAlchemy + Alembic
- JWT (python-jose + passlib + bcrypt 4.0.1)
- Pydantic v2

---

## Requisitos

- Python 3.12 ou superior
- PostgreSQL 14+
- Git

---

## Instalação e execução

### 1. Clonar o repositório

```bash
git clone https://github.com/OcimarPrado/raizes-backend.git
cd raizes-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
psql -U postgres -c "CREATE USER raizes_user WITH PASSWORD 'raizes123';"
psql -U postgres -c "CREATE DATABASE raizes_db OWNER raizes_user;"
alembic upgrade head
uvicorn app.main:app --reload
Acesse a documentação interativa em: http://localhost:8000/docs
Credenciais de teste
Perfil
E-mail
Senha
Gerente
gerente@raizes.com
gerente123
Cliente
joao@email.com
cliente123
Endpoints principais
Método
Rota
Auth
Descrição
POST
/auth/login
público
Retorna JWT
POST
/usuarios/
público
Cadastro de usuário
GET
/usuarios/me
JWT
Dados do usuário logado
GET
/produtos/
público
Lista cardápio
POST
/produtos/
GERENTE
Cria produto
GET
/unidades/
público
Lista unidades ativas
GET
/estoque/unidade/{id}
GERENTE
Saldo de estoque por unidade
POST
/pedidos/
JWT
Cria pedido
GET
/pedidos/
JWT
Lista pedidos
PATCH
/pedidos/{id}/status
JWT
Atualiza status do pedido
POST
/pagamentos/
JWT
Processa pagamento (mock)
GET
/fidelidade/me
JWT
Saldo de cupons
GET
/fidelidade/me/historico
JWT
Histórico de cupons
GET
/audit-logs/
GERENTE
Logs de auditoria
Canais de pedido
APP · TOTEM · BALCAO · PICKUP · WEB
AGUARDANDO_PAGAMENTO → CONFIRMADO → PREPARANDO → PRONTO → ENTREGUE
                                                         ↘ CANCELADO
Programa de fidelidade
A cada 10 pedidos com status ENTREGUE, o cliente recebe 1 cupom de desconto.
Histórico consultável via GET /fidelidade/me/historico.
Estrutura do projeto
app/
├── api/
│   ├── dependencies/     # auth.py (JWT + require_role)
│   ├── routers/          # auth, usuario, produto, unidade, estoque, pedido,
│   │                     # pagamento, fidelidade, audit_log
│   └── exception_handlers.py
├── application/
│   ├── schemas/          # Pydantic schemas
│   ├── usuario_service.py
│   ├── pedido_service.py
│   ├── pagamento_service.py
│   └── fidelidade_service.py
├── domain/               # Modelos SQLAlchemy
├── infrastructure/
│   ├── database/         # connection.py + migrations Alembic
│   ├── repositories/
│   └── security.py
└── main.py
\q
sair
exit
\q

## 🔒 Privacidade e Conformidade LGPD

A API "Raízes do Nordeste" foi desenvolvida priorizando a segurança e a privacidade dos dados pessoais, em conformidade com os princípios da Lei Geral de Proteção de Dados (LGPD). As principais medidas implementadas incluem:

* **Minimização de Dados:** Coletamos apenas as informações estritamente necessárias para a operação dos serviços[cite: 1].
* **Autenticação Segura:** Utilizamos JSON Web Tokens (JWT) para garantir que apenas usuários autenticados acessem recursos restritos[cite: 1].
* **Segurança no Armazenamento:** As senhas dos usuários são armazenadas utilizando *hashing* com BCrypt, garantindo que não fiquem expostas em formato legível[cite: 1].
* **Rastreabilidade:** Implementamos logs de auditoria para ações sensíveis, garantindo a transparência e segurança do fluxo de dados[cite: 1].

## Interface do Usuário (Front-End)
Este projeto possui uma interface web correspondente para consumo da API.
- Repositório Front-End: https://github.com/OcimarPrado/raizes-frontend

# Library Catalog API

Sistema de gerenciamento de livros, autores, estoques e filiais, estruturado com Django, Django REST Framework e arquitetura limpa.

## Requisitos

- Python 3.10+
- pip
- virtualenv (opcional, mas recomendado)
- PostgreSQL

## Instalação

```bash
git clone https://github.com/seuusuario/seuprojeto.git
cd seuprojeto
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configuração
Copie e edite o arquivo de variáveis de ambiente:
```bash
cp .env.example .env
```
Certifique-se de configurar corretamente o banco de dados e as chaves JWT.

## Migrações e Superusuário
```bash
python manage.py migrate
python manage.py createsuperuser
```
## Executando o Projeto
```bash
python manage.py runserver
```

## Rodando os Testes
```bash
pytest
```

## Com cobertura de código:
```bash
pytest --cov --cov-report=term-missing
```

## Estrutura do Projeto
```tree
backend/
│
├── author/
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   └── interface/
│
├── book/
├── book_stock/
├── branch/
├── tests/
├── manage.py
└── requirements.txt
```

## Convenções de Testes
- Views usam APIClient com force_authenticate
- Uso de fixtures: valid_author_data, make_branch, etc.
- Separação de InputSerializer e OutputSerializer
- Arquitetura orientada a comandos e queries

## Autenticação
A API usa JWT para autenticação:

Obter token:

```bash
POST /api/token
{
"username": "admin",
"password": "admin"
}
```
Atualizar token:

```bash
POST /api/token/refresh
```

Inclua o token nos headers:

```bash
Authorization: Bearer <seu_token>
```
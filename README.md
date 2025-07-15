# Book Manager API

Sistema de gerenciamento de livros, autores, estoques e filiais, estruturado com Django, Django REST Framework e arquitetura limpa.

## Requisitos

- Python 3.10+
- PostgreSQL
- RabbitMQ
- Elasticsearch

## Instalação

```bash
git clone https://github.com/FeeFelipe/bookmanager.git
cd bookmanager
docker-compose up --build
```

## Configuração
Copie e edite o arquivo de variáveis de ambiente:
```bash
cp .env.example .env
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
POST /api/token/
{
"username": "admin",
"password": "admin123"
}
```
Atualizar token:

```bash
POST /api/token/refresh/
```

Inclua o token nos headers:

```bash
Authorization: Bearer <seu_token>
```
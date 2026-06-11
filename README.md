# API de Acervo Digital de Livros (MADR)

Projeto backend desenvolvido com FastAPI para gerenciamento de usuários, autores e livros através de uma API REST.

O projeto foi construído com foco em boas práticas de desenvolvimento backend, incluindo autenticação baseada em JWT, persistência de dados com PostgreSQL, testes automatizados e containerização com Docker.

- Acesso ao Swagger: [madrapp.fly.dev/docs](https://madrapp.fly.dev/docs)

## Objetivo

Desenvolver uma API para gerenciamento de um acervo digital de livros, permitindo operações de cadastro, consulta, atualização e remoção de usuários, autores e livros.

Além das funcionalidades de CRUD, o projeto contempla autenticação, controle de acesso e organização modular da aplicação.

## Funcionalidades

### Usuários

* Criar usuários
* Atualizar usuários
* Remover usuários

### Autenticação

* Login de usuários
* Geração de tokens JWT
* Proteção de rotas autenticadas

### Autores

* Criar autores
* Atualizar autores
* Remover autores
* Listar autores

### Livros

* Criar livros
* Atualizar livros
* Remover livros
* Listar livros

## Tecnologias

* Python 3.12
* FastAPI
* SQLAlchemy
* PostgreSQL
* Alembic
* Poetry
* Docker
* Pytest

## Arquitetura

A aplicação foi organizada de forma modular, separando responsabilidades entre rotas, modelos, esquemas, segurança e persistência de dados.

```text
madr/
├── routers/
│   ├── auth.py
│   ├── users.py
│   ├── authors.py
│   └── books.py
├── database.py
├── models.py
├── schemas.py
├── security.py
└── app.py
```

## Banco de Dados

O projeto utiliza PostgreSQL como banco de dados relacional e SQLAlchemy como ORM para modelagem e persistência das entidades.

As alterações de esquema são gerenciadas através de migrações utilizando Alembic.

## Testes

Foram implementados testes automatizados para validação dos principais fluxos da aplicação:

* Autenticação
* Usuários
* Autores
* Livros
* Camada de persistência
* Segurança

Execução dos testes:

```bash
pytest
```

Cobertura de testes:

```bash
pytest --cov=madr
```

## Execução

Clone o repositório:

```bash
git clone https://github.com/gabitrombetta/MADR.git
cd MADR
```

Execute a aplicação com Docker:

```bash
docker compose up --build
```

A documentação interativa estará disponível em:

```text
http://localhost:8000/docs
```

## Autor

Gabriela Trombetta

[LinkedIn](https://www.linkedin.com/in/gabitrombetta/) • [GitHub](https://github.com/gabitrombetta)
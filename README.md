# Expense Management

A database design exercise for a multi-user expense management system.

## Overview

This project includes a complete database structure for managing accounts, categories, merchants, transactions, split transactions, tags, budgets, recurring transactions, and attachments.

## Included

* SQLAlchemy 2 models in `src/expense_management/models`
* Alembic setup with an initial migration
* Draw.io ERD in `docs/database_schema.drawio`
* Database layout explanation in `docs/database_layout.md`

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

By default, the project uses SQLite for local testing.

## Database Migration

Apply migrations:

```bash
alembic upgrade head
```

Create a new migration after model changes:

```bash
alembic revision --autogenerate -m "describe change"
```

## Project Structure

```text
docs/
  database_schema.drawio
  database_layout.md

src/
  expense_management/
    models/
    db/
    core/

alembic/
  versions/
```

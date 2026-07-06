# Expense Management Database Layout

## Core Design

The database separates the main transaction record from its category allocations:

* `transactions` stores the main financial event: account, amount, type, merchant, date, and status.
* `transaction_splits` stores category-level allocations for each transaction.
* `transaction_tags` connects transactions to tags through a many-to-many relationship.

This supports both simple and split transactions. For example, one supermarket payment can be split into `Groceries`, `Household`, and `Personal Care`.

## Tables

| Table                    | Purpose                                                     |
| ------------------------ | ----------------------------------------------------------- |
| `users`                  | Owns all personal finance data.                             |
| `accounts`               | Stores cash, bank, card, wallet, loan, or similar accounts. |
| `categories`             | Stores hierarchical categories such as `Food > Groceries`.  |
| `merchants`              | Stores payees, stores, vendors, or income sources.          |
| `transactions`           | Stores expenses, income, transfers, and adjustments.        |
| `transaction_splits`     | Stores category allocations for transactions.               |
| `tags`                   | Stores user-defined labels such as `travel` or `business`.  |
| `transaction_tags`       | Join table between transactions and tags.                   |
| `budgets`                | Stores budget limits for a user and optional category.      |
| `recurring_transactions` | Stores templates for repeated transactions.                 |
| `attachments`            | Stores file metadata for receipts, invoices, or notes.      |

## Main Relationships

| Relationship                           | Cardinality                             |
| -------------------------------------- | --------------------------------------- |
| `users` -> `accounts`                  | One-to-many                             |
| `users` -> `categories`                | One-to-many                             |
| `categories` -> `categories`           | Self-referencing parent/child           |
| `users` -> `merchants`                 | One-to-many                             |
| `users` -> `transactions`              | One-to-many                             |
| `accounts` -> `transactions`           | One-to-many                             |
| `merchants` -> `transactions`          | One-to-many                             |
| `transactions` -> `transaction_splits` | One-to-many                             |
| `categories` -> `transaction_splits`   | One-to-many                             |
| `transactions` -> `tags`               | Many-to-many through `transaction_tags` |
| `categories` -> `budgets`              | One-to-many                             |
| `transactions` -> `attachments`        | One-to-many                             |

## Business Rules

* Each account, category, merchant, transaction, tag, budget, and recurring rule belongs to one user.
* Categories can be nested using `parent_id`.
* A transaction can be an `expense`, `income`, `transfer`, or `adjustment`.
* Transfer transactions can use both `account_id` and `transfer_account_id`.
* Transaction splits should add up to the transaction amount.
* A budget can be global when `category_id` is null, or category-specific when it is set.
* Attachments store file metadata only; actual files can be stored locally or in external storage.

## Project Files

* ERD: `docs/database_schema.drawio`
* SQLAlchemy models: `src/expense_management/models`
* Alembic environment: `alembic/env.py`
* Initial migration: `alembic/versions/e7186a76a172_create_initial_expense_management_schema.py`

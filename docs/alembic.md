# DB migrations

- Has own directory, maintained as part of proejct + has alembic.ini file

Basic workflow:

- `alembic revision -m "descriptino migartion, e.g. create column x"`
- population upgrade() and downgrade() in created file
- run `alembic upgrade head` to apply latest migration
- update models.py to match

Downgrade:

- `alembic downgrade <revision>`

Alternative:

1. Update models.py
2. `alembic revision --autogenerate`
3. `alembic upgrade head`

Other

- `alembic history`
- `alembic stamp base`
- `alembic current`

For out of sync alembic: FAILED: Target database is not up to date.

1. `alembic stamp head`
2. `alembic revision --autogenerate -m "your_migration_message"`
3. `alembic upgrade head`

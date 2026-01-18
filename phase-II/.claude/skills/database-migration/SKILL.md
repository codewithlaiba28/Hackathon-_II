---
name: database-migration
description: |
  This skill handles database schema changes and migrations for SQLModel/SQLAlchemy using Alembic or similar tools. Use this skill when you need to manage database schema evolution, create new migrations, or apply schema changes to your database.
---

# Database Migration Skill

This skill should be used when users need to handle database schema changes and migrations for SQLModel/SQLAlchemy using Alembic or similar tools.

## Skill Type: Automation

## Domain: Database Migrations with SQLModel/SQLAlchemy

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Current database models, existing schema, migration history |
| **Conversation** | User's specific migration requirements, database provider, environment constraints |
| **Skill References** | Alembic documentation, SQLModel migration patterns, SQLAlchemy best practices |
| **User Guidelines** | Project-specific conventions, deployment requirements, rollback procedures |

Ensure all required context is gathered before implementing.

## Core Concepts

Database migrations involve:
- Schema versioning and tracking
- Forward and backward compatibility
- Data preservation during schema changes
- Environment-specific configurations
- Rollback capabilities

## Migration Workflow

The migration process follows these steps:
1. Create migration files from model changes
2. Review and modify migration scripts if needed
3. Apply migrations to target database
4. Verify migration success
5. Handle any migration failures

## Implementation Steps

### 1. Setup Alembic for SQLModel

First, initialize Alembic in your project:

```bash
# Install alembic if not already installed
pip install alembic

# Initialize alembic in your project
cd backend
alembic init alembic
```

### 2. Configure Alembic for SQLModel

Update the `alembic.ini` file to work with your project structure:

```ini
[alembic]
# path to migration scripts
script_location = alembic

# template used to generate migration file names; The default value is %%(rev)s_%%(slug)s
file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(rev)s_%%(slug)s

# sys.path path, will be prepended to sys.path if present.
# defaults to the current working directory.
prepend_sys_path = .

# timezone to use when rendering the date within the migration file
# as well as the filename.
# If specified, requires the python-dateutil library that can be
# installed by adding `alembic[tz]` to the pip requirements
# string value is passed to dateutil.tz.gettz()
# leave blank for localtime
# timezone =

# max length of characters to apply to the
# "slug" field
# max_length = 40

# version_num separator; default is ``_`` (underscore)
# version_separator = _

# version path separator; default is ``os.pathsep`` (``:`` on POSIX,
# ``;`` on Windows). For a script to be detected by the ``--version-path``
# option, it must be separated by this character.
# version_path_separator = os.pathsep

# the output encoding used when revision files are written from
# script.py.mako
# output_encoding = utf-8

sqlalchemy.url = driver://user:pass@localhost/dbname
```

Update the `alembic/env.py` file to work with your SQLModel models:

```python
# alembic/env.py
import sys
import os
from pathlib import Path
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Add the project root to the path so we can import models
sys.path.insert(0, Path(__file__).parent.parent.absolute())

from models import SQLModel  # Import your SQLModel models
from db import DATABASE_URL  # Import your database URL

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = SQLModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = DATABASE_URL
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### 3. Create Initial Migration

Create the initial migration based on your current models:

```bash
# Create the initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply the migration to your database
alembic upgrade head
```

### 4. Creating New Migrations

When you modify your models, create new migrations:

```bash
# After modifying your models, create a new migration
alembic revision --autogenerate -m "Description of the changes"

# Review the generated migration file in alembic/versions/
# Make any necessary adjustments

# Apply the migration
alembic upgrade head
```

### 5. Migration Script Example

Example of what a generated migration script might look like:

```python
"""Initial migration

Revision ID: abc123def456
Revises:
Create Date: 2024-01-15 10:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
import pgvector

# revision identifiers, used by Alembic.
revision = 'abc123def456'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create tables
    op.create_table('user',
        sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    op.create_table('task',
        sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=False, default='pending'),
        sa.Column('priority', sa.String(), nullable=False, default='medium'),
        sa.Column('due_date', sa.DateTime(), nullable=True),
        sa.Column('user_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes
    op.create_index('ix_user_email', 'user', ['email'])
    op.create_index('ix_task_user_id', 'task', ['user_id'])
    op.create_index('ix_task_status', 'task', ['status'])


def downgrade():
    # Drop tables in reverse order
    op.drop_index('ix_task_status')
    op.drop_index('ix_task_user_id')
    op.drop_index('ix_user_email')

    op.drop_table('task')
    op.drop_table('user')
```

### 6. Environment-Specific Configuration

Create environment-specific migration commands:

```bash
# For development
alembic upgrade head

# For production (with caution)
alembic upgrade head --sql  # Generate SQL without executing
alembic upgrade head       # Execute the migration

# Check current migration status
alembic current

# Show migration history
alembic history --verbose
```

### 7. Rollback Procedures

Handle migration rollbacks safely:

```bash
# Rollback to the previous migration
alembic downgrade -1

# Rollback to a specific migration
alembic downgrade abc123def456

# Rollback all the way to the beginning
alembic downgrade base
```

## Best Practices

1. **Always review auto-generated migrations** before applying them
2. **Backup your database** before running migrations in production
3. **Test migrations on a copy** of production data first
4. **Use transactions** to ensure atomicity of migrations
5. **Keep data migrations separate** from schema migrations when possible
6. **Document breaking changes** in migration descriptions

## Migration Safety Checklist

- [ ] Migration script reviewed for correctness
- [ ] Backup taken before applying to production
- [ ] Migration tested on staging environment
- [ ] Rollback plan prepared
- [ ] Downtime window scheduled if required
- [ ] Team notified of migration timing
- [ ] Monitoring in place to verify success

## Common Migration Patterns

### Adding a Column
```python
def upgrade():
    op.add_column('task', sa.Column('completed_at', sa.DateTime(), nullable=True))

def downgrade():
    op.drop_column('task', 'completed_at')
```

### Adding a Non-Nullable Column
```python
def upgrade():
    # Add nullable first
    op.add_column('task', sa.Column('priority', sa.String(), nullable=True))
    # Update existing rows
    op.execute("UPDATE task SET priority = 'medium' WHERE priority IS NULL")
    # Make it non-nullable
    op.alter_column('task', 'priority', nullable=False)

def downgrade():
    op.drop_column('task', 'priority')
```

### Renaming a Column
```python
def upgrade():
    op.alter_column('task', 'old_name', new_column_name='new_name')

def downgrade():
    op.alter_column('task', 'new_name', new_column_name='old_name')
```

This skill provides a comprehensive approach to handling database migrations with SQLModel/SQLAlchemy, ensuring safe and reliable schema changes across environments.
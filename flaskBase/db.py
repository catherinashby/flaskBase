import click
from flask import cli, current_app
from playhouse.flask_utils import FlaskDB
from flaskBase.migrate import DatabaseManager

def init_app(app):
    pwdb = FlaskDB(database={
                'name': 'flaskBase.db3',
                'engine': 'playhouse.sqlite_ext.SqliteExtDatabase',
                'pragmas': (
                    ('journal_mode', 'wal'),
                    ('ignore_check_constraints', 0),
                    ('foreign_keys', 1)
                )
            }
        )
    pwdb._db['name'] = app.config['DATABASE']
    pwdb.init_app(app)
    app.pwdb = pwdb
    app.cli.add_command(migrations)

@click.group()
@click.pass_context
@cli.with_appcontext
def migrations(ctx):
    """Run database migration commands."""
    class ScriptInfo:
        def __init__(self):
            self.data = {'manager': None}

    db = current_app.pwdb.database
    if db == None:
        current_app.pwdb._db['name'] = current_app.config['DATABASE']
        current_app.pwdb.init_app(current_app)
        db = current_app.pwdb.database
    dir = current_app.config['MIGRATIONS_DIR']

    ctx.obj = ctx.obj or ScriptInfo()
    ctx.obj.data['manager'] = DatabaseManager(db, directory=dir)

@migrations.command('create')
@click.argument('model')
@click.pass_context
def migrations_create(ctx,model):
    """Create a migration based on an existing model."""
    if not ctx.obj.data['manager'].create(model):
        sys.exit(1)

@migrations.command('delete')
@click.argument('target', default='')
@click.pass_context
@cli.with_appcontext
def migration_delete(ctx,target):
    """Delete the target migration from the filesystem and database."""
    if not ctx.obj.data['manager'].delete(target):
        sys.exit(1)

@migrations.command('downgrade')
@click.argument('target', default='')
@click.pass_context
def migrations_downgrade(ctx,target):
    """Run database downgrades."""
    if not ctx.obj.data['manager'].downgrade(target):
        sys.exit(1)

@migrations.command('info')
@click.pass_context
def migrations_info(ctx):
    """Show information about the current database."""
    ctx.obj.data['manager'].info()

@migrations.command('revision')
@click.argument('name', default='NONE')
@click.pass_context
def migrations_revision(ctx, name=None):
    """
    Create a blank migration file named FILENAME.
    Defaults to 'auto_migration'.
    """
    if name == 'NONE': name = None
    if not ctx.obj.data['manager'].revision(name):
        sys.exit(1)

@migrations.command('status')
@click.pass_context
def migrations_status(ctx):
    """Show information about migration status."""
    ctx.obj.data['manager'].status()

@migrations.command('upgrade')
@click.argument('target', default='')
@click.pass_context
def migrations_upgrade(ctx,target):
    """Run database upgrades."""
    if not ctx.obj.data['manager'].upgrade(target):
        sys.exit(1)

#
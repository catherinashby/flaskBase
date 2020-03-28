import logging, os
from flaskBase import app
from playhouse.flask_utils import FlaskDB

import pdb

def test_migrate_info(tmp_path, monkeypatch, caplog):
    runner = app.test_cli_runner()
#    if app.pwdb.database:
    db = os.path.join(tmp_path, 'flaskBase.db3')
    monkeypatch.setitem(app.config,'DATABASE',db)
    monkeypatch.setitem(app.config,'MIGRATIONS_DIR', tmp_path)
    monkeypatch.setattr(app.pwdb, 'database', None)
    with caplog.at_level(logging.INFO):
        result = runner.invoke(args=['migrations','info'])
        assert caplog.messages[0] == '   Driver: SqliteExtDatabase'
        assert caplog.messages[1] == ' Database: ' + db

def test_migrate_read_write(tmp_path, monkeypatch, caplog):
    runner = app.test_cli_runner()
    ldb = FlaskDB(app=runner.app,
        database={
            'name': ':memory:',
            'engine': 'playhouse.sqlite_ext.SqliteExtDatabase'
            }
        )
    monkeypatch.setattr(runner.app, 'pwdb', ldb)
    monkeypatch.setitem(runner.app.config, 'MIGRATIONS_DIR', tmp_path)
    with caplog.at_level(logging.INFO):
        result = runner.invoke(args=['migrations','status'])
        assert caplog.messages[0] == 'no migrations found'

        result = runner.invoke(args=['migrations','revision'])
        assert caplog.messages[1] == 'created: 0001_auto_migration'

        result = runner.invoke(args=['migrations','status'])
        assert caplog.messages[2] == '[ ] 0001_auto_migration'

        result = runner.invoke(args=['migrations','delete', '0001'])
        assert caplog.messages[3] == 'deleted: 0001_auto_migration'

        result = runner.invoke(args=['migrations','status'])
        assert caplog.messages[4] == 'no migrations found'

def test_migrate_creation(tmp_path, monkeypatch):
    runner = app.test_cli_runner()
    ldb = FlaskDB(app=runner.app,
        database={
            'name': ':memory:',
            'engine': 'playhouse.sqlite_ext.SqliteExtDatabase'
            }
        )
    monkeypatch.setattr(runner.app, 'pwdb', ldb)
    monkeypatch.setitem(runner.app.config, 'MIGRATIONS_DIR', tmp_path)

    result = runner.invoke(args=['migrations','create', 'name'])
    assert result.exit_code == 1

    result = runner.invoke(args=['migrations','create', 'tests.data.models'])
    assert result.exit_code == 0

def test_migrate_down_and_up(tmp_path,monkeypatch):
    runner = app.test_cli_runner()
    ldb = FlaskDB(app=runner.app,
        database={
            'name': ':memory:',
            'engine': 'playhouse.sqlite_ext.SqliteExtDatabase'
            }
        )
    monkeypatch.setattr(runner.app, 'pwdb', ldb)
    monkeypatch.setitem(runner.app.config, 'MIGRATIONS_DIR', tmp_path)

    result = runner.invoke(args=['migrations','revision'])
    assert result.exit_code == 0

    result = runner.invoke(args=['migrations','upgrade',''])
    assert result.exit_code == 0

    result = runner.invoke(args=['migrations','downgrade',''])
    assert result.exit_code == 0

#
import peewee
from pytest import raises as assertError
from flaskBase.migrate import TableCreator, DatabaseManager, build_upgrade_from_model

from tests.data import models

class Test_TableCreator:

    def test_initialize(self):
        tc = TableCreator('dummyTable')

        assert issubclass(tc.model, peewee.Model)


    def test_column(self):
        tc = TableCreator('dummyTable')
        tc.primary_key('id')
        tc.column('bare', 'col_bare')
        tc.column('biginteger', 'col_biginteger')
        tc.column('binary', 'col_binary')
        tc.column('blob', 'col_blob')
        tc.column('bool', 'col_bool')
        tc.column('char', 'col_char')
        csp = peewee.SQL('col_date not null')
        tc.column('date', 'col_date', constraints=[csp])
        tc.column('datetime', 'col_datetime')
        tc.column('decimal', 'col_decimal')
        tc.column('double', 'col_double')
        tc.column('fixed', 'col_fixed')
        tc.column('float', 'col_float')
        tc.column('int', 'col_int')
        tc.column('integer', 'col_integer')
        tc.column('smallint', 'col_smallint')
        tc.column('smallinteger', 'col_smallinteger')
        tc.column('text', 'col_text',constraints='col_text not null')
        tc.column('time', 'col_time')
        tc.column('uuid', 'col_uuid')
        tc.column('bin_uuid', 'col_bin_uuid')

        assert isinstance(tc.model.id, peewee.AutoField)
        assert isinstance(tc.model.col_bare, peewee.BareField)
        assert isinstance(tc.model.col_biginteger, peewee.BigIntegerField)
        assert isinstance(tc.model.col_binary, peewee.BlobField)
        assert isinstance(tc.model.col_blob, peewee.BlobField)
        assert isinstance(tc.model.col_bool, peewee.BooleanField)
        assert isinstance(tc.model.col_char, peewee.CharField)
        assert isinstance(tc.model.col_date, peewee.DateField)
        assert isinstance(tc.model.col_datetime, peewee.DateTimeField)
        assert isinstance(tc.model.col_decimal, peewee.DecimalField)
        assert isinstance(tc.model.col_double, peewee.DoubleField)
        assert isinstance(tc.model.col_fixed, peewee.CharField)
        assert isinstance(tc.model.col_float, peewee.FloatField)
        assert isinstance(tc.model.col_int, peewee.IntegerField)
        assert isinstance(tc.model.col_integer, peewee.IntegerField)
        assert isinstance(tc.model.col_smallint, peewee.SmallIntegerField)
        assert isinstance(tc.model.col_smallinteger, peewee.SmallIntegerField)
        assert isinstance(tc.model.col_text, peewee.TextField)
        assert isinstance(tc.model.col_time, peewee.TimeField)
        assert isinstance(tc.model.col_uuid, peewee.UUIDField)
        assert isinstance(tc.model.col_bin_uuid, peewee.BinaryUUIDField)


    def test_column_aliases(self):
        tc = TableCreator('dummyTable')
        tc.bare('col_bare')
        tc.biginteger('col_biginteger')
        tc.binary('col_binary')
        tc.blob('col_blob')
        tc.bool('col_bool')
        tc.char('col_char')
        tc.date('col_date')
        tc.datetime('col_datetime')
        tc.decimal('col_decimal')
        tc.double('col_double')
        tc.fixed('col_fixed')
        tc.float('col_float')
        tc.int('col_int')
        tc.integer('col_integer')
        tc.smallint('col_smallint')
        tc.smallinteger('col_smallinteger')
        tc.text('col_text')
        tc.time('col_time')
        tc.uuid('col_uuid')
        tc.bin_uuid('col_bin_uuid')

        assert isinstance(tc.model.col_bare, peewee.BareField)
        assert isinstance(tc.model.col_biginteger, peewee.BigIntegerField)
        assert isinstance(tc.model.col_binary, peewee.BlobField)
        assert isinstance(tc.model.col_blob, peewee.BlobField)
        assert isinstance(tc.model.col_bool, peewee.BooleanField)
        assert isinstance(tc.model.col_char, peewee.CharField)
        assert isinstance(tc.model.col_date, peewee.DateField)
        assert isinstance(tc.model.col_datetime, peewee.DateTimeField)
        assert isinstance(tc.model.col_decimal, peewee.DecimalField)
        assert isinstance(tc.model.col_double, peewee.DoubleField)
        assert isinstance(tc.model.col_fixed, peewee.CharField)
        assert isinstance(tc.model.col_float, peewee.FloatField)
        assert isinstance(tc.model.col_int, peewee.IntegerField)
        assert isinstance(tc.model.col_integer, peewee.IntegerField)
        assert isinstance(tc.model.col_smallint, peewee.SmallIntegerField)
        assert isinstance(tc.model.col_smallinteger, peewee.SmallIntegerField)
        assert isinstance(tc.model.col_text, peewee.TextField)
        assert isinstance(tc.model.col_time, peewee.TimeField)
        assert isinstance(tc.model.col_uuid, peewee.UUIDField)
        assert isinstance(tc.model.col_bin_uuid, peewee.BinaryUUIDField)


    def test_index(self):
        tc = TableCreator('dummyTable')
        tc.column('char', 'fname')
        tc.column('char', 'lname')
        tc.add_index(('fname', 'lname'), unique=True)

        assert tc.model._meta.indexes == [(('fname', 'lname'), True)]


    def test_constraint(self):
        tc = TableCreator('dummyTable')
        tc.column('char', 'fname')

        const = peewee.SQL('fname not null')
        tc.add_constraint(const)

        assert tc.model._meta.constraints == [const]


    def test_foreign_key(self):
        tc = TableCreator('dummyTable')
        tc.foreign_key('int', 'user_id', references='user.id', on_delete='cascade', on_update='cascade')
        tc.foreign_key('int', 'part_id', references='parts')

        assert isinstance(tc.model.user_id, peewee.ForeignKeyField)
        assert isinstance(tc.model.part_id, peewee.ForeignKeyField)


    def test_foreign_key_index(self):
        tc = TableCreator('dummyTable')
        tc.foreign_key('int', 'user_id', references='user.id', on_delete='cascade', on_update='cascade')
        tc.add_index(('user_id',), False)

        assert isinstance(tc.model.user_id, peewee.ForeignKeyField)
        assert tc.model._meta.indexes == [(('user_id',), False)]


class Test_DatabaseManager:

    def test_database_creation(self, tmpdir):
        db = peewee.SqliteDatabase(':memory:')
        manager = DatabaseManager(db, directory=tmpdir)
        assert isinstance(manager.database, peewee.SqliteDatabase)

        db = {'engine': 'peewee.SqliteDatabase', 'name': ':memory:'}
        manager = DatabaseManager(db, directory=tmpdir)
        assert isinstance(manager.database, peewee.SqliteDatabase)

        db = 'sqlite:///:memory:'
        manager = DatabaseManager(db, directory=tmpdir)
        assert isinstance(manager.database, peewee.SqliteDatabase)


    def test_database_creation_error(self, tmpdir):
        db = {'name': ':memory:'}
        with assertError(peewee.DatabaseError):
            DatabaseManager(db, directory=tmpdir)

        db = {'engine': 'peewee.SqliteDatabase'}
        with assertError(peewee.DatabaseError):
            DatabaseManager(db, directory=tmpdir)

        db = {'engine': 'unknown.FakeDatabase', 'name': ':memory:'}
        with assertError(peewee.DatabaseError):
            DatabaseManager(db, directory=tmpdir)


    def test_info(self, tmpdir, caplog):
        manager = DatabaseManager('sqlite:///:memory:', directory=tmpdir)

        manager.info()
        assert 'Driver: SqliteDatabase' in caplog.text
        assert 'Database: :memory:' in caplog.text


    def test_revision(self, tmpdir, caplog):
        manager = DatabaseManager('sqlite:///:memory:', directory=tmpdir)

        assert manager.revision()
        first = manager.migration_files[0]
        assert 'created: {}'.format(first) in caplog.text

        assert manager.revision('Custom Name')
        first = manager.migration_files[1]
        assert 'created: {}'.format(first) in caplog.text


    def test_revision_error(self, tmpdir, caplog):
        manager = DatabaseManager('sqlite:///:memory:', directory=tmpdir)

        assert not manager.revision('Bad Characters: \0')
        assert 'embedded' in caplog.text


    def test_find_migration(self, tmpdir):
        manager = DatabaseManager('sqlite:///:memory:', directory=tmpdir)
        manager.revision()

        # find the first migration name
        first = manager.migration_files[0]
        first_id = first.split('_')[0]

        rv = manager.find_migration(first_id)
        assert rv == first

        rv = manager.find_migration(first)
        assert rv == first

        # with assertError(ValueError):
        #     manager.find_migration('does_not_exist')


    def test_open_migration(self, tmpdir):
        manager = DatabaseManager('sqlite:///:memory:', directory=tmpdir)
        manager.revision()
        first = manager.migration_files[0]

        with manager.open_migration(first) as handle:
            content = handle.read()

        assert content.startswith('"""\nauto migration')
        assert 'def upgrade(migrator):\n    pass' in content
        assert 'def downgrade(migrator):\n    pass' in content


    def test_status(self, tmpdir, caplog):
        manager = DatabaseManager('sqlite:///:memory:', directory=tmpdir)

        manager.status()
        assert 'no migrations found' in caplog.text

        manager.revision()
        first = manager.migration_files[0]
        assert 'created: {}'.format(first) in caplog.text

        manager.status()
        assert '[ ] {}'.format(first) in caplog.text


    def test_files_and_diff(self, tmpdir):
        manager = DatabaseManager('sqlite:///:memory:', directory=tmpdir)
        manager.revision()
        manager.revision('custom name')
        migrations = manager.migration_files

        rv = manager.db_migrations
        assert not rv

        rv = manager.migration_files
        assert rv == (migrations[0], migrations[1],)

        rv = manager.diff
        assert rv == (migrations[0], migrations[1],)


    def test_upgrade_all(self, tmpdir, caplog):
        manager = DatabaseManager('sqlite:///:memory:', directory=tmpdir)
        manager.revision()
        manager.revision()
        migrations = manager.migration_files

        manager.upgrade()
        assert 'upgrade: {}'.format(migrations[0]) in caplog.text
        assert 'upgrade: {}'.format(migrations[1]) in caplog.text

        assert manager.db_migrations == (migrations[0], migrations[1])
        assert not manager.diff

        # All migrations applied now...
        manager.upgrade()
        assert 'all migrations applied!' in caplog.text


    def test_upgrade_target(self, tmpdir, caplog):
        manager = DatabaseManager('sqlite:///:memory:', directory=tmpdir)
        manager.revision()
        manager.revision()
        migrations = manager.migration_files

        manager.upgrade(migrations[0])
        assert 'upgrade: {}'.format(migrations[0]) in caplog.text

        assert manager.db_migrations == (migrations[0],)
        assert manager.diff == (migrations[1],)


    def test_already_upgraded(self, tmpdir, caplog):
        manager = DatabaseManager('sqlite:///:memory:', directory=tmpdir)
        manager.revision()
        migrations = manager.migration_files

        manager.upgrade(migrations[0])
        assert 'upgrade: {}'.format(migrations[0]) in caplog.text

        manager.upgrade(migrations[0])
        assert 'already applied: {}'.format(migrations[0]) in caplog.text


    def test_upgrade_target_error(self, tmpdir, caplog):
        manager = DatabaseManager('sqlite:///:memory:', directory=tmpdir)
        manager.revision()

        manager.upgrade('does-not-exist')
        assert 'could not find migration: does-not-exist' in caplog.text


    def test_downgrade_nodiff(self, tmpdir, caplog):
        manager = DatabaseManager('sqlite:///:memory:', directory=tmpdir)
        manager.downgrade()
        assert 'migrations not yet applied!' in caplog.text


    def test_downgrade_single(self, tmpdir, caplog):
        manager = DatabaseManager('sqlite:///:memory:', directory=tmpdir)
        manager.revision()
        manager.revision()
        manager.upgrade()
        migrations = manager.migration_files

        assert manager.db_migrations == (migrations[0], migrations[1],)
        assert not manager.diff

        manager.downgrade()
        assert 'downgrade: {}'.format(migrations[1]) in caplog.text

        assert manager.db_migrations == (migrations[0],)
        assert manager.diff == (migrations[1],)


    def test_downgrade_target(self, tmpdir, caplog):
        manager = DatabaseManager('sqlite:///:memory:', directory=tmpdir)
        manager.revision()
        manager.revision()
        manager.upgrade()
        migrations = manager.migration_files

        assert manager.db_migrations == (migrations[0], migrations[1],)
        assert not manager.diff

        manager.downgrade('0001')
        assert 'downgrade: {}'.format(migrations[1]) in caplog.text
        assert 'downgrade: {}'.format(migrations[0]) in caplog.text

        assert not manager.db_migrations
        assert manager.diff == (migrations[0], migrations[1],)


    def test_downgrade_not_applied(self, tmpdir, caplog):
        manager = DatabaseManager('sqlite:///:memory:', directory=tmpdir)
        manager.revision()
        migrations = manager.migration_files

        manager.downgrade(migrations[0])
        assert 'not yet applied: {}'.format(migrations[0]) in caplog.text


    def test_downgrade_target_error(self, tmpdir, caplog):
        manager = DatabaseManager('sqlite:///:memory:', directory=tmpdir)
        manager.revision()

        manager.downgrade('does-not-exist')
        assert 'could not find migration: does-not-exist' in caplog.text


    def test_run_migration_not_found(self, tmpdir, caplog):
        manager = DatabaseManager('sqlite:///:memory:', directory=tmpdir)
        manager.revision()

        manager.run_migration('does-not-exist')
        assert 'could not find migration: does-not-exist' in caplog.text


    def test_run_migration_exception(self, tmpdir, caplog):
        manager = DatabaseManager('sqlite:///:memory:', directory=tmpdir)
        manager.revision()

        # Open the migration file and write lines to it that will error when we try to run it.
        with manager.open_migration('0001_auto_migration', 'w') as handle:
            handle.write('def upgrade(migrator):\n    undefined\n')

        manager.upgrade()
        assert "upgrade: 0001_auto_migration" in caplog.text
        assert "'undefined' is not defined" in caplog.text


    def test_delete(self, tmpdir, caplog):
        manager = DatabaseManager('sqlite:///:memory:', directory=tmpdir)
        manager.revision()
        manager.upgrade()
        migrations = manager.migration_files

        manager.delete(migrations[0])
        assert 'deleted: {}'.format(migrations[0]) in caplog.text

        assert not manager.db_migrations
        assert not manager.migration_files


    def test_delete_not_found(self, tmpdir, caplog):
        manager = DatabaseManager('sqlite:///:memory:', directory=tmpdir)
        manager.revision()
        manager.upgrade()

        manager.delete('does-not-exist')
        assert 'could not find migration: does-not-exist' in caplog.text


class Test_Migrator:

    def test_create_table(self,tmpdir):
        manager = DatabaseManager('sqlite:///:memory:', directory=tmpdir)

        with manager.migrator.create_table('dummyTable') as table:
            table.primary_key('id')
            table.bare('col_bare')
            table.biginteger('col_biginteger')
            table.binary('col_binary')
            table.blob('col_blob')
            table.bool('col_bool')
            table.char('col_char')
            table.date('col_date')
            table.datetime('col_datetime')
            table.decimal('col_decimal')
            table.double('col_double')
            table.fixed('col_fixed')
            table.float('col_float')
            table.int('col_int')
            table.integer('col_integer')
            table.smallint('col_smallint')
            table.smallinteger('col_smallinteger')
            table.text('col_text')
            table.time('col_time')
            table.uuid('col_uuid')
            table.bin_uuid('col_bin_uuid')
            table.add_index(('col_char', 'col_integer'), unique=True)

        assert 'dummyTable' in manager.database.get_tables()


    def test_drop_table(self,tmpdir):
        manager = DatabaseManager('sqlite:///:memory:', directory=tmpdir)

        with manager.migrator.create_table('dummyTable') as table:
            table.primary_key('id')

        manager.migrator.drop_table('dummyTable')
        assert 'dummyTable' not in manager.database.get_tables()


    def test_add_drop_column(self,tmpdir):
        manager = DatabaseManager('sqlite:///:memory:', directory=tmpdir)

        with manager.migrator.create_table('dummyTable') as table:
            table.primary_key('id')

        manager.migrator.add_column('dummyTable', 'name', 'char', null=True)
        manager.migrator.drop_column('dummyTable', 'name')


    def test_rename_column(self,tmpdir):
        manager = DatabaseManager('sqlite:///:memory:', directory=tmpdir)

        with manager.migrator.create_table('dummyTable') as table:
            table.primary_key('id')

        manager.migrator.add_column('dummyTable', 'name', 'char', null=True)
        manager.migrator.rename_column('dummyTable', 'name', 'newname')


    def test_rename_table(self,tmpdir):
        manager = DatabaseManager('sqlite:///:memory:', directory=tmpdir)

        with manager.migrator.create_table('dummyTable') as table:
            table.primary_key('id')

        manager.migrator.rename_table('dummyTable', 'anotherTable')


    def test_not_null(self,tmpdir):
        manager = DatabaseManager('sqlite:///:memory:', directory=tmpdir)

        with manager.migrator.create_table('dummyTable') as table:
            table.primary_key('id')
            table.char('name')

        manager.migrator.add_not_null('dummyTable', 'name')
        manager.migrator.drop_not_null('dummyTable', 'name')


    def test_index(self,tmpdir):
        manager = DatabaseManager('sqlite:///:memory:', directory=tmpdir)

        with manager.migrator.create_table('dummyTable') as table:
            table.primary_key('id')
            table.char('name')

        manager.migrator.add_index('dummyTable', ('name',), unique=True)
        manager.migrator.drop_index('dummyTable', 'dummyTable_name')


    def test_execute_sql(self,tmpdir):
        manager = DatabaseManager('sqlite:///:memory:', directory=tmpdir)

        with manager.migrator.create_table('dummyTable') as table:
            table.primary_key('id')
            table.char('name')

        manager.migrator.execute_sql('select * from dummyTable')


    def test_str_constraints(self,tmpdir):
        manager = DatabaseManager('sqlite:///:memory:', directory=tmpdir)

        with manager.migrator.create_table('dummyTable') as table:
            table.primary_key('id')
            table.char('username', constraints=[
                "check (username in ('tim', 'bob'))",
                peewee.Check("username in ('tim', 'bob')")
            ])


    def test_foreign_key(self,tmpdir):
        manager = DatabaseManager('sqlite:///:memory:', directory=tmpdir)

        with manager.migrator.create_table('basic') as table:
            table.primary_key('id')
            table.char('username')

        with manager.migrator.create_table('related1') as table:
            table.primary_key('id')
            table.foreign_key('int', 'basic_id', 'basic')

        with manager.migrator.create_table('related5') as table:
            table.primary_key('id')
            table.foreign_key('char', 'basic', 'basic.username')

        assert 'basic' in manager.database.get_tables()
        assert 'related1' in manager.database.get_tables()


class Test_Creation:

    def test_create_import(self, tmpdir, caplog):
        manager = DatabaseManager('sqlite:///:memory:', directory=tmpdir)
        manager.create('Person')

        assert 'could not import: Person' in caplog.text


    def test_create_error(self,tmpdir, caplog):
        manager = DatabaseManager('sqlite:///:memory:', directory=tmpdir)
        manager.create(models.NotModel)
        assert "type object 'NotModel' has no attribute '_meta'" in caplog.text


    def test_create(self, tmpdir, caplog):
        manager = DatabaseManager('sqlite:///:memory:', directory=tmpdir)
        manager.create(models.Person)
        assert 'created: 0001_create_table_person' in caplog.text


    def test_create_module(self, tmpdir, caplog):
        """Test module creations.

        peewee changed the migration creation order in:
        https://github.com/coleifer/peewee/compare/2.9.2...2.10.0

        First create models on which current model depends
        (either through foreign keys or through depends_on),
        then create current model itself.
        """
        manager = DatabaseManager(models.database, directory=tmpdir)
        manager.create(models)
        migrations = manager.migration_files

        assert len(migrations) == 8

        # basicfields has no relationship
        assert migrations[0].endswith('create_table_basicfields')
        assert 'created: {}'.format(migrations[0]) in caplog.text

        # organization has no relationships
        assert migrations[1].endswith('create_table_organization')
        assert 'created: {}'.format(migrations[1]) in caplog.text

        # since complexpersion relates to organization is then now created
        assert migrations[2].endswith('create_table_complexperson')
        assert 'created: {}'.format(migrations[2]) in caplog.text

        # HasCheckConstraint has no relationships
        assert migrations[3].endswith('create_table_hascheckconstraint')
        assert 'created: {}'.format(migrations[3]) in caplog.text

        # Person has no relationship
        assert migrations[4].endswith('create_table_person')
        assert 'created: {}'.format(migrations[4]) in caplog.text

        # HasUniqueForeignKey relates to Person
        assert migrations[5].endswith('create_table_hasuniqueforeignkey')
        assert 'created: {}'.format(migrations[5]) in caplog.text

        # ModelWithTimestamp
        assert migrations[6].endswith('create_table_modelwithtimestamp')
        assert 'created: {}'.format(migrations[6]) in caplog.text

        # RelatesToName relates to Person
        assert migrations[7].endswith('create_table_relatestoname')
        assert 'created: {}'.format(migrations[7]) in caplog.text


    def test_build_upgrade_from_model(self):
        output = build_upgrade_from_model(models.ComplexPerson)
        output = list(output)
        assert output == [
            "with migrator.create_table('complexperson') as table:",
            "    table.primary_key('id')",
            "    table.char('name', max_length=5, unique=True)",
            "    table.foreign_key('AUTO', 'organization_id', on_delete=None, on_update=None, references='organization.id')",
            "    table.add_constraint('const1 fake')",
            "    table.add_constraint('CHECK (const2 fake)')",
        ]


    def test_non_id_foreign_key_output(self):
        output = build_upgrade_from_model(models.RelatesToName)
        output = list(output)

        assert output == [
            "with migrator.create_table('relatestoname') as table:",
            "    table.primary_key('id')",
            "    table.foreign_key('VARCHAR', 'person_name', on_delete='SET NULL', on_update='CASCADE', references='person.name')"]


    def test_index_field_names(self):
        output = build_upgrade_from_model(models.HasUniqueForeignKey)
        output = list(output)

        assert output == [
            "with migrator.create_table('hasuniqueforeignkey') as table:",
            "    table.primary_key('id')",
            "    table.int('age')",
            "    table.foreign_key('VARCHAR', 'person_name', on_delete=None, on_update=None, references='person.name')",
            "    table.add_index(('age', 'person_name'), unique=True)"]


    def test_timestamp_model(self):
        output = build_upgrade_from_model(models.ModelWithTimestamp)
        output = list(output)

        assert output == [
            "with migrator.create_table('modelwithtimestamp') as table:",
            "    table.primary_key('id')",
            "    table.int('tstamp')"]

#
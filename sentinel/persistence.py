import psycopg2
import re

import config

underscore_re = re.compile('(?!^)([A-Z]+)')


def to_underscore(name):
    return underscore_re.sub(r'_\1', name).lower()


class NotFoundError(BaseException):
    pass


class Database:
    """
    A simple wrapper for a global database connection.
    """

    _instance = None

    @classmethod
    def _set_timezone(cls):
        cur = cls._instance.connection.cursor()
        cur.execute("set timezone to 'utc'")
        cur.close()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            try:
                db_name = config.default_database
                # print(f'Connecting to database {db_name}')
                conn_str = config.databases[db_name]['connection_string']
                cls._instance.connection = psycopg2.connect(**conn_str)
                cls._set_timezone()
            except Exception as error:
                print(f'Error: Database connection not established: {error}')
                Database._instance = None
            else:
                # print('Database connection established')
                pass

        return cls._instance

    def __init__(self):
        self.connection = self._instance.connection

    def __del__(self):
        self.connection.close()

    def get_connection(self):
        return self._instance.connection

    def commit(self):
        self._instance.connection.commit()

    def rollback(self):
        self._instance.connection.rollback()

    def execute(self, sql: str, params={}):
        cur = self._instance.connection.cursor()
        cur.execute(sql, params)
        cur.close()

    def mogrify(self, sql: str, params={}):
        cur = self._instance.connection.cursor()
        res = cur.mogrify(sql, params)
        cur.close()
        return res

    def fetch_one(self, sql: str, params={}):
        cur = self._instance.connection.cursor()
        cur.execute(sql, params)
        row = cur.fetchone()
        cur.close()
        if row is None:
            raise NotFoundError()
        return row

    def fetch_all(self, sql: str, params={}):
        cur = self._instance.connection.cursor()
        cur.execute(sql, params)
        rows = cur.fetchall()
        cur.close()
        if rows is None:
            raise NotFoundError()
        return rows


db = Database()


class PersistentEntity:
    def __init__(self):
        self.id = None
        self._table_name = to_underscore(type(self).__name__)
        self._sql_insert = None
        self._sql_insert_with_id = None
        self._sql_update = None
        self._sql_select = None
        self._sql_delete = None

    def _init_sql(self):
        pub = self._get_public_variables_no_id()
        self._sql_insert = self._build_insert(pub)

        pub = self._get_public_variables()
        self._sql_insert_with_id = self._build_insert(pub)

        self._sql_update = self._build_update()
        self._sql_select = self._build_select()
        self._sql_delete = self._build_delete()

    def _build_insert(self, pub):
        columns = ','.join([k for k in pub])
        values = ','.join([f'%({k})s' for k in pub])
        sql = f"""
            insert into {self._table_name}({columns})
            values({values})
            """
        if 'id' not in pub:
            sql += " returning id"
        return sql

    def _build_update(self):
        pub = self._get_public_variables_no_id()
        values = ','.join([f'{k}=%({k})s' for k in pub])
        sql = f"""
            update {self._table_name}
            set {values}
            where id = %(id)s
            """
        return sql

    def _build_select(self):
        pub = self._get_public_variables()
        columns = ','.join([k for k in pub])
        sql = f"""
            select {columns}
            from {self._table_name}
            where id = %(id)s
            """
        return sql

    def _build_delete(self):
        sql = f"""
            delete from {self._table_name}
            where id = %(id)s
            """
        return sql

    def _get_public_variables(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}

    def _get_public_variables_no_id(self):
        pub = self._get_public_variables()
        del pub['id']
        return pub

    def insert(self):
        """
        Insert using all public variables and without getting an id back
        from the database (id provided by the user).
        This should be used when the id (primary key) is not a serial.
        """
        pub = self._get_public_variables()
        # print(db.mogrify(self._sql_insert_with_id, pub))
        db.execute(self._sql_insert_with_id, pub)

    def save(self):
        if self.id is not None:
            pub = self._get_public_variables()
            # print(db.mogrify(self._sql_update, pub))
            db.execute(self._sql_update, pub)
        else:
            pub = self._get_public_variables_no_id()
            # print(cur.mogrify(self._sql_insert, pub))
            self.id = db.fetch_one(self._sql_insert, pub)[0]

    def load(self):
        # print(db.mogrify(self._sql_select, {'id': self.id}))
        row = db.fetch_one(self._sql_select, {'id': self.id})
        pub = self._get_public_variables()
        i = 0
        for key in pub:
            setattr(self, key, row[i])
            i += 1

    def delete(self):
        if self.id is not None:
            # print(db.mogrify(self._sql_delete, {'id': self.id})
            db.execute(self._sql_delete, {'id': self.id})

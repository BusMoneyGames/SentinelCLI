import psycopg2
import re

import config

underscore_re = re.compile('(?!^)([A-Z]+)')


def to_underscore(name):
    return underscore_re.sub(r'_\1', name).lower()


class Database:
    """
    A simple wrapper for a global database connection.
    """

    _database_name = 'test'
    _connection = None

    @classmethod
    def set_active_database(cls, name):
        cls._database_name = name

    @classmethod
    def get_connection(cls):
        if not cls._connection:
            cls._connection = cls._connect()
            cls._set_timezone()
        return cls._connection

    @classmethod
    def _connect(cls):
        conn_str = config.databases[cls._database_name]['connection_string']
        return psycopg2.connect(**conn_str)

    @classmethod
    def _set_timezone(cls):
        cur = cls._connection.cursor()
        cur.execute("set timezone to 'utc'")
        cur.close()


class PersistentEntity:
    def __init__(self):
        self.id = None
        self._table_name = to_underscore(type(self).__name__)
        self._sql_insert = None
        self._sql_insert_with_id = None
        self._sql_update = None
        self._sql_select = None
        self._conn = Database.get_connection()

    def _init_sql(self):
        pub = self._get_public_variables_no_id()
        self._sql_insert = self._build_insert(pub)

        pub = self._get_public_variables()
        self._sql_insert_with_id = self._build_insert(pub)

        self._sql_update = self._build_update()
        self._sql_select = self._build_select()

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
        pub = self._get_public_variables_no_id()
        columns = ','.join([k for k in pub])
        sql = f"""
            select {columns}
            from {self._table_name}
            where id = %(id)s
            """
        return sql

    def _get_public_variables(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}

    def _get_public_variables_no_id(self):
        pub = self._get_public_variables()
        del pub['id']
        return pub

    def _execute(self, sql: str, params: tuple):
        cur = self._conn.cursor()
        cur.execute(sql, params)
        cur.close()

    def _fetch_one(self, sql: str, params: tuple):
        cur = self._conn.cursor()
        cur.execute(sql, params)
        row = cur.fetchone()
        if row:
            value = row[0]
        else:
            value = None
        cur.close()
        return value

    def insert(self):
        """
        Insert using all public variables and without getting an id back
        from the database (id provided by the user).
        """
        cur = self._conn.cursor()
        pub = self._get_public_variables()
        # print(cur.mogrify(self._sql_insert_with_id, pub))
        cur.execute(self._sql_insert_with_id, pub)
        cur.close()

    def save(self):
        cur = self._conn.cursor()
        if self.id:
            pub = self._get_public_variables()
            # print(cur.mogrify(self._sql_update, pub))
            cur.execute(self._sql_update, pub)
        else:
            pub = self._get_public_variables_no_id()
            # print(cur.mogrify(self._sql_insert, pub))
            cur.execute(self._sql_insert, pub)
            self.id = cur.fetchone()[0]
        cur.close()

    def load(self):
        cur = self._conn.cursor()
        # print(cur.mogrify(self._sql_select, {'id': self.id}))
        cur.execute(self._sql_select, {'id': self.id})
        row = cur.fetchone()
        pub = self._get_public_variables_no_id()
        i = 0
        for key in pub:
            setattr(self, key, row[i])
            i += 1
        cur.close()


if __name__ == '__main__':
    conn = Database.get_connection()

    class Queue(PersistentEntity):
        def __init__(self):
            super().__init__()
            self.status_id = 1
            self.name = "abc"
            self.value = 'some value'
            #self._id = 251
            self._init_sql()


    q1 = Queue()
    q1.value = 'brand new value'
    print(q1.save())
    print(q1.id)

    q2 = Queue()
    q2.id = 288
    q2.load()
    print(q2.id, q2.name, q2.status_id, q2.value)

    conn.commit()

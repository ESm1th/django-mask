from django.db import connection


class Queries:
    __slots__ = "__cursor"

    def __init__(self, cursor=None):
        if cursor is None:
            cursor = connection.cursor()
        self.__cursor = cursor

    def get_existing_values(self, db_table_name, field_names, ids):
        query = self.build_select_values_query(db_table_name, field_names, ids)
        self.__cursor.execute(query)
        raw_values = self.__cursor.fetchall()
        return raw_values[0]

    def update_db(self, db_table_name, field_names, values):
        query = self.build_update_query(db_table_name, field_names, values)
        self.__cursor.execute(query)

    @staticmethod
    def build_select_values_query(db_table_name, field_names, ids):
        """
        Возвращает sql запрос на получение данных из БД.

        Пример:
        -------
        db_table_name = "core_user"
        field_names   = ("email", "username")
        ids           = (111, 222, 333)

        SELECT *
        FROM (
            SELECT
                array_agg(email),
                array_agg(username)
            FROM core_user
            WHERE id in (111, 222, 333)
        ) AS pivot

        При использовании курсора вернет:
        ---------------------------------
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        >>> data
        [(
            ["test_x@test.test", "test_y@test.test", "test_z@test.test"],
            ["test_username_x", "test_username_y", "test_username_z"]
        )]

        >>> emails = data[0][fields.index("email")]
        >>> emails
        ["test_x@test.test", "test_y@test.test", "test_z@test.test"]

        >>> usernames = data[0][fields.index("username")]
        >>> usernames
        ["test_username_x", "test_username_y", "test_username_z"]
        """
        query = """
        SELECT *
        FROM (
            SELECT
                {aggs}
            FROM {tb}
            WHERE id in ({ids})
        ) as pivot
        """.format(
            aggs=",\n".join(["array_agg({})".format(f) for f in field_names]),
            tb=db_table_name,
            ids=",".join(ids)
        )
        return query

    @staticmethod
    def build_update_query(db_table_name, field_names, values):
        """
        Возвращает sql запрос на обновление данных в БД.

        Пример:
        -------
        db_table_name = "core_user"
        field_names   = ("email", "username")
        values        = [
                            (111, "test_x@test.test", "test_username_x"),
                            (222, "test_y@test.test", "test_username_y"),
                            (333, "test_z@test.test", "test_username_z")
                        ]

        UPDATE core_user AS base
        SET
            email = val.email,
            username = val.username
        FROM (
            VALUES
            (111, 'test_x@test.test', 'test_username_x'),
            (222, 'test_y@test.test', 'test_username_y'),
            (333, 'test_z@test.test', 'test_username_z')
        ) AS val(id, email, username)
        WHERE base.id = val.id
        """
        query = """
        UPDATE {db_table_name} as base
        SET
            {set_str}
        FROM (
            VALUES
            {values_str}
        ) AS val(id, {fields_str})
        WHERE base.id = val.id
        """

        set_str = ",\n\t    ".join([
            "{} = val.{}".format(field, field)
            for field in field_names
        ])
        values_str = ",\n\t    ".join([str(val) for val in values])
        fields_str = ", ".join(field_names)

        query = query.format(
            db_table_name=db_table_name,
            set_str=set_str,
            values_str=values_str,
            fields_str=fields_str
        )
        return query

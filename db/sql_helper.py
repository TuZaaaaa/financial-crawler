import pymysql


class SqlHelper:
    def __init__(self, user='root', password='roo1t', database='crawler_db', host='49.232.214.47', port=3307):
        self.user = user
        self.password = password
        self.database = database
        self.host = host
        self.port = port
        self.conn = pymysql.connect(user=self.user, password=self.password, database=self.database, host=self.host,
                                    port=self.port)
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)

    def get_one(self, sql, args):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchone()
        return result

    def get_list(self, sql, args):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchall()
        return result

    def modify(self, sql, args):
        self.cursor.execute(sql, args)
        self.conn.commit()

    def multiple_modify(self, sql, args):
        self.cursor.executemany(sql, args)
        self.conn.commit()

    def create(self, sql, args):
        self.cursor.execute(sql, args)
        result = self.cursor.lastrowid
        self.conn.commit()
        return result

    def close(self):
        self.cursor.close()
        self.conn.close()

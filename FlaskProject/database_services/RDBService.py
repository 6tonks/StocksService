import pymysql
import json
import middleware.context as context


def _get_db_connection():

    db_connect_info = context.get_db_info()

    print("Connection info = \n", json.dumps(db_connect_info, indent=2, default=str))

    db_connection = pymysql.connect(**db_connect_info)
    return db_connection


def get_table(db_schema, table_name):

    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "select * from " + db_schema + "." + table_name
    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql)
    res = cur.fetchall()

    conn.close()

    return res
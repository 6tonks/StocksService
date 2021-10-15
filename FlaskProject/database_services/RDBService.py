import pymysql
import json
import middleware.context as context


def _get_db_connection():

    db_connect_info = context.get_db_info()

    print("Connection info = \n", json.dumps(db_connect_info, indent=2, default=str))

    db_connection = pymysql.connect(**db_connect_info)
    return db_connection


def update_stock(db_schema, table_name, stock_ticker, stock_name, stock_price):
    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "INSERT INTO " + db_schema + "." + table_name + " (ticker, stock_name, latest_price) " \
          + "VALUES ('%s', '%s', %s)" %(stock_ticker, stock_name, stock_price) + " ON DUPLICATE KEY UPDATE " + \
          "stock_name='%s', latest_price='%s'" %(stock_name, stock_price)
    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql)
    res = conn.commit()

    conn.close()

    return res

def get_table(db_schema, table_name):

    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "select * from " + db_schema + "." + table_name
    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql)
    res = cur.fetchall()

    conn.close()

    return res


def get_by_prefix(db_schema, table_name, column_name, value_prefix):

    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "select * from " + db_schema + "." + table_name + " where " + \
        column_name + " like " + "'" + value_prefix + "%'"
    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql)
    res = cur.fetchall()

    conn.close()

    return res


def delete_by_prefix(db_schema, table_name, column_name, value_prefix):

    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "delete from " + db_schema + "." + table_name + " where " + \
        column_name + "=" + "'" + value_prefix + "'"
    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql)
    res = conn.commit()

    conn.close()

    return res


def clear_table(db_schema, table_name):
    conn = _get_db_connection()
    cur = conn.cursor()

    sql = "delete from " + db_schema + "." + table_name
    print("SQL Statement = " + cur.mogrify(sql, None))

    res = cur.execute(sql)
    res = conn.commit()

    conn.close()

    return res

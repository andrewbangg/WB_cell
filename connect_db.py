import json
import sqlite3
import copy_db_wb
import psycopg2
import settings

conn = psycopg2.connect(host=settings.DATABASE['default']['HOST'],
                        port=settings.DATABASE['default']['PORT'],
                        password=settings.DATABASE['default']['PASSWORD'],
                        dbname=settings.DATABASE['default']['NAME'],
                        user=settings.DATABASE['default']['USER'])
cursor = conn.cursor()


def connect_db(wb_path, path_app):
    copy_db_wb.copy_wb_db(wb_path, path_app)
    path_db = r'wb_point_db.sqlite'
    connection = sqlite3.connect(path_db)
    cursor = connection.cursor()
    # cursor.execute('SELECT * FROM buyers_with_cells order by status_updated desc limit 1')
    cursor.execute(
        'SELECT cell,acceptance_unix_timestamp,scanned_code FROM goods_in_pick_point order by acceptance_unix_timestamp desc limit 1')
    cell_sql = cursor.fetchall()
    cursor.close()
    metadata_cell = {"cell": cell_sql[0][0],
                     "ts": cell_sql[0][1],
                     "scaned_code": cell_sql[0][2]}
    return metadata_cell


def connect_db_get_id(wb_path, path_app):
    copy_db_wb.copy_wb_db(wb_path, path_app)
    path_db = r'wb_point_db.sqlite'
    connection = sqlite3.connect(path_db)
    connection.row_factory = sqlite3.Row
    # cursor.execute('SELECT * FROM buyers_with_cells order by status_updated desc limit 1')
    row = connection.cursor().execute(
        'SELECT * FROM local_storage_table where key = "pickPoint"').fetchone()

    pick_point_data = json.loads(dict(row)['value'])
    pick_point_data_dict = json.loads(pick_point_data)
    pvz_id = pick_point_data_dict['external_id']
    connection.close()
    return pvz_id


def check_subsc(id_pvz):
    cursor.execute(f"SELECT * from pay_success where pvz_id = '{id_pvz}'")
    record = cursor.fetchall()
    if len(record) >= 1:
        return True
    else:
        return False

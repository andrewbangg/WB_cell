import json
import time

import check_job
import connect_db
import xprinter


def check_cell(wb_path, path_app, name_printer, flag_check_queue, size_stick):
    cash = {'cell': None,
            'timestamp': None,
            'scaned_code': None}
    while True:
        try:
            if flag_check_queue:
                check_job.check_job(name_printer)
            time.sleep(0.01)
            cell_db = connect_db.connect_db(wb_path, path_app)
            cell = str(cell_db['cell'])
            timestamp = str(cell_db['ts'])
            scaned_code = str(cell_db['scaned_code'])
            if len(cell) < 1:
                print('В последней строке ничего нет')
            else:
                if cash['cell'] is None:
                    cash['cell'] = cell
                    cash['timestamp'] = timestamp
                    cash['scaned_code'] = scaned_code
                    xprinter.print_yc(f'{cell}.', size_stick)
                    print(cash['cell'])
                else:
                    if cash['cell'] == cell:
                        if cash['scaned_code'] == scaned_code:
                            pass
                        else:
                            cash.clear()
                            cash['cell'] = cell
                            cash['timestamp'] = timestamp
                            cash['scaned_code'] = scaned_code
                            xprinter.print_yc(f'{cash["cell"]}.', size_stick)
                            print(cash['cell'])
                    else:
                        cash.clear()
                        cash['cell'] = cell
                        cash['timestamp'] = timestamp
                        cash['scaned_code'] = scaned_code
                        xprinter.print_yc(f'{cash["cell"]}.', size_stick)
                        print(cash['cell'])
        except Exception as e:
            print(e)


if __name__ == '__main__':
    with open('conf.json', 'r', encoding='utf-8') as conf:
        file = json.load(conf)
        wb_path = file['WB_DB']
        path_app = file['PATH_CELL']
        size_stick = int(file['SIZE_STICK'])
        name_printer = file['NAME_PRINTER']
        flag_check_queue = file['FLAG_CHECK_QUEUE']
    pvz_id = connect_db.connect_db_get_id(wb_path, path_app)
    check_subsc = connect_db.check_subsc(pvz_id)
    if check_subsc:
        check_cell(wb_path, path_app, name_printer, flag_check_queue, size_stick)
    else:
        print(
            'У вас закончилась подписка.\nДля возобновления пользования программой, продлите подписку в телеграм-боте @wb_buy_cell_bot.')
        time.sleep(1500)

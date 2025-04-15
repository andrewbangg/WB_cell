
import connect_db


cash = []

def check_cell(cell_db):
    cell = cell_db
    if len(cell_db) < 1:
        print('В последней строке ничего нет')
    else:
        cell_is_db = cell_db[0][0]
        if len(cash) == 0:
            cash.append(cell_is_db)
            return cell_is_db
        else:
            if cash[0] == cell_is_db:
                return
            else:
                cash.clear()
                cash.append(cell[0])
                return cell_is_db

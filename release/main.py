import sqlite3
import sys

from addEditCoffeeForm import Ui_Window

from PyQt6.QtWidgets import QLineEdit, QSpinBox
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem


class Window(QMainWindow, Ui_Window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.path_bd = "data/coffee.sqlite"
        self.name_table = "coffee_redactor"
        self.set_tw()

        les_append_list = [self.sb_ID, self.le_name_variety, self.sb_degree_roast, self.le_type_make,
                           self.le_description, self.sb_price, self.sb_volume]
        self.coll_type = [None, str, str, str, str, str, str]
        coll_names_list = self.get_coll_names()
        self.les_type = []
        self.les_append = {}
        for i in range(len(coll_names_list)):
            self.les_append[coll_names_list[i]] = les_append_list[i]
            if type(les_append_list[i]) == QSpinBox:
                self.les_type.append(int)
            elif type(les_append_list[i]) == QLineEdit:
                self.les_type.append(str)

        self.initUI()

    def initUI(self):
        self.pb_append.clicked.connect(self.append_row)
        self.pb_update.clicked.connect(self.update_bd)

    def append_row(self):
        self.status_bar.showMessage("")
        if self.les_append["ID"].value() in list(map(lambda row: row[0], self.set_bd(f"SELECT * FROM {self.name_table}", True))):
            self.status_bar.showMessage("Кофе с таким ID уже существует!")
        else:
            rowPosition = self.tw_data.rowCount()
            self.tw_data.insertRow(rowPosition)
            ind = 0
            for k, v in self.les_append.items():
                insert_item = ""
                if self.les_type[ind] == int:
                    insert_item = v.value()
                elif  self.les_type[ind] == str:
                    insert_item = v.text()
                self.tw_data.setItem(rowPosition, ind, QTableWidgetItem(str(insert_item)))
                ind += 1

    def update_bd(self):
        coll_names = self.get_coll_names()
        coll_bd = list(map(lambda row: row[0], self.set_bd(f"SELECT * FROM {self.name_table}", True)))
        for i_row in range(self.tw_data.rowCount()):
            keys, items = [], []
            for i_coll in range(self.tw_data.columnCount()):
                key = coll_names[i_coll]
                if self.coll_type[i_coll] == None:
                    key = coll_names[i_coll]
                elif self.coll_type[i_coll] == str:
                    key = f"'{coll_names[i_coll]}'"
                item = "-"
                if self.les_type[i_coll] == int:
                    item = f"{self.tw_data.item(i_row, i_coll).text()}"
                elif self.les_type[i_coll] == str:
                    item = f"'{self.tw_data.item(i_row, i_coll).text()}'"
                keys.append(key)
                items.append(item)
            ID = int(self.tw_data.item(i_row, 0).text())
            if ID in coll_bd:
                for i in range(len(keys)):
                    # print(f"""UPDATE {self.name_table} SET {keys[i]} = {items[i]} WHERE ID = {ID}""")
                    # print()
                    self.set_bd(f"""UPDATE {self.name_table}
                                          SET {keys[i]} = {items[i]}
                                          WHERE ID = {ID}""", False)
            else:
                keys, items = ", ".join(keys), ", ".join(items)
                # print(f"INSERT INTO {self.name_table}({keys}) VALUES({items})")
                # print()
                self.set_bd(f"INSERT INTO {self.name_table}({keys}) VALUES({items})", False)
        self.status_bar.showMessage("БД обновлена!")
        self.set_tw()

    def set_bd(self, query, do_return):
        connection = sqlite3.connect(self.path_bd)
        cursor = connection.cursor()
        res = None
        if do_return:
            res = cursor.execute(query).fetchall()
        else:
            cursor.execute(query)
            connection.commit()
        connection.close()
        if do_return:
            return res

    def get_coll_names(self):
        connection = sqlite3.connect(self.path_bd)
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {self.name_table}")
        res = list(map(lambda x: x[0], cursor.description))
        connection.close()
        return res

    def set_tw(self):
        res = self.set_bd(f"SELECT * FROM {self.name_table}", True)
        coll_names = self.get_coll_names()
        self.tw_data.setColumnCount(len(coll_names))
        self.tw_data.setHorizontalHeaderLabels(coll_names)
        self.tw_data.setRowCount(0)
        for i, row in enumerate(res):
            self.tw_data.setRowCount(
                self.tw_data.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tw_data.setItem(
                    i, j, QTableWidgetItem(str(elem)))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec())
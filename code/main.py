import sys
import sqlite3
from random import randint
from datetime import datetime
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTableWidgetItem, QMessageBox
from main_menu_interface import Ui_MainWindow
from visualyser_interface import Ui_Form
from first_train_interface import Ui_Form_1, Ui_Form_Settings_1
from second_train_interface import Ui_Form_2, Ui_Form_Settings_2, HoverButton
from PyQt5 import QtCore


class MainMenu(QMainWindow, Ui_MainWindow):
    """Главное меню,  из которого открываются  все функции программы"""

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.open_first_train)
        self.pushButton_2.clicked.connect(self.open_second_train)
        self.pushButton_3.clicked.connect(self.open_your_results)

    def open_first_train(self):
        """Открываем первую тренировку, если введено имя пользователя"""
        if self.lineEdit.text():
            # передаем в конструктор класса имя  пользователя
            self.first_train = FirstTrain(self.lineEdit.text())
            self.first_train.show()
        else:
            QMessageBox.question(self, 'Введите  %user_name%',
                                 "Для того, чтобы  начать  игру, нужно ввести имя пользователя", QMessageBox.Ok)

    def open_second_train(self):
        """Открываем окно второй тренировки"""
        if self.lineEdit.text():
            # передаем в конструктор класса имя  пользователя
            self.second_train = SecondTrain(self.lineEdit.text())
            self.second_train.show()
        else:
            QMessageBox.question(self, 'Введите  %user_name%',
                                 "Для того, чтобы  начать  игру, нужно ввести имя пользователя", QMessageBox.Ok)

    def open_your_results(self):
        """Открываем окно для мониторинга результатов"""
        if self.lineEdit.text():
            # передаем в конструктор класса имя  пользователя
            self.your_results = YourResults(self.lineEdit.text())
            self.your_results.show()
        else:
            QMessageBox.question(self, 'Введите  %user_name%',
                                 "Для того, чтобы  начать  игру, нужно ввести имя пользователя", QMessageBox.Ok)


class FirstTrain(QMainWindow, Ui_Form_1):
    """Первая минии-игра"""

    def __init__(self, user_name):
        super().__init__()
        self.setupUi(self)
        self.hoverButton_positive.clicked.connect(self.positive_click)
        self.hoverButton_negative.clicked.connect(self.negative_click)
        self.pushButton.clicked.connect(self.prepare_to_start)
        self.pushButton_2.clicked.connect(self.stop)
        self.pushButton_3.clicked.connect(self.open_settings)
        self.hoverButton_positive.hide()
        self.hoverButton_negative.show()
        # задаем начальные значения параметров игры
        self.ping = 500
        self.n = 15
        # вспомогательный счетчик для остановки игры
        self.count = 0
        # считаем  удавшиеся попытки
        self.correct_pushes = 0
        # создаем  таймер, чтобы отсчитывать интервал  между картинками
        self.timer_1 = QTimer()
        self.timer_1.timeout.connect(self.change_button_1)
        # создаем таймер, чтобы отсчитывать интервал жизни картинки, на которую можно нажимать
        self.timer_2 = QTimer()
        self.timer_2.timeout.connect(self.change_button_2)
        # задаем временные рамки,  когда  кнопка может поменяться  (в секундах)
        self.time_range_min = 2000
        self.time_range_max = 5000
        # база данных, используемая для  работы
        self.con = sqlite3.connect("results.db")
        self.user_name = user_name
        #  фиксируем остановку игры
        self.changes = False

    def positive_click(self):
        """"Засчитываем удачное нажатие"""
        self.correct_pushes += 1
        self.lcdNumber.display(self.correct_pushes)
        self.hoverButton_positive.setEnabled(False)

    def negative_click(self):
        """Засчитываем ложное срабатывание, отнимая очки"""
        if self.correct_pushes:
            self.correct_pushes -= 1
            self.lcdNumber.display(self.correct_pushes)

    def stop(self):
        """Останавливаем игру  по желанию пользователя.
        Для этого изменяем  значение счетчика и записывам изменение в переменную"""
        self.count = self.n + 1
        self.changes = True

    def prepare_to_start(self):
        """Подготовка к началу игры"""
        self.count = 0
        self.correct_pushes = 0
        self.changes = False
        self.lcdNumber.display(self.correct_pushes)
        self.first_stage()

    def first_stage(self):
        """Первый этап  цикла смены  кнопок"""
        self.count += 1
        if self.count <= self.n:
            self.timer_1.start(randint(self.time_range_min, self.time_range_max))
        elif not self.changes:
            self.message_window()

    def change_button_1(self):
        """Меняем отображение кнопок 1-й раз"""
        if not self.changes:
            self.timer_1.stop()
            self.hoverButton_positive.show()
            self.hoverButton_positive.setEnabled(True)
            self.hoverButton_negative.hide()
            self.timer_2.start(self.ping)

    def change_button_2(self):
        """Меняем отображение кнопок 2-й раз"""
        self.timer_2.stop()
        self.hoverButton_negative.show()
        self.hoverButton_positive.hide()
        # повторяем  все сначала
        self.first_stage()

    def message_window(self):
        """Предложение  сохранить результат в базу данных"""
        valid = QMessageBox.question(self, 'Сохранить результат',
                                     "Вы действительно хотите сохранить эту  попытку?", QMessageBox.Yes,
                                     QMessageBox.No)
        if valid == QMessageBox.Yes:
            # сохраняем результат в базу данных
            self.data_base()

    def data_base(self):
        """"Сохранение в базу данных"""
        cur = self.con.cursor()
        config = str(self.ping) + "_" + str(self.n) + "_" + str(self.time_range_min) + "_" + str(self.time_range_max)
        date_time = datetime.today().isoformat(sep=" ")[:-7]
        cur.execute(
            "INSERT INTO first_train(user_name, score, config, date_time) VALUES ('{}', {}, '{}', '{}')".format(
                self.user_name,
                self.correct_pushes,
                config,
                date_time))
        self.con.commit()

    def open_settings(self):
        """Открываем настройки"""
        self.stop()
        self.settings = FirstTrainSettings()
        self.settings.show()


class FirstTrainSettings(QWidget, Ui_Form_Settings_1):
    """Настройки для первой тренировки"""

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.parametres_to_the_mainform)
        self.pushButton_2.clicked.connect(self.close)
        self.spinBox.setValue(ex.first_train.ping)
        self.spinBox_2.setValue(ex.first_train.n)
        self.spinBox_3.setValue(ex.first_train.time_range_min)
        self.spinBox_4.setValue(ex.first_train.time_range_max)

    def parametres_to_the_mainform(self):
        """Применяем  настройки и передаем параметры в главное окно"""
        ex.first_train.ping = int(self.spinBox.text())
        ex.first_train.n = int(self.spinBox_2.text())
        ex.first_train.time_range_min, ex.first_train.time_range_max = sorted((int(self.spinBox_3.text()),
                                                                               int(self.spinBox_4.text())))
        self.close()


class SecondTrain(QMainWindow, Ui_Form_2):
    """Вторая мини-игра"""

    def __init__(self, user_name):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.start)
        self.pushButton_2.clicked.connect(self.stop)
        self.pushButton_3.clicked.connect(self.open_settings)
        # создаем  пары  "кнопка + таймер"
        self.n_buttons = 10
        self.buttons_and_timers = [(HoverButton(self), QTimer()) for i in range(self.n_buttons)]
        for elem in self.buttons_and_timers:
            elem[0].setGeometry(QtCore.QRect(40, 40, 60, 60))
            elem[0].hide()
            elem[0].clicked.connect(self.clicked_button)
            elem[1].timeout.connect(self.hide_button)
        # главный  таймер
        self.timer = QTimer()
        self.timer.timeout.connect(self.show_new_button)
        # интервал появления кнопок
        self.time_range_min = 600
        self.time_range_max = 1500
        # задаем начальные парамтры
        self.ping = 800
        self.n = 20
        # очередь  кнопок
        self.current_buttons = []
        self.button_index = 0
        # считаем количество показанных кнопок
        self.count = 0
        # считаем нажатия
        self.pushes = 0
        #  подключаем базу данных
        self.con = sqlite3.connect("results.db")
        self.user_name = user_name
        # фиксируем остановку игры
        self.changes = True

    def stop(self):
        """Останавливаем игру  по желанию пользователя.
        Для этого изменяем  значение счетчика и записывам изменение в переменную"""
        self.count = self.n + 1
        self.changes = True

    def start(self):
        """Функция, в  которой запускается главный таймер"""
        self.pushes = 0
        self.count = 0
        self.button_index = 0
        self.changes = False
        self.current_buttons.clear()
        self.timer.stop()
        for elem in self.buttons_and_timers:
            elem[0].hide()
            elem[1].stop()
        self.lcdNumber.display(self.pushes)
        self.timer.start(randint(self.time_range_min, self.time_range_max))

    def show_new_button(self):
        """Показываем новую кнопку"""
        if self.count < self.n:
            self.count += 1
            self.buttons_and_timers[self.button_index][0].move(randint(0, 250), randint(0, 300))
            self.buttons_and_timers[self.button_index][0].show()
            self.buttons_and_timers[self.button_index][1].start(self.ping)
            # добавляем  кнопку в очередь
            self.current_buttons.append(self.button_index)
            # следим, чтобы индекс был корректен  и список  шел  покругу
            if self.button_index != self.n_buttons - 1:
                self.button_index += 1
            else:
                self.button_index = 0
        elif not self.changes:
            self.timer.stop()
            for elem in self.buttons_and_timers:
                elem[0].hide()
            # вызываем диалоговое  окно для сохарнения результатаа в базу данных
            self.message_window()

    def hide_button(self):
        """По истечении времени таймера прячем  кнопку и удаляем ее из очереди"""
        self.buttons_and_timers[self.current_buttons[0]][0].hide()
        self.buttons_and_timers[self.current_buttons[0]][1].stop()
        self.current_buttons.pop(0)

    def clicked_button(self):
        """Обрабатываемнажатие на кнопку. Кнопка скрывается, а счетчик обновляется"""
        self.sender().hide()
        self.pushes += 1
        self.lcdNumber.display(self.pushes)

    def message_window(self):
        """Предложение  сохранить результат в базу данных"""
        valid = QMessageBox.question(self, 'Сохранить результат',
                                     "Вы действительно хотите сохранить эту  попытку?", QMessageBox.Yes,
                                     QMessageBox.No)
        if valid == QMessageBox.Yes:
            # сохраняем результат в базу данных
            self.data_base()

    def data_base(self):
        """"Сохранение в базу данных"""
        cur = self.con.cursor()
        config = str(self.ping) + "_" + str(self.n) + "_" + str(self.time_range_min) + "_" + str(self.time_range_max)
        date_time = datetime.today().isoformat(sep=" ")[:-7]
        cur.execute(
            "INSERT INTO second_train(user_name, score, config, date_time) VALUES ('{}', {}, '{}', '{}')".format(
                self.user_name,
                self.pushes,
                config,
                date_time))
        self.con.commit()

    def open_settings(self):
        self.stop()
        self.settings = SecondTrainSettings()
        self.settings.show()


class SecondTrainSettings(QWidget, Ui_Form_Settings_2):
    """Настройки для первой тренировки"""

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.parametres_to_the_mainform)
        self.pushButton_2.clicked.connect(self.close)
        self.spinBox.setValue(ex.second_train.ping)
        self.spinBox_2.setValue(ex.second_train.n)
        self.spinBox_3.setValue(ex.second_train.time_range_min)
        self.spinBox_4.setValue(ex.second_train.time_range_max)

    def parametres_to_the_mainform(self):
        """Применяем  настройки и передаем параметры в главное окно"""
        ex.second_train.ping = int(self.spinBox.text())
        ex.second_train.n = int(self.spinBox_2.text())
        ex.second_train.time_range_min, ex.second_train.time_range_max = sorted((int(self.spinBox_3.text()),
                                                                                 int(self.spinBox_4.text())))
        self.close()


class YourResults(QMainWindow, Ui_Form):
    def __init__(self, user_name):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.user_request)
        self.pushButton_2.clicked.connect(self.history)
        self.pushButton_3.clicked.connect(self.delete_elem)
        self.checkBox.stateChanged.connect(self.checkbox_1)
        self.checkBox.setChecked(True)
        self.checkBox_2.stateChanged.connect(self.checkbox_1)
        # словарь в  котором ключ - чекбокс, а  значение - список полей  ввода данного чекбокса
        # необходим, чтобы можно было удобно делать поля активными/неактивными
        self.checkbox_and_lines = {
            self.checkBox_6: (self.lineEdit_2,),
            self.checkBox_4: (self.dateTimeEdit, self.dateTimeEdit_2),
            self.checkBox_5: (self.spinBox, self.spinBox_2)
        }
        self.checkBox_4.stateChanged.connect(self.checkbox_2)
        self.checkBox_5.stateChanged.connect(self.checkbox_2)
        self.checkBox_6.stateChanged.connect(self.checkbox_2)
        # подключаем базу данных
        self.con = sqlite3.connect("results.db")
        self.user_name = user_name

    def user_request(self):
        """Формируем пользовательский запрос"""
        cur = self.con.cursor()
        # собираем  наш запрос в кучу
        request = "SELECT * FROM "
        que = []
        if self.checkBox.isChecked():
            request += "first_train WHERE"
        else:
            request += "second_train WHERE"
        que.append("(user_name = '{}')".format(self.user_name))
        if not self.checkBox_4.isChecked():
            # переводим данные в удобный для базы данных формат
            date_time_min = self.dateTimeEdit.dateTime().toString(Qt.ISODate).replace("T", " ")
            date_time_max = self.dateTimeEdit_2.dateTime().toString(Qt.ISODate).replace("T", " ")
            que.append("(date_time >= '{}' AND date_time <= '{}')".format(date_time_min,
                                                                          date_time_max))
        if not self.checkBox_5.isChecked():
            que.append("(score >= {} AND score <= {})".format(self.spinBox.text(),
                                                              self.spinBox_2.text()))
        request += " " + " AND ".join(que)
        result = cur.execute(request).fetchall()
        title = [description[0] for description in cur.description]
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(len(result))
        for i in range(len(result)):
            for j in range(len(title)):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(result[i][j])))
        self.tableWidget.resizeColumnsToContents()

    def history(self):
        """Выводим всю историю одной из тренировок"""
        cur = self.con.cursor()
        if self.checkBox.isChecked():
            result = cur.execute("SELECT * from first_train WHERE user_name = '{}'".format(self.user_name)).fetchall()
        else:
            result = cur.execute("SELECT * from second_train WHERE user_name = '{}'".format(self.user_name)).fetchall()
        title = [description[0] for description in cur.description]
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(len(result))
        for i in range(len(result)):
            for j in range(len(title)):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(result[i][j])))
        self.tableWidget.resizeColumnsToContents()

    def checkbox_1(self, state):
        """Делаем так, чтобы нельзя была выбрать больше одной тренировки"""
        if state == Qt.Checked:
            if self.sender().text() == "Тренировка №1":
                self.checkBox_2.setChecked(False)
            else:
                self.checkBox.setChecked(False)
        else:
            if self.sender().text() == "Тренировка №1":
                self.checkBox_2.setChecked(True)
            else:
                self.checkBox.setChecked(True)

    def checkbox_2(self, state):
        """Если чекбокс активен,  то  окна ввода неактивны, и наоборот"""
        if state == Qt.Checked:
            for elem in self.checkbox_and_lines[self.sender()]:
                elem.setDisabled(True)
        else:
            for elem in self.checkbox_and_lines[self.sender()]:
                elem.setEnabled(True)

    def delete_elem(self):
        """Удаляем выделенные  курсором элементы из базы данных"""
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        ids = [self.tableWidget.item(i, 0).text() for i in rows]
        valid = QMessageBox.question(self, 'Удаление из базы данных',
                                     "Действительно удалить элементы с id " +
                                     ",".join(ids), QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            cur = self.con.cursor()
            if self.checkBox.isChecked():
                cur.execute("DELETE from first_train WHERE ID in (" +
                            ", ".join('?' * len(ids)) + ")", ids)
            else:
                cur.execute("DELETE from second_train WHERE ID in (" +
                            ", ".join('?' * len(ids)) + ")", ids)

            self.con.commit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = MainMenu()
    ex.show()
    sys.exit(app.exec_())

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form_1(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(483, 360)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(20, 20, 31, 31))
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(370, 0, 111, 71))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.lcdNumber = QtWidgets.QLCDNumber(self.verticalLayoutWidget)
        self.lcdNumber.setLineWidth(1)
        self.lcdNumber.setObjectName("lcdNumber")
        self.verticalLayout.addWidget(self.lcdNumber)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(360, 250, 121, 101))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_2.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_2.addWidget(self.pushButton_3)

        self.hoverButton_positive = HoverButtonPositive(Form)
        self.hoverButton_positive.setGeometry(QtCore.QRect(30, 30, 270, 270))

        self.hoverButton_negative = HoverButtonNegative(Form)
        self.hoverButton_negative.setGeometry(QtCore.QRect(30, 30, 270, 270))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Тренировка №1"))
        self.label_4.setText(_translate("Form", "Удачных попыток:"))
        self.pushButton.setText(_translate("Form", "Пуск"))
        self.pushButton_2.setText(_translate("Form", "Стоп"))
        self.pushButton_3.setText(_translate("Form", "Настройки"))


class HoverButtonPositive(QtWidgets.QPushButton):
    """Создаем  круглую кнопку, нажатие которой засчитывается"""

    def __init__(self, parent=None):
        super(HoverButtonPositive, self).__init__(parent)
        self.setStyleSheet('''border-image: url("positivet.png")''')

    def resizeEvent(self, event):
        self.setMask(QtGui.QRegion(self.rect(), QtGui.QRegion.Ellipse))
        QtWidgets.QPushButton.resizeEvent(self, event)


class HoverButtonNegative(QtWidgets.QPushButton):
    """Создаем  круглую кнопку, нажатие которойне НЕ засчитывается"""

    def __init__(self, parent=None):
        super(HoverButtonNegative, self).__init__(parent)
        self.setStyleSheet('''border-image: url("negativet.png")''')

    def resizeEvent(self, event):
        self.setMask(QtGui.QRegion(self.rect(), QtGui.QRegion.Ellipse))
        QtWidgets.QPushButton.resizeEvent(self, event)


class Ui_Form_Settings_1(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(380, 139)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 10, 151, 111))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.spinBox = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.spinBox.setWrapping(True)
        self.spinBox.setFrame(True)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(10000)
        self.spinBox.setObjectName("spinBox")
        self.verticalLayout.addWidget(self.spinBox)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.spinBox_2 = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.spinBox_2.setMinimum(1)
        self.spinBox_2.setMaximum(10000)
        self.spinBox_2.setObjectName("spinBox_2")
        self.verticalLayout.addWidget(self.spinBox_2)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(180, 10, 181, 111))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.spinBox_3 = QtWidgets.QSpinBox(self.verticalLayoutWidget_2)
        self.spinBox_3.setObjectName("spinBox_3")
        self.spinBox_3.setMinimum(1)
        self.spinBox_3.setMaximum(10000)
        self.verticalLayout_2.addWidget(self.spinBox_3)
        self.spinBox_4 = QtWidgets.QSpinBox(self.verticalLayoutWidget_2)
        self.spinBox_4.setObjectName("spinBox_4")
        self.spinBox_4.setMinimum(1)
        self.spinBox_4.setMaximum(10000)
        self.verticalLayout_2.addWidget(self.spinBox_4)
        spacerItem = QtWidgets.QSpacerItem(20, 3, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Тренировка  №1. Настройки"))
        self.label.setText(_translate("Form", "Задержка, мс:"))
        self.label_2.setText(_translate("Form", "Количество повторений:"))
        self.label_3.setText(_translate("Form", "Интервал  появления кнопки, мс:"))
        self.pushButton.setText(_translate("Form", "Применить"))
        self.pushButton_2.setText(_translate("Form", "Отмена"))

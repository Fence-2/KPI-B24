# -*- coding: utf-8 -*-

# Created by: PyQt5 UI code generator 5.15.6

from PyQt5 import QtCore, QtWidgets
from qtwidgets import PasswordEdit
from datetime import datetime

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(260, 413)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")

        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.month = QtWidgets.QSpinBox(Form)
        self.month.setObjectName("month")
        self.month.setMinimum(1)
        self.month.setMaximum(12)
        self.month.setProperty("value", datetime.now().month)
        self.horizontalLayout_2.addWidget(self.month)

        self.year = QtWidgets.QSpinBox(Form)
        self.year.setObjectName("year")
        self.year.setMinimum(2010)
        self.year.setMaximum(2030)
        self.year.setProperty("value", 2022)
        self.horizontalLayout_2.addWidget(self.year)

        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 2, 1, 1)

        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 1, 1, 1)

        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1)

        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 1, 1, 1)

        self.login = QtWidgets.QLineEdit(Form)
        self.login.setObjectName("login")
        self.gridLayout.addWidget(self.login, 0, 2, 1, 1)

        self.password = PasswordEdit(Form)
        self.password.setObjectName("password")
        self.gridLayout.addWidget(self.password, 1, 2, 1, 1)

        self.webhook = PasswordEdit(Form)
        self.webhook.setObjectName("webhook")
        self.gridLayout.addWidget(self.webhook, 2, 2, 1, 1)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.working_emp = QtWidgets.QCheckBox(Form)
        self.working_emp.setChecked(True)
        self.working_emp.setProperty("value", True)
        self.verticalLayout.addWidget(self.working_emp)

        self.fired_emp = QtWidgets.QCheckBox(Form)
        self.fired_emp.setObjectName("fired_emp")
        self.verticalLayout.addWidget(self.fired_emp)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.gridLayout.addLayout(self.verticalLayout, 4, 2, 1, 1)

        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_3.addWidget(self.label_5)

        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)

        self.gridLayout.addLayout(self.verticalLayout_3, 4, 1, 1, 1)

        self.verticalLayout_2.addLayout(self.gridLayout)

        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)

        self.status = QtWidgets.QLabel(Form)
        self.status.setObjectName("status")
        self.status.setMinimumWidth(250)
        self.horizontalLayout.addWidget(self.status)

        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)

        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.status_bar = QtWidgets.QProgressBar(Form)
        self.status_bar.setProperty("value", 0)
        self.status_bar.setObjectName("status_bar")
        self.verticalLayout_2.addWidget(self.status_bar)

        self.create_report_button = QtWidgets.QPushButton(Form)
        self.create_report_button.setObjectName("create_report_button")
        self.verticalLayout_2.addWidget(self.create_report_button)

        self.label_copyright = QtWidgets.QLabel(Form)
        self.label_copyright.setObjectName("label_5")
        self.label_copyright.setStyleSheet("color: grey; font-style: italic;")
        self.verticalLayout_2.addWidget(self.label_copyright)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Отчёт по эффективности сотрудников"))
        self.label.setText(_translate("Form", "Логин"))
        self.label_3.setText(_translate("Form", "Вебхук"))
        self.label_2.setText(_translate("Form", "Пароль"))
        self.label_4.setText(_translate("Form", "Отчёт за месяц:"))
        self.working_emp.setText(_translate("Form", "Работающие сотрудники"))
        self.fired_emp.setText(_translate("Form", "Уволенные сотрудники"))
        self.label_5.setText(_translate("Form", "Параметры"))
        self.label_copyright.setText(_translate("Form", "@Made by Dmitrii Chistyakov"))
        self.create_report_button.setText(_translate("Form", "Сформировать отчёт"))


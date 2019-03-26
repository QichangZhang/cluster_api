# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(748, 519)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 20, 31, 31))
        self.label.setObjectName("label")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(60, 20, 104, 31))
        self.textEdit.setObjectName("textEdit")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(180, 26, 41, 21))
        self.label_2.setObjectName("label_2")
        self.textEdit_2 = QtWidgets.QTextEdit(Form)
        self.textEdit_2.setGeometry(QtCore.QRect(220, 20, 104, 31))
        self.textEdit_2.setObjectName("textEdit_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(340, 26, 51, 21))
        self.label_3.setObjectName("label_3")
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(380, 20, 86, 31))
        self.comboBox.setObjectName("comboBox")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(490, 20, 89, 31))
        self.pushButton.setObjectName("pushButton")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(20, 80, 711, 431))
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(590, 20, 151, 31))
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")

        self.retranslateUi(Form)
        self.pushButton.clicked.connect(Form.add)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "姓名"))
        self.label_2.setText(_translate("Form", "工号"))
        self.label_3.setText(_translate("Form", "部门"))
        self.pushButton.setText(_translate("Form", "录入信息"))


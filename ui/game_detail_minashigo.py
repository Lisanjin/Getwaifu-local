# Form implementation generated from reading ui file './ui/game_detail_minashigo.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_game_detail_minashigo(object):
    def setupUi(self, game_detail_minashigo):
        game_detail_minashigo.setObjectName("game_detail_minashigo")
        game_detail_minashigo.resize(240, 720)
        game_detail_minashigo.setWindowTitle("")
        game_detail_minashigo.setStyleSheet("")
        self.updateRes = QtWidgets.QPushButton(parent=game_detail_minashigo)
        self.updateRes.setGeometry(QtCore.QRect(65, 640, 110, 23))
        self.updateRes.setObjectName("updateRes")
        self.resouce_version = QtWidgets.QLabel(parent=game_detail_minashigo)
        self.resouce_version.setGeometry(QtCore.QRect(0, 670, 240, 16))
        self.resouce_version.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.resouce_version.setObjectName("resouce_version")
        self.update_time = QtWidgets.QLabel(parent=game_detail_minashigo)
        self.update_time.setGeometry(QtCore.QRect(0, 690, 240, 16))
        self.update_time.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.update_time.setObjectName("update_time")
        self.comboBox = QtWidgets.QComboBox(parent=game_detail_minashigo)
        self.comboBox.setGeometry(QtCore.QRect(45, 30, 150, 22))
        self.comboBox.setObjectName("comboBox")
        self.textEdit = QtWidgets.QTextEdit(parent=game_detail_minashigo)
        self.textEdit.setGeometry(QtCore.QRect(45, 90, 150, 32))
        self.textEdit.setObjectName("textEdit")
        self.review_button = QtWidgets.QPushButton(parent=game_detail_minashigo)
        self.review_button.setGeometry(QtCore.QRect(40, 210, 75, 23))
        self.review_button.setObjectName("review_button")
        self.download_button = QtWidgets.QPushButton(parent=game_detail_minashigo)
        self.download_button.setGeometry(QtCore.QRect(140, 210, 75, 23))
        self.download_button.setObjectName("download_button")

        self.retranslateUi(game_detail_minashigo)
        QtCore.QMetaObject.connectSlotsByName(game_detail_minashigo)

    def retranslateUi(self, game_detail_minashigo):
        _translate = QtCore.QCoreApplication.translate
        self.updateRes.setText(_translate("game_detail_minashigo", "更新资源表"))
        self.resouce_version.setText(_translate("game_detail_minashigo", "资源表版本：2.5.503"))
        self.update_time.setText(_translate("game_detail_minashigo", "上次更新时间：2024.10.20"))
        self.review_button.setText(_translate("game_detail_minashigo", "预览"))
        self.download_button.setText(_translate("game_detail_minashigo", "下载"))
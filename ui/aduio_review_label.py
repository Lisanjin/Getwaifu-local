# Form implementation generated from reading ui file './ui/aduio_review_label.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_aduio_review_label(object):
    def setupUi(self, aduio_review_label):
        aduio_review_label.setObjectName("aduio_review_label")
        aduio_review_label.resize(400, 200)
        aduio_review_label.setStyleSheet("")
        self.aduio_play_button = QtWidgets.QPushButton(parent=aduio_review_label)
        self.aduio_play_button.setGeometry(QtCore.QRect(130, 85, 30, 30))
        self.aduio_play_button.setStyleSheet("background-color: grey;")
        self.aduio_play_button.setText("")
        self.aduio_play_button.setIconSize(QtCore.QSize(30, 30))
        self.aduio_play_button.setObjectName("aduio_play_button")
        self.aduio_stop_button = QtWidgets.QPushButton(parent=aduio_review_label)
        self.aduio_stop_button.setGeometry(QtCore.QRect(240, 85, 30, 30))
        self.aduio_stop_button.setStyleSheet("background-color: grey;")
        self.aduio_stop_button.setText("")
        self.aduio_stop_button.setIconSize(QtCore.QSize(30, 30))
        self.aduio_stop_button.setObjectName("aduio_stop_button")
        self.aduio_pause_button = QtWidgets.QPushButton(parent=aduio_review_label)
        self.aduio_pause_button.setGeometry(QtCore.QRect(185, 85, 30, 30))
        self.aduio_pause_button.setStyleSheet("background-color: grey;")
        self.aduio_pause_button.setText("")
        self.aduio_pause_button.setIconSize(QtCore.QSize(30, 30))
        self.aduio_pause_button.setObjectName("aduio_pause_button")

        self.retranslateUi(aduio_review_label)
        QtCore.QMetaObject.connectSlotsByName(aduio_review_label)

    def retranslateUi(self, aduio_review_label):
        _translate = QtCore.QCoreApplication.translate
        aduio_review_label.setWindowTitle(_translate("aduio_review_label", "Form"))
import sys
import config
from qtpy import QtCore, QtWidgets, QtGui


class LaunchDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(LaunchDialog, self).__init__(parent)
        self.okPressed = False

        self.user = QtWidgets.QLabel()
        userEdit = QtWidgets.QLineEdit()
        userEdit.textChanged.connect(self.user_changed)

        self.batch = QtWidgets.QLabel()
        batchEdit = QtWidgets.QLineEdit()
        batchEdit.textChanged.connect(self.batch_changed)

        self.grp = QtWidgets.QLabel()
        grpEdit = QtWidgets.QLineEdit()
        grpEdit.textChanged.connect(self.grp_changed)

        grid = QtWidgets.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(QtWidgets.QLabel('Username'), 1, 0)
        grid.addWidget(userEdit, 1, 1)

        grid.addWidget(QtWidgets.QLabel('D4 Batch No.'), 2, 0)
        grid.addWidget(batchEdit, 2, 1)

        grid.addWidget(QtWidgets.QLabel('Data Group'), 3, 0)
        grid.addWidget(grpEdit, 3, 1)

        okBtn = QtWidgets.QPushButton('Ok', self)
        okBtn.clicked.connect(self.ok_pressed)

        grid.addWidget(okBtn, 4, 2)
        self.setWindowTitle(config.TITLE)
        self.setLayout(grid)
        self.setGeometry(300, 300, 350, 200)

    def ok_pressed(self):
        user, batch, grp = self.get_user(), self.get_user(), self.get_user()
        err = ""
        if user == "":
            err = "Username cannot be empty"
        if batch == "":
            err = "Batch No. cannot be empty"
        if grp == "":
            err = "Test group cannot be empty"
        if err != "":
            reply = QtWidgets.QMessageBox.warning(self, 'Message', err,
                                                  QtWidgets.QMessageBox.Ok)
        else:
            self.okPressed = True
            self.close()

    def user_changed(self, text):
        self.user.setText(text)

    def batch_changed(self, text):
        self.batch.setText(text)

    def grp_changed(self, text):
        self.grp.setText(text)

    def get_user(self):
        return self.user.text()

    def get_batch(self):
        return self.batch.text()

    def get_grp(self):
        return self.grp.text()

    def closeEvent(self, event):
        if self.okPressed:
            event.accept()
        else:
            mb = QtWidgets.QMessageBox
            reply = mb.question(self, 'Message', "Do you want to quit?",
                                mb.Yes, mb.No)
            if reply == mb.Yes:
                self.user.setText("")
                self.batch.setText("")
                self.grp.setText("")
                event.accept()
            else:
                event.ignore()

    @staticmethod
    def get_data(parent=None):
        dialog = LaunchDialog(parent)
        dialog.exec_()
        return {
                'user': dialog.get_user(),
                'batch': dialog.get_batch(),
                'img_grp': dialog.get_grp()
               }

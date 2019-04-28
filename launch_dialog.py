import sys
import config
from qtpy import QtCore, QtWidgets, QtGui


class LaunchDialog(QtWidgets.QDialog):
    """ Class for the launch screen for starting the app.

        This class is designed to provide the layout of the original
        launch window for beginning the application. This window was
        written following the QtPy UI framework. The basic layout of
        this window contains three text entry windows utilized to enter
        intitial data such as the name of the user, the D4 batch number,
        as well as the data group. When all of the appropriate information
        is transfered, the user can proceed to the next window.

    """
    def __init__(self, parent=None):
        """ __init__ method for setting up LaunchDialog UI display

        This method is utilized to set up the location and visualization
        of the launch window. All buttons, labels, and functionalities
        are set here. This method can be called to set up the GUI upon calling
        the class.

        Args:
            parent (class) = Inherited class if present.

        Returns:
            None

        """
        super(LaunchDialog, self).__init__(parent)

        # Initialize button as off
        self.okPressed = False

        # Add QLine Widgets for text entry
        self.user = QtWidgets.QLabel()
        userEdit = QtWidgets.QLineEdit()
        userEdit.textChanged.connect(self.user_changed)

        self.batch = QtWidgets.QLabel()
        batchEdit = QtWidgets.QLineEdit()
        batchEdit.textChanged.connect(self.batch_changed)

        self.grp = QtWidgets.QLabel()
        grpEdit = QtWidgets.QLineEdit()
        grpEdit.textChanged.connect(self.grp_changed)

        self.location = QtWidgets.QLabel()
        locationEdit = QtWidgets.QLineEdit()
        locationEdit.textChanged.connect(self.location_changed)

        grid = QtWidgets.QGridLayout()
        grid.setSpacing(10)

        # Add the labels to various widgets
        grid.addWidget(QtWidgets.QLabel('Username'), 1, 0)
        grid.addWidget(userEdit, 1, 1)

        grid.addWidget(QtWidgets.QLabel('D4 Batch Number'), 2, 0)
        grid.addWidget(batchEdit, 2, 1)

        grid.addWidget(QtWidgets.QLabel('Data Group'), 3, 0)
        grid.addWidget(grpEdit, 3, 1)

        grid.addWidget(QtWidgets.QLabel('Location'), 4, 0)
        grid.addWidget(locationEdit, 4, 1)

        # Ok button = initialized to off
        okBtn = QtWidgets.QPushButton('Ok', self)
        okBtn.clicked.connect(self.ok_pressed)

        grid.addWidget(okBtn, 5, 2)
        self.setWindowTitle(config.TITLE)
        self.setLayout(grid)
        self.setGeometry(300, 300, 350, 200)

    def ok_pressed(self):
        """ Method for regulating what occurs if the OK button is pressed.

        This method controls the user display when buttons are triggered.
        First the get_data() method is called in order to determine the text
        that the user inputted into the text window. Next, string handling is
        done to ensure that none of the parameters are left blank. If there
        are blank entries, the system will provide an error provide. If all
        goes well, the window will terminate.

        Args:
            None
        Returns:
            None

        """
        # Obtain the user inputs:
        user = self.get_user()
        batch = self.get_batch()
        grp = self.get_grp()

        # Determine whether there are blank inputs
        status = True
        if (
            user == "" or
            batch == "" or
            grp == ""
        ):
            error_message = "Please fill in all entries"
            status = False

        # Send an alert message:
        if status == False:

            reply = QtWidgets.QMessageBox.warning(self, 'Message',
                                                  error_message,
                                                  QtWidgets.QMessageBox.Ok)
        # If all entries are valid move to next window
        else:
            self.okPressed = True
            self.close()

    def user_changed(self, text):
        """ Method for handling if the the text has been changed.

        This function is utilized to handle any changes that have
        occured when uploading the user into the text box.

        Args:
            text () =

        Returns:
            None

        """
        self.user.setText(text)

    def batch_changed(self, text):
        """ Method for handling if the the text has been changed.

        This function is utilized to handle any changes that have
        occured when uploading the user into the text box.

        Args:
            text () =

        Returns:
            None

        """
        self.batch.setText(text)

    def grp_changed(self, text):
        """ Method for handling if the the text has been changed.

        This function is utilized to handle any changes that have
        occured when uploading the user into the text box.

        Args:
            text () =

        Returns:
            None

        """
        self.grp.setText(text)

    def location_changed(self, text):
        """ Method for handling if the the text has been changed.

        This function is utilized to handle any changes that have
        occured when uploading the user into the text box.

        Args:
            text (str) = User string input

        Returns:
            None

        """
        self.location.setText(text)

    def get_user(self):
        """ Method for returning the user's information that was uploaded.

        This method is used to determine the data that was uploaded by the
        user in order to save it on the server.

        Args:
            None

        Returns:
            user_input (str) = String containg text passed through by user.

        """
        user_input = self.user.text()

        return user_input

    def get_batch(self):
        """ Method for returning the user's information that was uploaded.

        This method is used to determine the data that was uploaded by the
        user in order to save it on the server.

        Args:
            None

        Returns:
            batch_input (str) = String containg text passed through by user.

        """
        batch_input = self.batch.text()

        return batch_input

    def get_grp(self):
        """ Method for returning the user's information that was uploaded.

        This method is used to determine the data that was uploaded by the
        user in order to save it on the server.

        Args:
            None

        Returns:
            grp_input (str) = String containg text passed through by user.

        """
        grp_input = self.grp.text()

        return grp_input

    def closeEvent(self, event):
        """ Method for handling events after pressing the exit button

        This function contains the logical isntructions for processing
        what happens after the exit button is pressed by the user. First,
        a warning prompt is passed to the user to check if they are willing
        to proceed. If the window wishes to be closed, the text is set back
        to blanks and closed down.

        Args:
            event () =

        Returns:
            None

        """
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
        """ Method for getting all of the data entered at once.

        This function obtains all of the information that has been
        passed to the program thus far at once. It does this by calling
        the functions get_user, get_batch, and get_grp all together and
        passing the data back as a dictionary.

        Args:
            parent (class) = Inheritance if present

        Returns:
            output_dict (dict) = Dictionary containing all of the user
                defined information.

        """
        dialog = LaunchDialog(parent)
        dialog.exec_()

        output_dict = {
                'user': dialog.get_user(),
                'batch': dialog.get_batch(),
                'img_grp': dialog.get_grp(),
               }

        return output_dict

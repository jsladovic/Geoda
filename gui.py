import sys
from PyQt4 import QtGui, QtCore
from cor import CorParser

class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 500, 200)
        self.setWindowTitle('.cor file parser')
        self.home()

    def home(self):
        self.create_file_pickers()
        self.create_radio_buttons()

        self.create_button('Quit', self.close_application, 125)
        self.create_button('Confirm', self.confirm, 375)
        self.create_button('Backup', self.backup, 250)
        
        self.show()

    def create_button(self, text, function, x_position):
        button = QtGui.QPushButton(text, self)
        button.clicked.connect(function)
        button.resize(100, 25)
        button.move(x_position, 160)

    def create_file_pickers(self):
        self.input_file_lbl = QtGui.QLineEdit(self)
        self.input_file_lbl.resize(350, 25)
        self.input_file_lbl.move(15, 10)

        self.input_picker_button = QtGui.QPushButton('Select input folder', self)
        self.input_picker_button.resize(120, 25)
        self.input_picker_button.clicked.connect(self.get_input_filename)
        self.input_picker_button.move(375, 10)
        
        self.output_file_lbl = QtGui.QLineEdit(self)
        self.output_file_lbl.resize(350, 25)
        self.output_file_lbl.move(15, 50)

        self.output_picker_button = QtGui.QPushButton('Select output folder', self)
        self.output_picker_button.resize(120, 25)
        self.output_picker_button.clicked.connect(self.get_output_filename)
        self.output_picker_button.move(375, 50)

    def create_radio_buttons(self):
        self.rb_first_last = QtGui.QRadioButton('First and last lines only', self)
        self.rb_first_last.move(25, 100)
        self.rb_first_last.setChecked(True)
        self.rb_first_last.resize(self.rb_first_last.minimumSizeHint())

        self.every_n_lines = QtGui.QRadioButton('Select every n-th line', self)
        self.every_n_lines.move(25, 125)
        self.every_n_lines.setChecked(False)
        self.every_n_lines.resize(self.every_n_lines.minimumSizeHint())

        self.spin_box = QtGui.QSpinBox(self)
        self.spin_box.move(160, 124)
        self.spin_box.setValue(10)
        self.spin_box.setMinimum(1)
        self.spin_box.setSingleStep(5)
        self.spin_box.resize(self.spin_box.minimumSizeHint())

    def confirm(self):
        input_path, output_path = self.get_file_paths()
        output_path = str(self.output_file_lbl.text()).replace('\\', '/')
        cor = CorParser()
        cor.parse_files(input_path, output_path, self.rb_first_last.isChecked(), self.spin_box.value())
        self.show_popup('Files successfully parsed')

    def backup(self):
        input_path, output_path = self.get_file_paths()
        cor = CorParser()
        cor.backup_files(input_path, output_path)
        self.show_popup('Backup successful')

    def get_file_paths(self):
        input_path = str(self.input_file_lbl.text()).replace('\\', '/')
        output_path = str(self.output_file_lbl.text()).replace('\\', '/')
        return input_path, output_path

    def get_input_filename(self):
        self.get_filename(self.input_file_lbl)

    def get_output_filename(self):
        self.get_filename(self.output_file_lbl)

    def get_filename(self, file_lbl):
        path = QtGui.QFileDialog.getExistingDirectory(self, 'Select folder')
        if path:
            file_lbl.setText(path)
        else:
            file_lbl.setText('') 

    def close_application(self):
        sys.exit()

    def show_popup(self, message):
        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Information)

        msg.setText(message)
        msg.setWindowTitle('Success')
        msg.setStandardButtons(QtGui.QMessageBox.Ok)
	
        retval = msg.exec_()
    
def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

run()

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
        self.create_textbox()

        self.create_button('Quit', self.close_application, 125)
        self.create_button('Confirm', self.confirm, 375)
        self.create_button('Backup', self.backup, 250)
        self.create_button('To GPGGA', self.to_gpgga, 375, 110)
        
        self.show()

    def create_textbox(self):
        self.textbox = QtGui.QLineEdit('0.025', self)
        self.textbox.move(250, 108)
        self.textbox.setValidator(QtGui.QDoubleValidator())

    def create_button(self, text, function, x_position, y_position = 160):
        button = QtGui.QPushButton(text, self)
        button.clicked.connect(function)
        button.resize(100, 25)
        button.move(x_position, y_position)

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
        self.rb_first_last = self.create_radio_button('First and last lines only', 100, True)
        self.every_n_lines = self.create_radio_button('Select every n-th line', 125, False)

        self.spin_box = QtGui.QSpinBox(self)
        self.spin_box.move(160, 124)
        self.spin_box.setValue(10)
        self.spin_box.setMinimum(1)
        self.spin_box.setSingleStep(5)
        self.spin_box.resize(self.spin_box.minimumSizeHint())

    def create_radio_button(self, text, y, checked = False):
        rb = QtGui.QRadioButton(text, self)
        rb.move(25, y)
        rb.setChecked(checked)
        rb.resize(rb.minimumSizeHint())
        return rb

    def confirm(self):
        input_path, output_path = self.get_file_paths()
        output_path = str(self.output_file_lbl.text()).replace('\\', '/')        
        number_of_lines = self.spin_box.value()
        first_last_only = self.rb_first_last.isChecked()
        
        cor = CorParser()
        cor.parse_files(input_path, output_path, first_last_only, number_of_lines)
        self.show_popup('Files successfully parsed')

    def backup(self):
        input_path, output_path = self.get_file_paths()
        cor = CorParser()
        cor.backup_files(input_path, output_path)
        self.show_popup('Backup successful')

    def to_gpgga(self):
        input_path, output_path = self.get_file_paths()
        step = float(self.textbox.text())
        
        cor = CorParser()
        cor.convert_to_gpgga(input_path, output_path, step)
        self.show_popup('Files successfully converted to GPGGA')

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

import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import Image
import pilgram



class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(600, 400)
        Dialog.setMaximumSize(QtCore.QSize(600, 400))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.Input_path = QtWidgets.QLineEdit(Dialog)
        self.Input_path.setObjectName("Input_path")
        self.verticalLayout_2.addWidget(self.Input_path)
        self.button_input_path = QtWidgets.QPushButton(Dialog)
        self.button_input_path.setObjectName("button_input_path")
        self.verticalLayout_2.addWidget(self.button_input_path)
        self.Output_path = QtWidgets.QLineEdit(Dialog)
        self.Output_path.setObjectName("Output_path")
        self.verticalLayout_2.addWidget(self.Output_path)
        self.button_output_path = QtWidgets.QPushButton(Dialog)
        self.button_output_path.setObjectName("button_output_path")
        self.verticalLayout_2.addWidget(self.button_output_path)
        self.sepia_edit = QtWidgets.QLineEdit(Dialog)
        self.sepia_edit.setObjectName("sepia_edit")
        self.verticalLayout_2.addWidget(self.sepia_edit)
        self.Sepia_button = QtWidgets.QPushButton(Dialog)
        self.Sepia_button.setObjectName("Sepia_button")
        self.verticalLayout_2.addWidget(self.Sepia_button)
        self.Contrast_edit = QtWidgets.QLineEdit(Dialog)
        self.Contrast_edit.setObjectName("Contrast_edit")
        self.verticalLayout_2.addWidget(self.Contrast_edit)
        self.Contrast_button = QtWidgets.QPushButton(Dialog)
        self.Contrast_button.setObjectName("Contrast_button")
        self.verticalLayout_2.addWidget(self.Contrast_button)
        self.Saturate_edit = QtWidgets.QLineEdit(Dialog)
        self.Saturate_edit.setObjectName("Saturate_edit")
        self.verticalLayout_2.addWidget(self.Saturate_edit)
        self.Saturate_button = QtWidgets.QPushButton(Dialog)
        self.Saturate_button.setObjectName("Saturate_button")
        self.verticalLayout_2.addWidget(self.Saturate_button)
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_2.addWidget(self.progressBar)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "GUI photo editor"))
        self.button_input_path.setText(_translate("Dialog", "Add path to input photo"))
        self.button_output_path.setText(_translate("Dialog", "Add path to output directory"))
        self.Sepia_button.setText(_translate("Dialog", "Set sepia (default value: 1.0)"))
        self.Contrast_button.setText(_translate("Dialog", "Set contrast (default value: 1.0)"))
        self.Saturate_button.setText(_translate("Dialog", "Set saturate (default value: 1.0)"))

class App(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.sepia_level = 1.0
        self.contrast_level = 1.0
        self.saturate_level = 1.0
        self.button_input_path.clicked.connect(self.search_input_path)
        self.button_output_path.clicked.connect(self.search_output_path)
        self.Sepia_button.clicked.connect(self.set_sepia)
        self.Contrast_button.clicked.connect(self.set_contrast)
        self.Saturate_button.clicked.connect(self.set_saturate)
        self.buttonBox.accepted.connect(self.run)

    def accept(self):
        pass

    def search_input_path(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self, "Select path to photo")[0]
        self.Input_path.setText(path)

    def search_output_path(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "Output folder")
        self.Output_path.setText(path)

    def set_sepia(self):
        try:
            self.sepia_level = float(self.sepia_edit.text())
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Error", "Enter valid number")
    
    def set_contrast(self):
        try:
            self.contrast_level = float(self.Contrast_edit.text())
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Error", "Enter valid number")

    def set_saturate(self):
        try:
            self.saturate_level = float(self.Saturate_edit.text())
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Error", "Enter valid number")

    def run(self):
        input_path = self.Input_path.text()
        output_path = self.Output_path.text()

        if((not input_path) or (not output_path)):
            QtWidgets.QMessageBox.warning(self,"Error","Both paths needed")
            return

        tasks = [
            self.step1,
            self.step2,
            self.step3,
        ]

        self.progressBar.setMaximum(len(tasks))
        self.progressBar.setValue(0)

        for i, task in enumerate(tasks):
            task(input_path, output_path)
            self.progressBar.setValue(i + 1)
            QtWidgets.QApplication.processEvents()

    def step1(self, input_path, output_path):
        self.image = Image.open(str(input_path))
        filename = os.path.basename(str(input_path))
        name, ext = os.path.splitext(filename)
        filename = name + "_edit" + ext
        self.path_saved = str(os.path.join(str(output_path), filename))
    def step2(self, input_path, output_path):
        self.image = pilgram.css.sepia(self.image,self.sepia_level)
        self.image = pilgram.css.contrast(self.image,self.contrast_level)
        self.image = pilgram.css.saturate(self.image,self.saturate_level)
    def step3(self, input_path, output_path):
        self.image.save(str(self.path_saved))


def main():
    app2 = QtWidgets.QApplication(sys.argv)
    ui = App()
    ui.show()
    sys.exit(app2.exec())
    return 0


if(__name__ == "__main__"):
    main()
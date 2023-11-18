from PyQt5.QtWidgets import *
from PyQt5 import uic

import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

class MyGui(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("gui.ui", self)
        self.show()

        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(self.attach)
        self.pushButton_3.clicked.connect(self.send)
        self.pushButton_5.clicked.connect(self.clear)


        self.lineEdit_4.setText("587")
        self.lineEdit_2.setText("smtp.gmail.com")
        self.lineEdit.setText("abdallahfetyani2@gmail.com")
        self.lineEdit_3.setText("lwid cigv iqey zkkh")
        self.lineEdit_5.setText("fetyani123123@gmail.com")

        self.attachements = []

        
    
    def login(self):
        try:
            self.server = smtplib.SMTP(self.lineEdit_2.text(), self.lineEdit_4.text())
            self.server.ehlo()
            self.server.starttls()
            self.server.ehlo()
            self.server.login(self.lineEdit.text(), self.lineEdit_3.text().replace(" ", ""))

            self.lineEdit.setEnabled(False)
            self.lineEdit_2.setEnabled(False)
            self.lineEdit_3.setEnabled(False)
            self.lineEdit_4.setEnabled(False)
            self.pushButton.setEnabled(False)


            self.lineEdit_5.setEnabled(True)
            self.lineEdit_6.setEnabled(True)
            self.lineEdit_7.setEnabled(True)
            self.textEdit.setEnabled(True)
            self.pushButton_2.setEnabled(True)
            self.pushButton_3.setEnabled(True)
            self.pushButton_5.setEnabled(True) 
            
        except smtplib.SMTPAuthenticationError:
            message_box = QMessageBox()
            message_box.setWindowTitle("Error")
            message_box.setText("Invaild Login Information")
            message_box.exec_()

        except:
            message_box = QMessageBox()
            message_box.setWindowTitle("Error")
            message_box.setText("Login Failed Please Try Again")
            message_box.exec_()


    def clear(self):
        self.lineEdit_5.setText("")
        self.lineEdit_6.setText("")
        self.textEdit.setText("")
        self.label_8.setText("Attachments:")
        self.attachements = []

    def attach(self):
        options = QFileDialog.Options()
        filenames,_ = QFileDialog.getOpenFileNames(self,"Open File", "","All Files (*.*)", options=options)
        if filenames != []:
            for file in filenames:
                attachment = open(file, "rb")
                filename = file.split("/")[-1]

                p = MIMEBase('application', 'octet-stream')
                p.set_payload(attachment.read())
                encoders.encode_base64(p)
                p.add_header('Content-Disposition', f'attachment; filename={filename}')
                self.attachements.append(p)

                if not self.label_8.text().endswith(':'):
                    self.label_8.setText(self.label_8.text() + ",")
                self.label_8.setText(self.label_8.text() + " "+filename)

        
    def send(self):
        dialog = QMessageBox()
        dialog.setText("Do you want to send this email?")
        dialog.addButton(QPushButton("Yes"), QMessageBox.YesRole) # 0
        dialog.addButton(QPushButton("No"), QMessageBox.NoRole) # 1
        if dialog.exec_() == 0:
            try:
                self.msg = MIMEMultipart()
                for attachement in self.attachements:
                    self.msg.attach(attachement)
                if self.lineEdit_7.text() == "":
                    self.lineEdit_7.setText(self.lineEdit.text().split("@")[0])
                self.msg['From'] = formataddr((self.lineEdit_7.text(), self.lineEdit.text()))
                self.msg['To'] = self.lineEdit_5.text()
                self.msg['Subject'] = self.lineEdit_6.text()

                self.msg.attach(MIMEText(self.textEdit.toPlainText(), 'plain'))
                text = self.msg.as_string()

                self.server.sendmail(self.lineEdit.text(), self.lineEdit_5.text(), text)

                message_box = QMessageBox()
                message_box.setFixedSize(500, 200)
                message_box.setText("Email Sent")
                message_box.exec_()
            except Exception as e:
                message_box = QMessageBox()
                message_box.setFixedSize(500, 200)
                message_box.setText(str(e))
                message_box.exec_()
            

if __name__ == "__main__":
    app = QApplication([])
    window = MyGui()
    app.exec_()
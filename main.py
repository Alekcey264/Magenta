from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QRadioButton, QTextEdit, QPushButton, QMessageBox
import sys
from cbc import CipherBlockChaining
from cfb import CipherFeedBack
from ecb import ElectronicCodeBook
from ofb import OutputFeedBack
from magenta import Magenta

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(720, 480)

        self.key_label = QLabel('Ключ:')
        self.key_input = QLineEdit(self)
        self.key_input.setPlaceholderText('Введите ключ')
        self.key_length_label = QLabel('Длина ключа: 0')

        self.message_label = QLabel('Сообщение:')
        self.message_input = QLineEdit(self)
        self.message_input.setPlaceholderText('Введите сообщение 16')
        self.message_length_label = QLabel('Длина сообщения: 0')

        self.vector_label = QLabel('Нулевой вектор:')
        self.vector_input = QLineEdit(self)
        self.vector_input.setPlaceholderText('Введите начальный вектор для методов CBC, CFB, OFB')

        self.magenta = QRadioButton('Обычный режим шифрования', self)
        self.magenta.setChecked(True)
        self.cbc = QRadioButton('CBC', self)
        self.cfb = QRadioButton('CFB', self)
        self.ecb = QRadioButton('ECB', self)
        self.ofb = QRadioButton('OFB', self)

        self.encrypt_button = QPushButton('Начать работу', self)
        self.encrypt_button.clicked.connect(self.encrypt_message)

        self.result_textedit = QTextEdit(self)
        self.result_textedit.setReadOnly(True)

        self.radio_group = QVBoxLayout()
        self.radio_group.addWidget(self.magenta)
        self.radio_group.addWidget(self.cbc)
        self.radio_group.addWidget(self.cfb)
        self.radio_group.addWidget(self.ecb)
        self.radio_group.addWidget(self.ofb)

        layout = QVBoxLayout()
        layout.addWidget(self.key_label)
        layout.addWidget(self.key_input)
        layout.addWidget(self.key_length_label)
        layout.addWidget(self.message_label)
        layout.addWidget(self.message_input)
        layout.addWidget(self.message_length_label)
        layout.addWidget(self.vector_label)
        layout.addWidget(self.vector_input)
        layout.addLayout(self.radio_group)
        layout.addWidget(self.encrypt_button)
        layout.addWidget(self.result_textedit)

        self.setLayout(layout)

        self.key_input.textChanged.connect(self.update_key_length)
        self.message_input.textChanged.connect(self.update_message_length)

    def encrypt_message(self):
        key = self.key_input.text()
#Проверяем, что пользователь ввел ключ
        if not key:
            QMessageBox.warning(self, "Ошибка", "Введите ключ", QMessageBox.StandardButton.Ok)
            return
#Проверяем, что пользователь ввел сообщение        
        message = self.message_input.text()
        if not message:
            QMessageBox.warning(self, "Ошибка", "Введите сообщение", QMessageBox.StandardButton.Ok)
            return
        
        vector = self.vector_input.text()
        result_text = ""

        if self.magenta.isChecked():
#Проверяем, что пользователь ввел ключ корректной длины
            if len(key) not in [16, 24, 32]:
                QMessageBox.warning(self, "Ошибка", "Проверьте длину ключа", QMessageBox.StandardButton.Ok)
                return
#Проверяем, что пользователь ввел сообщение корректной длины
            if len(message) != 16:
                QMessageBox.warning(self, "Ошибка", "Проверьте длину сообщения", QMessageBox.StandardButton.Ok)
                return
            method = Magenta(key.encode())
            encoded_message = method.encode_block(message.encode())
            decoded_message = method.decode_block(encoded_message)
        elif self.cbc.isChecked():
#Проверяем, что пользователь ввел вектор
            if not vector:
                QMessageBox.warning(self, "Ошибка", "Введите вектор", QMessageBox.StandardButton.Ok)
                return
            method = CipherBlockChaining(key.encode(), vector.encode())
            encoded_message = method.encode(message.encode())
            decoded_message = method.decode(encoded_message)
        elif self.cfb.isChecked():
#Проверяем, что пользователь ввел вектор
            if not vector:
                QMessageBox.warning(self, "Ошибка", "Введите вектор", QMessageBox.StandardButton.Ok)
                return
            method = CipherFeedBack(key.encode(), vector.encode())
            encoded_message = method.encode(message.encode())
            decoded_message = method.decode(encoded_message)
        elif self.ecb.isChecked():
            method = ElectronicCodeBook(key.encode())
            encoded_message = method.encode(message.encode())
            decoded_message = method.decode(encoded_message)
        elif self.ofb.isChecked():
#Проверяем, что пользователь ввел вектор
            if not vector:
                QMessageBox.warning(self, "Ошибка", "Введите вектор", QMessageBox.StandardButton.Ok)
                return
            method = OutputFeedBack(key.encode(), vector.encode())
            encoded_message = method.encode(message.encode())
            decoded_message = method.decode(encoded_message)

        result_text += f"Обычный способ шифрования:\nСообщение: {message}\n"
        result_text += f"Зашифрованное сообщение: {encoded_message}\n"
        result_text += f"Расшифрованное сообщение: {decoded_message.decode('utf-8')}"
        self.result_textedit.setPlainText(result_text)

    def update_key_length(self):
        key_length = len(self.key_input.text())
        self.key_length_label.setText(f'Длина ключа: {key_length}')

    def update_message_length(self):
        message_length = len(self.message_input.text())
        self.message_length_label.setText(f'Длина сообщения: {message_length}')

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

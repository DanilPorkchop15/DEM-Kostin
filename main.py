import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from ui.main_window import MainWindow
from modules.database import Database
import traceback


def handle_exception(exc_type, exc_value, exc_traceback):
    print("".join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
    QApplication.quit()


def main():
    app = QApplication(sys.argv)

    try:
        db = Database()
        if not db.connect():
            QMessageBox.critical(None, "Ошибка", "Не удалось подключиться к базе данных")
            return 1

        window = MainWindow(db)
        window.show()
        return app.exec_()

    except Exception as e:
        QMessageBox.critical(None, "Ошибка", f"Ошибка при запуске: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
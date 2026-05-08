import sys
from PyQt6.QtWidgets import *


class Calorie(QMainWindow):
   # Основной класс приложения 'Счетчик калорий'
   # В версии 1.1 реализовано удаление строк в таблице

    def __init__(self):
        super().__init__()
        # Инициализация параметров главного окна
        self.setWindowTitle("Счетчик калорий v1.1")
        self.resize(500, 450)

        # Константные данные: справочник энергетической ценности продуктов
        self.food_library = {
            "Курица (вар.)": 113,
            "Рис (вар.)": 130,
            "Гречка": 110,
            "Яблоко": 52,
            "Творог": 97,
            "Яйцо (1 шт)": 75
        }

        # Список для хранения текущей сессии пользователя
        self.daily_log = []

        # Запуск построения интерфейса
        self.init_ui()

    def init_ui(self):
        """Метод инициализации графических компонентов (Layout Management)"""
        layout = QVBoxLayout()  # Основной вертикальный контейнер

        # Блок ввода данных
        input_row = QHBoxLayout()

        self.combo = QComboBox()
        self.combo.addItems(self.food_library.keys())

        self.weight_input = QLineEdit()
        self.weight_input.setPlaceholderText("Вес в граммах")

        btn_add = QPushButton("Добавить")
        # Связываем сигнал клика с методом добавления данных
        btn_add.clicked.connect(self.add_to_list)

        input_row.addWidget(self.combo)
        input_row.addWidget(self.weight_input)
        input_row.addWidget(btn_add)

        # Таблица отображения
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Продукт", "Вес (г)", "Ккал"])
        # Настройка поведения: выделение всей строки при клике (удобно для удаления)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        # Новые функции v1.1
        # Кнопка удаления для управления списком продуктов
        self.btn_delete = QPushButton("Удалить выбранную строку")
        self.btn_delete.clicked.connect(self.delete_entry)
        # Визуальное выделение деструктивного действия
        self.btn_delete.setStyleSheet("background-color: #ffcccc; color: #b30000; font-weight: bold;")

        # Информационная панель
        self.total_label = QLabel("Итого за день: 0 ккал")
        self.total_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-top: 10px;")

        # Компоновка всех элементов в главном окне
        layout.addLayout(input_row)
        layout.addWidget(self.table)
        layout.addWidget(self.btn_delete)
        layout.addWidget(self.total_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def add_to_list(self):
        # Логика валидации, расчета и добавления новой записи в лог
        name = self.combo.currentText()
        weight_text = self.weight_input.text()

        # Простая валидация на ввод числовых значений
        if weight_text.isdigit():
            weight = float(weight_text)
            cal_per_100 = self.food_library[name]
            # Математический расчет на основе данных словаря
            result_cal = round((cal_per_100 * weight) / 100, 1)

            # Обновление модели данных (списка)
            self.daily_log.append([name, weight, result_cal])
            # Принудительное обновление визуального представления
            self.update_view()
            self.weight_input.clear()

    def delete_entry(self):
        # Новая функциональность v1.1
        # Позволяет пользователю корректировать список, удаляя ошибочные записи

        # Определяем индекс выделенной строки в таблице
        selected_row = self.table.currentRow()

        if selected_row >= 0:
            # Удаляем элемент из модели данных по индексу
            self.daily_log.pop(selected_row)
            # Перерисовываем таблицу с учетом изменений
            self.update_view()
        else:
            # Обработка исключения: попытка удаления без выбора строки
            QMessageBox.warning(self, "Ошибка выбора", "Пожалуйста, выделите строку в таблице для удаления!")

    def update_view(self):
        #Метод синхронизации данных daily_log с виджетом QTableWidget
        self.table.setRowCount(len(self.daily_log))
        total_sum = 0

        # Цикл отрисовки данных и подсчета суммы
        for i, entry in enumerate(self.daily_log):
            self.table.setItem(i, 0, QTableWidgetItem(entry[0]))
            self.table.setItem(i, 1, QTableWidgetItem(str(entry[1])))
            self.table.setItem(i, 2, QTableWidgetItem(str(entry[2])))
            total_sum += entry[2]

        # Обновление финального итога в интерфейсе
        self.total_label.setText(f"Итого за день: {round(total_sum, 1)} ккал")


if __name__ == "__main__":
    # Точка входа в приложение
    app = QApplication(sys.argv)
    window = Calorie()
    window.show()
    sys.exit(app.exec())

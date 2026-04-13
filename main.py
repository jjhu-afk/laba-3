import sys
from PyQt6.QtWidgets import *

# Класс приложения, наследующий основной функционал окна из PyQt6
class Calorie(QMainWindow):
    def __init__(self):
        super().__init__()
        # Установка базовых параметров графического интерфейса
        self.setWindowTitle("Счетчик каллорий")
        self.resize(450, 400)

        # Библиотека продуктов (Название: Калории на 100г)
        # Использование словаря обеспечивает быстрый
        self.food_library = {
            "Курица (вар.)": 113,
            "Рис (вар.)": 130,
            "Гречка": 110,
            "Яблоко": 52,
            "Творог": 97,
            "Яйцо (1 шт)": 75
        }

        # Список для хранения объектов съеденного за текущую сессию
        self.daily_log = []

        # Инициализация компонентов интерфейса
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout() # Основной вертикальный контейнер

        # Верхняя панель ввода (горизонтальный ряд элементов)
        input_row = QHBoxLayout()

        self.combo = QComboBox()
        # Динамически загружаем ключи из словаря продуктов в выпадающий список
        self.combo.addItems(self.food_library.keys())

        self.weight_input = QLineEdit()
        self.weight_input.setPlaceholderText("Вес в граммах")

        btn_add = QPushButton("Добавить")
        # Привязка события нажатия кнопки к методу обработки логики
        btn_add.clicked.connect(self.add_to_list)

        # Сборка горизонтального ряда
        input_row.addWidget(self.combo)
        input_row.addWidget(self.weight_input)
        input_row.addWidget(btn_add)

        # Таблица отображения 3 колонки для детализации данных
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Продукт", "Вес (г)", "Ккал"])

        # Информационная метка для вывода итогов
        self.total_label = QLabel("Итого за день: 0 ккал")
        self.total_label.setStyleSheet("font-weight: bold; font-size: 14px;")

        # Добавление всех элементов и рядов в главный вертикальный контейнер
        layout.addLayout(input_row)
        layout.addWidget(self.table)
        layout.addWidget(self.total_label)

        # Настройка центрального виджета согласно архитектуре QMainWindow
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def add_to_list(self):
        # Расчет калорийности и валидация ввода
        name = self.combo.currentText()
        weight_text = self.weight_input.text()

        # Проверяем, что введено целое число
        if weight_text.isdigit():
            weight = float(weight_text)

            # Получение коэффициента из базы данных (словаря) и расчет по формуле
            cal_per_100 = self.food_library[name]
            result_cal = round((cal_per_100 * weight) / 100, 1)

            # Сохранение новой записи в оперативный список
            self.daily_log.append([name, weight, result_cal])

            # Синхронизация визуального представления с обновленными данными
            self.update_view()
            # Очистка поля ввода для удобства пользователя
            self.weight_input.clear()

    def update_view(self):
        # Обновление таблицы на экране и пересчет финальной суммы
        self.table.setRowCount(len(self.daily_log))
        total_sum = 0

        # Проходим по списку записей и заполняем ячейки таблицы
        for i, entry in enumerate(self.daily_log):
            self.table.setItem(i, 0, QTableWidgetItem(entry[0]))  # Продукт
            self.table.setItem(i, 1, QTableWidgetItem(str(entry[1])))  # Вес
            self.table.setItem(i, 2, QTableWidgetItem(str(entry[2])))  # Калории
            total_sum += entry[2]

        # Обновление текстового вывода итоговой суммы
        self.total_label.setText(f"Итого за день: {round(total_sum, 1)} ккал")


# Точка входа в приложение
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calorie()
    window.show()
    sys.exit(app.exec())
import pytest
from main import Calorie


@pytest.fixture
def app(qtbot):
    """Создание окна приложения для тестов"""
    window = Calorie()
    qtbot.addWidget(window)
    return window


def test_add_food(app):
    """Тест: Добавление продукта и расчет калорий"""
    # Выбираем Курицу (113 ккал)
    app.combo.setCurrentText("Курица (вар.)")
    app.weight_input.setText("200")
    app.add_to_list()

    # Проверяем расчет: (113 * 200) / 100 = 226
    assert app.daily_log[-1][2] == 226.0


def test_delete_row(app):
    """Тест: Удаление выбранной строки"""
    app.weight_input.setText("100")
    app.add_to_list()

    # Выделяем строку и удаляем
    app.table.selectRow(0)
    app.delete_entry()

    assert len(app.daily_log) == 0


def test_delete_functionality(app):
    """Проверка удаления выбранной строки и пересчета суммы"""
    app.weight_input.setText("100")
    app.add_to_list()

    app.table.selectRow(0)
    app.delete_entry()

    assert len(app.daily_log) == 0
    assert app.table.rowCount() == 0
    assert "Итого: 0.0 ккал" in app.total_label.text()


def test_invalid_input(app):
    """Проверка защиты от некорректного ввода веса (буквы вместо цифр)"""
    app.weight_input.setText("abc")
    app.add_to_list()

    assert len(app.daily_log) == 0


from typing import Dict, Any
from cl_ph_book import PhoneBook
import os


def event_loop() -> None:
    '''
    Ф-ция где запускается главный цикл, в котором 
    происходит управление приложением.
    '''

    # Запуск основного цикла
    while True:

        # Вывод "меню"
        answer: str = input(
            'Выберите необходимое действие:\n'
            '1 - Показать записи в справочнике\n'
            '2 - Добавить запись\n'
            '3 - Удалить запись\n'
            '4 - Редактировать запись\n'
            '5 - Поиск контактов\n'
            '0 - Выход\n'
            '-> '
        )
        os.system('cls' if os.name == 'nt' else 'clear')

        # Проверка ответа
        if answer == '0':
            break
        try:
            # Попытка запуска одного из методов класса
            button_dict.get(answer)()
        except TypeError:
            print(
                '\tВведена неверная команда!\n'
                '\tПопробуйте еще раз.\n'
                f'{"-" * 41}'
            )


def main() -> None:
    '''
    Главная ф-ция, отвечает за вызов основных циклов событий,
    а так же упрощает добавление дополнительного функционала
    в будущем.
    '''

    # Очистка экрана и вывод названия программы
    os.system('cls' if os.name == 'nt' else 'clear')
    print(
        '\tТелефонный справочник (v0.9)\n'
        f'{"-" * 45}'
    )

    # Запуск ф-ции в которой работает основной цикл
    event_loop()


if __name__ == '__main__':

    # Создание объекта класса "PhoneBook" и словаря с "кнопками"
    ph_bk: PhoneBook = PhoneBook()
    button_dict: Dict[str, Any] = {
        '1': ph_bk.show_contacts,
        '2': ph_bk.add_contact,
        '3': ph_bk.remove_contact,
        '4': ph_bk.edit_contact,
        '5': ph_bk.find_contact
    }

    # Запуск главной ф-ции
    main()

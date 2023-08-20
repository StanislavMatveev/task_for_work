from typing import Dict, List, Union
from math import ceil
from random import randint
import os
import json


class PhoneBook:
    '''
    Базовый класс, в котором реализованы все основные
    возможности телефонного справочника, такие как:
    - просмотр контактов;
    - добавление контакта;
    - удаление контакта;
    - редактирование характеристик контакта;
    - поиск по одной или более характеристикам.
    
    Для хранения данных контактов, создается JSON-файл
    по относительному пути "data/contacts.json".
    '''

    # Создание словаря имитирующего "кнопки"
    __char_dict: Dict[str, List[str]] = {
        '1': ['name', 'имени'],
        '2': ['surname', 'фамилии'],
        '3': ['desperation', 'отчества'],
        '4': ['organization', 'организации'],
        '5': ['work_number', 'рабочего телефона'],
        '6': ['personal_number', 'личного телефона']
    }

    def __init__(self) -> None:
        # Инициализация переменной для данных контактов и 
        # попытка подключения к существующему файлу с контактами
        self.__data_for_work: Dict[str, Dict[str, str]] = dict()
        self.__connect_to_file()

    def show_contacts(self, temp_data: Dict[str, Dict[str, str]] = None) -> None:
        '''
        Метод для отображения контактов постранично.
        Базовый вывод 3 контакта на страницу.
        По умолчанию выводит основной список контактов,
        если же передать в аргументы отсортированный словарь
        (например после поиска), то выведет уже контакты из
        переданного словаря.
        '''

        # Проверка есть ли контакты, если нету выход
        if self.__empty_contacts():
            return
        
        # Проверка был ли получен в аргументах отсортированный словарь,
        # если нет, установка для работы основного словаря с данными
        if not temp_data:
            temp_data: Dict[str, Dict[str, str]] = self.__data_for_work

        # Установка базового значения текущей страницы, 
        # базового сдвига и определение максимально возможного 
        # кол-ва страниц с учетом сдвига
        page: int = 1
        shift: int = 3
        max_page_count: int = ceil(len(temp_data) / shift)

        # Запуск цикла для имитации постраничной работы с контактами
        while True:

            # Вывод информации
            print(
                f'\tКонтакты, страница {page} из {max_page_count}\n'
                f'{"-" * 41}'
            )

            # Определение того, какие контакты должны быть выведенны
            # в соответсвии с текущей страницей и сдвигом, и проход
            # по ним циклом
            for elem_id in list(temp_data)[shift * (page - 1):shift * page]:

                # Вывод информации о контакте в терминал
                self.__output_contact_info(elem_id)
                print('-' * 41)

            # Вывод меню для перелистывания "страниц" или выхода в меню
            answer: str = input(
            'Выберите необходимое действие:\n' \
            '1 - Следующая страница\n' \
            '2 - Предыдущая страница\n' \
            '0 - Вернуться в меню\n' \
            '-> '
            )
            os.system('cls' if os.name == 'nt' else 'clear')

            # Проверка ответа
            if answer == '0':
                # Выход в меню
                break
            elif answer == '1' and page < max_page_count:
                # "Перелистывание" вправо
                page += 1
            elif answer == '2' and page > 1:
                # "Перелистывание" влево
                page -= 1
            elif answer in ('1', '2'):
                # Вывод сообщения что достигнут предел страниц
                print(
                    '  Запрашиваемой страницы не существует.\n'
                    f'{"-" * 41}'
                )
            else:
                # Вывод сообщения что введенная команда не верна
                print(
                    '\tВведена неверная команда!\n'
                    '\tПопробуйте еще раз.\n'
                    f'{"-" * 41}'
                )

    def add_contact(self) -> None:
        '''
        Метод для добавления контактов.
        Поочередно запрашивает характеристики контакта,
        присваивает случайный 4-х значный номер, заносит
        информацию в переменную и записывает данные в файл.
        '''

        # Вывод информационного сообщения и запрос информации о контакте
        print(
            '\tДобавление нового контакта\n'
            f'{"-" * 42}'
        )
        added_name: str = input('Введите имя: ')
        added_surname: str = input('Введите фамилию: ')
        added_desperation: str = input('Введите отчество: ')
        added_organization: str = input('Введите организацию: ')
        added_work_number: str = input('Введите рабочий телефон: ')
        added_personal_number: str = input('Введите личный телефон: ')
        os.system('cls' if os.name == 'nt' else 'clear')

        # Запуск цикла, для присвоения контакту при записи уникального идентификатора
        while True:

            # Генерация ключа
            gen_key: str = str(randint(1000, 9999))

            # Проверка нету ли аналогичного ключа, если нет, запись информации в переменную
            if not gen_key in self.__data_for_work:
                self.__data_for_work[gen_key] = {
                    self.__char_dict['1'][0]: added_name,
                    self.__char_dict['2'][0]: added_surname,
                    self.__char_dict['3'][0]: added_desperation,
                    self.__char_dict['4'][0]: added_organization,
                    self.__char_dict['5'][0]: added_work_number,
                    self.__char_dict['6'][0]: added_personal_number
                }
                break

        # Запись данных в файл и вывод информационного сообщения
        self.__write_data()
        print(
            '\tКонтакт успешно добавлен!\n'
            f'{"-" * 41}'
        )

    def remove_contact(self) -> None:
        '''
        Метод для удаления контакта.
        Запрашивает идентификатор, удаляет
        и записывает изменения в файл.
        '''

        # Проверка есть ли контакты, если нету выход
        if self.__empty_contacts():
            return
        
        # Запуск основного цикла для работы с идентификатором
        while True:

            # Вывод информации
            print(
                '\tУдаление контакта\n'
                f'{"-" * 33}'
            )

            # Запрос идентификатора
            contact_id: str = input(
                'Введите ID контакта, или\n'
                'введите 0 для возврата в меню\n'
                '-> '
            )
            os.system('cls' if os.name == 'nt' else 'clear')

            # Проверка ответа
            if contact_id == '0':
                # Выход в меню
                break
            if self.__data_for_work.get(contact_id):

                # Если идентификатор существующий, запуск вторичного цикла для удаления
                while True:

                    # Вывод информации об удаляемом контакте
                    print('-' * 41)
                    self.__output_contact_info(contact_id)
                    print('-' * 41)

                    # Запрос подтверждения удаления контакта
                    answer: str = input(
                        'Вы точно хотите удалить данный контакт?\n'
                        '1 - да | 2 - нет\n'
                        '-> '
                    )
                    os.system('cls' if os.name == 'nt' else 'clear')

                    # Проверка ответа
                    if answer == '1':

                        # Удаление контакта, запись изменений в файл и вывод информационного сообщения
                        self.__data_for_work.__delitem__(contact_id)
                        self.__write_data()
                        print(
                            '\t Контакт удален!\n'
                            f'{"-" * 33}'
                        )
                        return
                    
                    elif answer == '2':
                        # Выход в меню
                        return
                    
                    else:
                        # Вывод информационного сообщения об ошибке
                        print(
                            '\tВведена неверная команда!\n'
                            '\tПопробуйте еще раз.'
                        )
            else:
                # Вывод информационного сообщения об ошибке
                print(
                    'Такого контакта не существует!\n'
                    'Попробуйте еще раз.\n'
                    f'{"-" * 33}'
                )

    def edit_contact(self) -> None:
        '''
        Метод для редактирования данных контакта.
        Запрашивает идентификатор, запрашивает тип данных
        для изменнений, записывает изменения в файл.
        '''

        # Проверка есть ли контакты, если нету выход
        if self.__empty_contacts():
            return
        
        # Запуск основного цикла для работы с идентификатором
        while True:

            # Вывод информации
            print(
                '\tРедактирование контакта\n'
                f'{"-" * 39}'
            )

            # Запрос идентификатора
            contact_id: str = input(
                'Введите ID контакта, или\n'
                'введите 0 для возврата в меню\n'
                '-> '
            )
            os.system('cls' if os.name == 'nt' else 'clear')

            # Проверка ответа
            if contact_id == '0':
                # Выход в меню
                break

            if self.__data_for_work.get(contact_id):

                # Если идентификатор существующий, запуск вторичного цикла для редактирования
                while True:

                    # Вывод информации о редактируемом контакте
                    print('-' * 39)
                    self.__output_contact_info(contact_id)
                    print('-' * 39)

                    # Запрос какие именно данные необходимо отредактировать
                    answer: str = input(
                        'Выберите, что именно необходимо изменить:\n'
                        '1 - Имя\n'
                        '2 - Фамилия\n'
                        '3 - Отчество\n'
                        '4 - Организация\n'
                        '5 - Рабочий телефон\n'
                        '6 - Личный телефон\n'
                        '0 - Вернуться в меню\n'
                        '-> '
                    )
                    os.system('cls' if os.name == 'nt' else 'clear')

                    # Проверка ответа
                    if answer == '0':
                        # Выход в меню
                        return
                    
                    if answer in self.__char_dict:

                        # Изменение данных для выбранной характеристики
                        self.__data_for_work[contact_id][self.__char_dict[answer][0]] = input(
                            'Введите новые данные: '
                        )
                        os.system('cls' if os.name == 'nt' else 'clear')

                        # Запись данных и вывод информационного собщения
                        self.__write_data()
                        print('Данные успешно изменены!')

                    else:
                        # Вывод информационного сообщения об ошибке
                        print(
                            '\tВведена неверная команда!\n'
                            '\tПопробуйте еще раз.'
                        )
            else:
                # Вывод информационного сообщения об ошибке
                print(
                    'Такого контакта не существует!\n'
                    'Попробуйте еще раз.\n'
                    f'{"-" * 39}'
                )

    def find_contact(self) -> None:
        '''
        Метод для поиска данных контакта.
        Запрашивает одну или более характеристику для поиска,
        если были найдены результаты, выводит их в постраничном режиме.
        '''

        # Проверка есть ли контакты, если нету выход
        if self.__empty_contacts():
            return
        
        # Запуск основного цикла для работы с поиском
        while True:

            # Вывод информации
            print(
                '\tПоиск контактов\n'
                f'{"-" * 30}'
            )

            # Запрос одной или нескольких характеристик
            # по которым будет производится поиск
            answer: str = input(
                'По какой характеристике ищем?\n'
                'Введите одну или более характеристик,\n'
                'через запятую.\n'
                '1 - Имя\n'
                '2 - Фамилия\n'
                '3 - Отчество\n'
                '4 - Организация\n'
                '5 - Рабочий телефон\n'
                '6 - Личный телефон\n'
                '0 - Вернуться в меню\n'
                '-> '
            )
            os.system('cls' if os.name == 'nt' else 'clear')

            # Проверка ответа
            if answer == '0':
                # Выход в меню
                break

            # Создание списка ответом, если было передано больше одной характеристики
            answer_list: List[str] = [elem.strip() for elem in answer.split(',')]

            # Проверка есть ли данные характеристики среди стандартных
            if all(map(lambda elem: elem in self.__char_dict, answer_list)):

                # Создание словаря для временных данных
                temp_dict: Dict[str, Dict[str, str]] = dict()

                # Итерации по переданным характеристикам
                for char_elem in answer_list:

                    # Запрос значения для поиска относительно конкретной характеристики
                    obj_for_search: str = input(
                        f'Введите значение для {self.__char_dict[char_elem][1]}: '
                    ).lower()
                    os.system('cls' if os.name == 'nt' else 'clear')

                    # Поиск совпадение среди существующих контактов
                    for key, value in self.__data_for_work.items():

                        if value[self.__char_dict[char_elem][0]].lower() == obj_for_search:
                            # Если совпадение найдено, запись во временный словарь
                            temp_dict[key] = value

                # Проверка были ли найдены контакты подходящие условиям поиска
                if temp_dict:

                    # Сортировка по имени
                    temp_dict: Dict[str, Dict[str, str]] = dict(
                        sorted(
                        temp_dict.items(), key=lambda elem: elem[1].get('name', '').lower()
                        )
                    )

                    # Вызов метода для вывода в терминал в страничном режиме
                    self.show_contacts(temp_data=temp_dict)
                    break

                else:
                    # Вывод информационного сообщения об ошибке
                    print(
                        '     Контакты не найдены\n'
                        f'{"-" * 30}'
                    )

            else:
                # Вывод информационного сообщения об ошибке
                print(
                    '  Введена неверная команда!\n'
                    '  Попробуйте еще раз.\n'
                    f'{"-" * 30}'
                )

    def __connect_to_file(self) -> None:
        '''
        Скрытый метод для работы внутри класса.
        Создает директорию для хранения данных,
        если необходимо. Так же пытается подключится
        к существующему файлу с данными.
        '''

        # Проверка существует ли директория для
        # хранения данных, если нет, то создать
        if not os.path.exists('data'):
            os.mkdir('data')

        # Попытка подключения к существующему файлу с данными
        try:
            with open('data/contacts.json', 'r', encoding='utf-8') as contacts:
                self.__data_for_work: Dict[str, Dict[str, str]] = json.load(contacts)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            pass

    def __write_data(self) -> None:
        '''
        Скрытый метод для работы внутри класса.
        Сортирует и записывает данные в файл
        '''

        # Сортировка данных контактов по имени
        self.__data_for_work: Dict[str, Dict[str, str]] = dict(
            sorted(
            self.__data_for_work.items(), key=lambda elem: elem[1].get('name', '').lower()
            )
        )

        # Запись в файл
        with open('data/contacts.json', 'w', encoding='utf-8') as contacts:
            json.dump(self.__data_for_work, contacts, indent=4, ensure_ascii=False)

    def __output_contact_info(self, elem_id: str) -> None:
        '''
        Скрытый метод для работы внутри класса.
        Выводит информацию о контакте в терминал.
        На вход принимает идентивикатор контакта.
        '''

        # Запись данных контакта в переменную по его идентификатору
        elem: Dict[str, str] = self.__data_for_work.get(elem_id)

        # Если по идентификатору хранятся данные, запуск вывода
        if elem:

            # Вывод информации о контакте
            print(
                'ID: {el_id}'.format(
                el_id=elem_id
                )
            )
            print(
                'ФИО: {nm} {srnm} {dspr}'.format(
                nm=elem.get('name', ''),
                srnm=elem.get('surname', ''),
                dspr=elem.get('desperation', '')
                )
            )
            print(
                'Организация: {org}'.format(
                org=elem.get('organization', '')
                )
            )
            print(
                'Рабочий телефон: {wrk_num}'.format(
                wrk_num=elem.get('work_number', '')
                )
            )
            print(
                'Личный телефон: {prs_num}'.format(
                prs_num=elem.get('personal_number', '')
                )
            )
        else:
            # Вывод сообщения о проблеме с данными контакта
            print(f'Запись с ID - {elem_id} записана некорректно, проверьте файл.')

    def __empty_contacts(self) -> Union[None, bool]:
        '''
        Скрытый метод для работы внутри класса.
        Проверяет наличие контактов.
        '''

        # Если контакты не найдены выводит
        # сообщение и возвращает флаг True
        if not self.__data_for_work:
            print(
                '\tКонтакты отсутствуют!\n'
                f'{"-" * 37}'
            )
            return True

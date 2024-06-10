###   ПОДКЛЮЧЕНИЕ БИБЛИОТЕК

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QInputDialog ,QLineEdit, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QTextEdit, QListWidget
import json #Json файлы
import os   #библиотека os для работы с Операционной Системой (тут нужны файлы)





###   СОЗДАНИЕ ИНТЕРФЕЙСА

app = QApplication([])
notes_win = QWidget()

notes_win.setWindowTitle('Умные заметки')

#0
field_text = QTextEdit()

notes_GB = QGroupBox('Список заметок')
tags_GB = QGroupBox('Список тегов')

V = QVBoxLayout()
main_H = QHBoxLayout()

V.addWidget(notes_GB)
V.addWidget(tags_GB)

main_H.addWidget(field_text)
main_H.addLayout(V)

notes_win.setLayout(main_H)

#1
list_notes = QListWidget()

create_note_button = QPushButton('Создать заметку')
delete_note_button = QPushButton('Удалить заметку')
save_note_button = QPushButton('Сохранить заметки')

notes_GB_V = QVBoxLayout()
notes_GB_H = QHBoxLayout()

notes_GB_H.addWidget(create_note_button)
notes_GB_H.addWidget(delete_note_button)

notes_GB_V.addWidget(list_notes)
notes_GB_V.addLayout(notes_GB_H)
notes_GB_V.addWidget(save_note_button)

notes_GB.setLayout(notes_GB_V)

#2
list_tags = QListWidget()
field_tag = QLineEdit()

create_tag_button = QPushButton('Создать тег')
delete_tag_button = QPushButton('Удалить тег')
search_tag_button = QPushButton('Искать по тегу')

tag_GB_V = QVBoxLayout()
tag_GB_H = QHBoxLayout()

tag_GB_H.addWidget(create_tag_button)
tag_GB_H.addWidget(delete_tag_button)

tag_GB_V.addWidget(list_tags)
tag_GB_V.addWidget(field_tag)
tag_GB_V.addLayout(tag_GB_H)
tag_GB_V.addWidget(search_tag_button)

tags_GB.setLayout(tag_GB_V)






###   ФУНКЦИИ-ОБРАБОТЧИКИ СОБЫТИЙ (ДЛЯ КНОПОК И ДР.)

def show_note():   #показать заметку
    note_name = list_notes.selectedItems()[0].text()     #взяли название выбранной заметки из list_notes
    field_text.setText(notes[note_name]['text'])         #достали из словаря текст и вывели его в field_text
    list_tags.clear()                                    #очистили список тегов
    list_tags.addItems(notes[note_name]['tags'])         #достали из словаря теги и вывели в list_tags

def add_note():   #добавить заметку
    note_name,result = QInputDialog.getText(notes_win,'Добавление заметки.', 'Добавить заментку:') #спросили пользователя название заметки
    if result and note_name != '':       #если он нажал ок и название не пустое:
        notes[note_name]={                      #добавляем в словарь пустую заметку (с пустым текстом и тегами)
            'text':'',
            'tags':[]
        }
        list_notes.addItem(note_name)          #добавляем заметку на виджет list_notes

def add_tag():     #добавить тег
    tag_name = field_tag.text()                             #взяли название тега из линии ввода
    if len(list_notes.selectedItems()) > 0:                      #если есть выбранные заметки (длина списка > 0)
        note_name = list_notes.selectedItems()[0].text()               #берем название выбранной заметки
        notes[note_name]['tags'].append(tag_name)                      #добавляем новый тег в список тегов в словаре
        list_tags.addItem(tag_name)                                    #добавляем новый тег на список-виджет


def del_note():     #удалить заметку 
    if len(list_notes.selectedItems()) > 0:                   #если есть выбранные заметки (длина списка > 0)
        note_name = list_notes.selectedItems()[0].text()        #берем название выбранной заметки
        del notes[note_name]                                    #удаляем из словаря ее
        list_notes.clear()                                      
        field_text.clear()                                      #очищаем ВСЕ поля
        field_tag.clear()
        list_tags.clear()
        list_notes.addItems(notes)                              #выводим обновленный словарь заметок в list_notes

def del_tag():     #удалить тег
    if len(list_notes.selectedItems())*len(list_tags.selectedItems()) > 0: #если есть выбранные ЗАМЕТКИ И ТЕГИ (длина списков > 0)
        tag_name = list_tags.selectedItems()[0].text()            #берем название тега
        note_name = list_notes.selectedItems()[0].text()          #берем название заметки
        notes[note_name]['tags'].remove(tag_name)                 #из списка тегов этой заметки удаляем этот тег
        list_tags.clear()                                         #очищаем list_tags
        list_tags.addItems(notes[note_name]['tags'])              #выводим обновленный список тегов туда

def save_note():    #сохранить заметку
    with open('notes_data.json', 'w') as file:                    #открываем файл для записи
        json.dump(notes, file)                                        #записываем в него словарь заметок

def change_note():  #изменить заметку
    if len(list_notes.selectedItems()) > 0:                      #если есть выбранные заметки
        note_name = list_notes.selectedItems()[0].text()              #берем название заметки
        if note_name in notes:                                        #если оно есть в словаре заметок
            notes[note_name]['text']=field_text.toPlainText()         #сохраняем текст из поля ввода (field_text) в текст этой заметки в словаре


def search_tag():   #икать по тегу
        list_tags.clear()
        field_text.clear()         #очищаем все поля
        field_tag.clear()
        list_notes.clear()
        tag_name = field_tag.text()         #берем название тега
        if search_tag_button.text() == 'Искать по тегу' and tag_name  != '':      #если текст заметки 'Искать'
            #образуем отфильтрованный словарь заметки
            notes_filtered = {}                                        #создаем пустой словарь      
            for note_name in notes:                                    #перебираем все названия заметок. Для каждого:
                if tag_name in notes[note_name]['tags']:                   #если тег есть в списке тегов этой заметки
                    notes_filtered [note_name]  =  notes[note_name]             #добавляем заметку в отфильтрованный словарь
                  
            list_notes.addItems(notes_filtered)           #на список-виджет list_notes выводим отфильтрованные заметки
            search_tag_button.setText('Сбросить поиск')   #меняем текст кнопки на "Сбросить;

        else:                                                #Иначе (то есть текст кнопки - "Сбросить")
            list_notes.addItems(notes)                            #добавляем в список-виджет list_notes обычный словарь заметок
            search_tag_button.setText('Искать по тегу')           #текст кнопки меняем на "Искать"







###   ПОДПИСКИ НА СОБЫТИЯ

field_text.cursorPositionChanged.connect(change_note)    #когда редактировали текст заметки - запустить change_note

list_notes.itemClicked.connect(show_note)   #когда нажали по заметке - запустить show_note

create_note_button.clicked.connect(add_note)   #добавить заметку    
delete_note_button.clicked.connect(del_note)    #удалить заметку
save_note_button.clicked.connect(save_note)     #сохранить заметку

create_tag_button.clicked.connect(add_tag)      #добавить тег
delete_tag_button.clicked.connect(del_tag)      #удалить тег
search_tag_button.clicked.connect(search_tag)   #искать по тегу






###   СОЗДАНИЕ/ОТКРЫТИЕ ФАЙЛА С ЗАМЕТКАМИ notes_data.json

if os.path.isfile('notes_data.json'):   #если ФАЙЛ УЖЕ ЕСТЬ 
    with open('notes_data.json', 'r') as file:  #Открываем файл для чтения
        notes = json.load(file)                 #загружаем в notes
else:     #иначе (ТО ЕСТЬ ФАЙЛА НЕТ)
    notes = {          # создаем новый словарь-пример
        'О планетах':
            {
                'text':'Что если вод на марсе это признак жизни?',
                'tags':['Марс','гипотезы']
            },
        "О чёрных дырах":
            {
                "text":"Сингулярность на горизонте событий отсутствует",
                "tags":["черные дыры","факты"]
            },
        "Название заметки":
            {
                "text":'ТУТ ТЕКСТ ЗАМЕТКИ',
                "tags":['ТУТ','СПИСОК',"ТЕГОВ"]
            }
    }
    
    with open('notes_data.json', 'w') as file:   #открываем для записи (файл создаётся)
        json.dump(notes, file)                   #записываем в него словарь-пример

field_tag.setPlaceholderText('Введите тег...')  #setPlaceholderText
list_notes.addItems(notes)        #загружаем все заметки (старые или новые) в список-виджет










notes_win.show()
app.exec_()


### Hexlet tests and linter status:
[![Actions Status](https://github.com/ilia-rassolov/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/ilia-rassolov/python-project-83/actions)

[![Maintainability](https://api.codeclimate.com/v1/badges/ffa0f30f16b9baf237d7/maintainability)](https://codeclimate.com/github/ilia-rassolov/python-project-83/maintainability)

---

# Мой склад

### Это моё первое тестовое задание

Flask-приложение с использованием PostgreSQL. Имитирует простейший складской функционал

---

### Установка проекта 

##### Вы можете пользоваться готовым проектом в сети: https://python-project-83-j08w.onrender.com

##### Либо установить на PC:

Требования для установки: наличие CLI, CPython ^3.10 и PostgreSQL  

Скачайте проект, перейдите в директорию  

`git clone git@github.com:ilia-rassolov/python-project-83.git`  
`cd python-project-83`  

Переименуйте файл .env_example в .env и измените в нём данные конфигурации  
Например, укажите настройки Вашей PostgreSQL:  

`DATABASE_URL="postgresql://<имя пользователя>:<пароль пользователя>@localhost:5432/<имя сущ. базы данных>"`

Совершите сборку проекта, потом старт  
`make build`  
`make start`  

Перейдите по ссылке в терминале 

---

### Использование

Бизнес-логика:

При создании заказа проверяется наличие достаточного количества товара на складе.
Обновляется количество товара на складе при создании заказа (уменьшение доступного количества).
В случае недостаточного количества товара при заказе возвращается ошибка с соответствующим сообщением.

---
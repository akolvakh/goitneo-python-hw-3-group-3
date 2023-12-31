
# AUTHOR
- Anton Kolvakh
- Group 3
- a.kolvakh@outlook.com

# TODO
- next year validator
- optimization
- refactoring

# RUN
- you should be inside python bot directory
- to start python bot run **`python3 _main.py`**  in your terminal 
- or run **`_main.py`** via your IDE

# COMMANDS
1.  Команда  **`"hello"`**:
    -   Введення:  **`"hello"`**
    -   Вивід:  **`"How can I help you?"`**
2.  Команда  **`"add [ім'я] [номер телефону]"`.**:
    -   Введення:  **`"add John 1234567890"`**
    -   Вивід:  **`"Contact added."`**
3.  Команда  **`"change [ім'я] [новий номер телефону]"`.**:
    -   Введення:  **`"change John 0987654321"`**
    -   Вивід:  **`"Contact updated."`**  або повідомлення про помилку, якщо ім'я не знайдено
4.  Команда  **`"phone [ім'я]"`.**:
    -   Введення:  **`"phone John"`**
    -   Вивід:  **`[номер телефону]`**  або повідомлення про помилку, якщо ім'я не знайдено
5.  Команда  **`"all"`.**:
    -   Введення:  **`"all"`**
    -   Вивід: усі збережені контакти з номерами телефонів
6.  Команда  **`"save [ім'я файлу].pkl / none"`.**:
    -   Введення:  **`"save / save book.pkl"`**
    -   Вивід: Address book saved або повідомлення про помилку, якщо файл не знайдено
7.  Команда  **`"load [ім'я файлу].pkl / none"`.**:
    -   Введення:  **`"load / load book.pkl"`**
    -   Вивід: Address book loaded або повідомлення про помилку, якщо файл не знайдено
8.  Команда  **`"add-birthday [ім'я] [дата народження]"`** додає дату народження для вказаного контакту:
    -   Введення: **`"add-birthday Bonnie 12.10.2023"`**: 
    -   Вивід:  **`"Birthday added for NAME`** або повідомлення про помилку, якщо форма Дня Народження невірний
9.  Команда  **`"show-birthday"`** показує дату народження для вказаного контакту:
    -   Введення: **`"show-birthday Bonnie"`.**
    -   Вивід:  **`"Birthday for Bonnie: 12.12.2024"`**  або повідомлення про помилку, якщо недостатня кількість аргументів. **`"NAME does not exist in the address book."`** якщо імені немає у записній книжці.
10.  Команда  **`"close"`**  або  **`"exit"`.**:
    -   Введення: будь-яке з цих слів
    -   Вивід:  **`"Good bye!"`**  та завершення роботи бота
11.  Команда  **`"birthdays"`** показує дні народження, які відбудуться протягом наступного тижня:
    -   Введення: **`"birthdays"`**
    -   Вивід:  **`"Upcoming birthdays: Friday Bonnie"`**  або **`"No upcoming birthdays in the next week."`** якщо немає Днів Народження на цьому тижні.
12.  Відсутня або неправильна Команда:
    -   Введення: відсутня або неправильна команда
    -   Вивід:  **`"Invalid command."`** 

# TIPS
1. Якщо Ви хочете змінити день народження, то використайте команду **`"add-birthday"`**
2. Якщо Ви хочете використовувати дані з попередньої сесії, то не забудьте використати команду **`"save"`**
3. Якщо Ви хочете використати дані з іншого джерела (текстовий файл формату .pkl), то скористайтеся командою **`"load"`**
4. Формат вводу номеру телефону == **`"10 цифр [0502332384]"`**
5. Формат вводу Дня Народження == **`"DD.MM.YYY [12.10.2024]"`**


# ARCHITECTURE
## Structure
- imports
- classes definitions
- errors decorator
- commands handlers
- commands wrapper/router
- main as entrypoint
- client code -> main() call and bot init


## Classes
### Class "Field"
- Базовий клас для полів запису.

### Class "Name"
- Клас для зберігання імені контакту. 
- Обов'язкове поле.

### Class "Phone"
- Клас для зберігання номера телефону.
- Має валідацію формату (10 цифр).

### Class "Record"
- Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів.
- Додавання телефонів.
- Видалення телефонів.
- Редагування телефонів.
- Пошук телефону.

### Class "AddressBook"
- Клас для зберігання та управління записами.
- Додавання записів.
- Пошук записів за іменем.
- Видалення записів за іменем.

### Class "Birthday"
- Функція  `get_birthdays_per_week`  виводить імена іменинників у форматі:

```
Monday: Bill Gates, Jill Valentine
Friday: Kim Kardashian, Jan Koum
```
- Користувачів, у яких день народження був на вихідних, потрібно привітати в понеділок.
- Функція виводить користувачів з днями народження на тиждень вперед від поточного дня.
- Тиждень починається з понеділка.
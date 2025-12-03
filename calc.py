import os
import sys
import json
from decimal import Decimal, getcontext, InvalidOperation

getcontext().prec = 28

HISTORY_FILE = "calc_history.json"

OPERATIONS = {
    1: "+",
    2: "-",
    3: "÷",
    4: "×",
    5: "%"
}

history = []
last_result = None

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def format_number(num: Decimal):
    if num is None:
        return ""
    
    if num.is_infinite():
        return "Бесконечность"

    if num.is_nan():
        return "Ошибка"
    
    if num == 0:
        return "0"

    s = "{:f}".format(num)
    
    if '.' in s:
        s = s.rstrip('0').rstrip('.')
        
    return s

def get_decimal(prompt_text):
    while True:
        try:
            value = input(prompt_text)
            value = value.replace(",", ".")
            return Decimal(value)
        except (InvalidOperation, ValueError):
            print("Ошибка: Введите корректное число!")

def save_history():
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Ошибка при сохранении истории: {e}")

def load_history():
    global history
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    history = data
        except (IOError, json.JSONDecodeError):
            history = []

def show_history():
    print("\n--- История вычислений ---")
    if not history:
        print("История пуста.")
    else:
        for record in history:
            print(record)
    print("--------------------------\n")

def main():
    global last_result, history
    
    load_history()
    
    while True:
        clear_screen()
        if history:
            print("Последние действия:")
            print("\n".join(history[-3:]))
            print("-" * 20)
        
        if last_result is not None:
            print(f"Текущий результат в памяти: {format_number(last_result)}")

        print("""Выберите действие:
1 - Сложение (+)
2 - Вычитание (-)
3 - Деление (÷)
4 - Умножение (×)
5 - Процент от числа (%)
6 - Очистить память и историю
7 - Показать всю историю
0 - Выход""")
        
        try:
            choice = input("-> ")
            if not choice.isdigit():
                raise ValueError
            tip = int(choice)
        except ValueError:
            print("Ошибка: Введите число от 0 до 7")
            input("Нажмите Enter для продолжения...")
            continue

        if tip == 0:
            print("Выход из программы.")
            sys.exit()
            
        if tip == 7:
            show_history()
            input("Нажмите Enter, чтобы вернуться...")
            continue
            
        if tip == 6:
            last_result = None
            history = []
            save_history() # Сохраняем пустой список
            print("Память и история очищены.")
            input("Нажмите Enter...")
            continue

        if tip not in (1, 2, 3, 4, 5):
            print("Неверный выбор операции.")
            continue

        num1 = Decimal(0)
        
        if last_result is not None:
            ans = input(f"Использовать {format_number(last_result)} как первое число? (Enter - Да / n - Нет): ").lower()
            if ans == '' or ans == 'y' or ans == 'д':
                num1 = last_result
            else:
                num1 = get_decimal("Введите первое число: ")
        else:
            num1 = get_decimal("Введите первое число: ")

        num2 = get_decimal("Введите второе число: ")

        res = None
        error_msg = None
        
        try:
            if tip == 1:
                res = num1 + num2
            elif tip == 2:
                res = num1 - num2
            elif tip == 3:
                if num2 == 0:
                    error_msg = "Бесконечность"
                    res = Decimal('Infinity')
                else:
                    res = num1 / num2
            elif tip == 4:
                res = num1 * num2
            elif tip == 5:
                res = (num1 / Decimal(100)) * num2
        except Exception as e:
            error_msg = f"Ошибка вычислений: {e}"

        val1 = format_number(num1)
        val2 = format_number(num2)
        op_char = OPERATIONS[tip]
        
        if error_msg and error_msg != "Бесконечность":
            print(error_msg)
            input("Нажмите Enter...")
            continue

        if error_msg == "Бесконечность":
            res_str = "Бесконечность"
            log_entry = f"{val1} {op_char} {val2} = {res_str}"
            last_result = None
        else:
            res_str = format_number(res)
            log_entry = f"{val1} {op_char} {val2} = {res_str}"
            last_result = res

        history.append(log_entry)
        save_history()
        
        print(f"\nРезультат: {res_str}")
        input("\nНажмите Enter для продолжения...")

if __name__ == "__main__":
    main()
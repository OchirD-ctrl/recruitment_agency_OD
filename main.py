DATA_FILE = "candidates.txt"


def read_data(filename):
    data = []

    try:
        f = open(filename, "r", encoding="utf-8")
    except FileNotFoundError:
        print("Файл с данными не найден.")
        return data

    for line in f:
        parts = line.strip().split()
        if len(parts) != 11:
            continue

        try:
            record = [
                parts[0],                  # фамилия
                parts[1],                  # имя
                parts[2],                  # отчество
                parts[3],                  # пол
                int(parts[4]),              # год
                int(parts[5]),              # месяц
                int(parts[6]),              # день
                parts[7],                  # специальность
                int(parts[8]),              # стаж
                parts[9],                  # языки
                int(parts[10])              # оклад
            ]
            data.append(record)
        except ValueError:
            # если где-то число оказалось не числом — просто пропускается строка
            continue

    f.close()
    return data


def shaker_sort(arr, need_swap):
    left = 0
    right = len(arr) - 1

    while left < right:
        for i in range(left, right):
            if need_swap(arr[i], arr[i + 1]):
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
        right -= 1

        for i in range(right, left, -1):
            if need_swap(arr[i - 1], arr[i]):
                arr[i], arr[i - 1] = arr[i - 1], arr[i]
        left += 1


def print_list(arr):
    print("-" * 105)
    print(f"{'Фамилия':12} {'Имя':10} {'Пол':4} {'Спец.':15} {'Стаж':6} {'Оклад':10}")
    print("-" * 105)

    for r in arr:
        print(f"{r[0]:12} {r[1]:10} {r[3]:4} {r[7]:15} {r[8]:6} {r[10]:10}")

    print("-" * 105)


def show_all(data):
    temp = data.copy()

    def cmp(a, b):
        if a[7] != b[7]:
            return a[7] > b[7]      # специальность
        return a[0] > b[0]          # фамилия

    shaker_sort(temp, cmp)
    print_list(temp)

def show_by_specialty(data):
    spec = input("Введите специальность: ").strip()

    temp = []
    for r in data:
        if r[7] == spec:
            temp.append(r)

    if not temp:
        print("Нет соискателей по данной специальности.")
        return

    def cmp(a, b):
        if a[8] != b[8]:
            return a[8] < b[8]      # стаж по убыванию
        if a[3] != b[3]:
            return a[3] < b[3]      # пол (М > Ж)
        return a[0] > b[0]

    shaker_sort(temp, cmp)
    print_list(temp)


def filter_by_salary(data):
    try:
        n1 = int(input("Минимальный оклад: "))
        n2 = int(input("Максимальный оклад: "))
    except ValueError:
        print("Оклад должен быть числом.")
        return

    if n1 > n2:
        n1, n2 = n2, n1

    temp = []
    for r in data:
        if n1 <= r[10] <= n2:
            temp.append(r)

    if not temp:
        print("Подходящих записей нет.")
        return

    def cmp(a, b):
        if a[10] != b[10]:
            return a[10] < b[10]    # оклад по убыванию
        return a[0] > b[0]

    shaker_sort(temp, cmp)
    print_list(temp)


def menu():
    data = read_data(DATA_FILE)

    if not data:
        return

    while True:
        print("\nКАДРОВОЕ АГЕНТСТВО")
        print("1 — Все соискатели")
        print("2 — По специальности")
        print("3 — По диапазону окладов")
        print("0 — Выход")

        choice = input("Ваш выбор: ").strip()

        if choice == "1":
            show_all(data)
        elif choice == "2":
            show_by_specialty(data)
        elif choice == "3":
            filter_by_salary(data)
        elif choice == "0":
            print("Работа завершена.")
            break
        else:
            print("Неверный пункт меню.")


menu()

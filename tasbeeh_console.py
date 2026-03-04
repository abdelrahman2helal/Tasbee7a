import json

DATA_FILE = "tasbeeh_data.json"
SETTINGS_FILE = "settings.json"


def choose_language():
    print("Choose Language / اختر اللغة")
    print("1. English")
    print("2. العربية")
    ch = input(" >> ")
    if ch == "2":
        return "ar"
    return "en"


def text(lang, key):
    messages = {
        "menu_title": {
            "en": "--- Tasbeeh Counter Menu ---",
            "ar": "--- قائمة برنامج السبحة ---"
        },
        "menu_items": {
         "en": [
                "1. Click Mode",
                "2. Show All Records",
                "3. Show Total",
                "4. Number of Zikr Types",
                "5. Reset All",
                "6. Add Preset",
                "7. Change Language",
                "0. Exit"
            ],
         "ar": [
                "1. وضع العدّ",
                "2. عرض جميع البيانات",
                "3. عرض المجموع",
                "4. عدد الأذكار",
                "5. مسح الكل",
                "6. إضافة ذكر",
                "7. تغيير اللغة",
                "0. خروج"
            ]
        },
        "choose_zikr": {
            "en": "Choose Zikr:",
            "ar": "اختر الذكر:"
        },
        "click_help": {
            "en": "ENTER = +1 | number = +n | stop = finish",
            "ar": "ENTER = +1 | رقم = +n | stop = إنهاء"
        },
        "invalid": {
            "en": "Invalid input.",
            "ar": "اختيار غير صالح."
        },
        "total": {
            "en": "Total tasbeeh =",
            "ar": "مجموع التسبيحات ="
        },
        "types": {
            "en": "Zikr types =",
            "ar": "عدد الأذكار ="
        },
        "reset_done": {
            "en": "All data cleared.",
            "ar": "تم مسح جميع البيانات."
        },
        "goodbye": {
            "en": "Goodbye!",
            "ar": "مع السلامة!"
        }
    }
    return messages[key][lang]

def load_data():
    try:
        return json.load(open(DATA_FILE, "r"))
    except:
        return {}

def save_data(data):
    json.dump(data, open(DATA_FILE, "w"), indent=4)

def load_settings():
    try:
        return json.load(open(SETTINGS_FILE, "r"))
    except:
        default = {
            "language": choose_language(),
            "presets": ["Subhan Allah", "Alhamdulillah", "Allahu Akbar"]
        }
        save_settings(default)
        return default

def save_settings(settings):
    json.dump(settings, open(SETTINGS_FILE, "w"), indent=4)


def add_zikr_count(data, zikr, count):
    if zikr not in data:
        data[zikr] = 0
    data[zikr] += count
    return data

def reset_all(data):
    return {}

def get_total(data):
    total = 0
    for k in data:
        total += data[k]
    return total

def get_number_of_zikr_types(data):
    c = 0
    for k in data:
        c += 1
    return c

def print_all(data, lang):
    if data == {}:
        print(text(lang, "invalid"))
        return
    for k in data:
        print(k, ":", data[k])

def increment_once(count):
    return count + 1

def add_multiple(count, n):
    return count + n



def choose_zikr(lang, settings):
    print(text(lang, "choose_zikr"))
    presets = settings["presets"]

    for i in range(len(presets)):
        print(i + 1, presets[i])
    print(len(presets) + 1, "Custom")

    ch = input(">> ")

    if ch.isdigit():
        ch = int(ch)
        if 1 <= ch <= len(presets):
            return presets[ch - 1]
        elif ch == len(presets) + 1:
            return input("Enter zikr: ")

    return presets[0]

def click_mode(lang, zikr):
    print(text(lang, "click_help"))
    count = 0

    while True:
        user = input()
        if user == "stop":
            break
        if user == "":
            count = increment_once(count)
            print("Count:", count)
        elif user.isdigit():
            count = add_multiple(count, int(user))
            print("Count:", count)
        else:
            print(text(lang, "invalid"))

    return count



def show_menu(lang):
    print()
    print(text(lang, "menu_title"))
    for item in text(lang, "menu_items"):
        print(item)


def main():
    settings = load_settings()
    lang=settings["language"]
    data = load_data()

    while True:
        show_menu(lang)
        ch = input(">> ")

        if ch == "1":
            zikr = choose_zikr(lang, settings)
            added = click_mode(lang, zikr)
            data = add_zikr_count(data, zikr, added)
            save_data(data)

        elif ch == "2":
            print_all(data, lang)

        elif ch == "3":
            print(text(lang, "total"), get_total(data))

        elif ch == "4":
            print(text(lang, "types"), get_number_of_zikr_types(data))

        elif ch == "5":
            data = reset_all(data)
            save_data(data)
            print(text(lang, "reset_done"))

        elif ch == "6":
            settings["presets"].append(input("New zikr: "))
            save_settings(settings)

        elif ch == "7":
            settings["language"] = choose_language()
            save_settings(settings)
            lang = settings["language"]

        elif ch == "0":
            print(text(lang, "goodbye"))
            break

        else:
            print(text(lang, "invalid"))

main()
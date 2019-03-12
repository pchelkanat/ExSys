import json
from operator import itemgetter

filepath = "rules1.txt"


class Rule():
    def __init__(self, name, priority, conditions, acts):
        self.name = name
        self.priority = priority
        self.conditions = conditions
        self.acts = acts

    def __str__(self):
        return "%s, %s, %s, %s" % (self.name, self.priority, self.conditions, self.acts)

    def add_rule(self):
        name, priority, conditions = input().splitlines()
        return Rule(name, priority, conditions)

    def totxt(self):
        data = fromtxt(filepath)
        data.append(self.__dict__)
        with open(filepath, 'w+', encoding="utf-8") as file:
            file.write(json.dumps(data, ensure_ascii=False))

        return True


def fromtxt(filepath):
    file = open(filepath, 'r+', encoding="utf-8")
    raw = file.readline()
    if len(raw) > 0:
        data = json.loads(raw)
    else:
        data = []
    return data


def create_my_rules():
    templvl_normal = Rule("Определение нормального уровня температуры", 10, (35, 37.1),
                          json.dumps({"температура": "нормальная"}, ensure_ascii=False))
    templvl_medium = Rule("Определение среднего уровня температуры", 10, (37.1, 38.3),
                          json.dumps({"температура": "средняя"}, ensure_ascii=False))
    templvl_high = Rule("Определение высокого уровня температуры", 10, (38.3, 42),
                        json.dumps({"температура": "высокая"}, ensure_ascii=False))
    diag_healthy = Rule("Определение здорового диагноза", 10,
                        json.dumps({"начало": "нет", "температура": "нормальная"}, ensure_ascii=False),
                        json.dumps({"диагноз": "здоров"}, ensure_ascii=False))
    diag_orz = Rule("Определение ОРЗ", 10,
                    json.dumps({"начало": "постепенное", "температура": "средняя"}, ensure_ascii=False),
                    json.dumps({"диагноз": "ОРЗ"}, ensure_ascii=False))
    diag_flu = Rule("Определение гриппа", 10,
                    json.dumps({"начало": "лихорадочное", "температура": "высокая"}, ensure_ascii=False),
                    json.dumps({"диагноз": "грипп"}, ensure_ascii=False))
    diag_undedefine = Rule("Определение неопределенного диагноза", 9, None,
                           json.dumps({"диагноз": "не определен"}, ensure_ascii=False))

    templvl_normal.totxt()
    templvl_medium.totxt()
    templvl_high.totxt()
    diag_undedefine.totxt()
    diag_healthy.totxt()
    diag_orz.totxt()
    diag_flu.totxt()


def my_rules():
    rules = fromtxt(filepath)
    rules = sorted(rules, key=itemgetter('priority'), reverse=True)  # сортировка по приоритету
    # print(rules)
    arr_rules = []
    for rule in rules:
        arr_rules.append(Rule(rule['name'], rule['priority'], rule['conditions'], rule['acts']))
    return arr_rules


def solving(my_start, my_temp):
    arr_rules = my_rules()
    my_templvl = ""
    diag = ""
    output = "\n#################\nINPUT: начало %s, температура %s\n____________________" % (my_start, my_temp)
    for i in range(len(arr_rules)):  # проход по каждому правилу
        # print("Итерация %s:\n проход правила: %s" % (i, arr_rules[i]))
        output += "\nИтерация %s:\n проход правила: %s\n" % (i, arr_rules[i])

        act = json.loads(arr_rules[i].acts)
        if "температура" in act.keys():  # если в правиле действие-факт направлен на определение уровня температуры
            t1, t2 = arr_rules[i].conditions
            if my_temp >= t1 and my_temp < t2:
                my_templvl = act["температура"]
                # print("правило, удовлетворяющее цели: %s" % (arr_rules[i]))
                output += " правило, удовлетворяющее цели: %s\n" % (arr_rules[i])


        elif "диагноз" in act.keys():  # если в правиле действие-факт направлен на определение диагноза
            if arr_rules[
                i].conditions != None:  # неопределеный диагноз не имеет условий-фактов !по приоритету он в самом конце!
                start = json.loads(arr_rules[i].conditions)["начало"]
                templvl = json.loads(arr_rules[i].conditions)["температура"]
                if start == my_start and templvl == my_templvl:
                    diag = act["диагноз"]
                    # print(" правило, удовлетворяющее цели: %s" % (arr_rules[i]))
                    output += " правило, удовлетворяющее цели: %s\n" % (arr_rules[i])
                    break
            elif arr_rules[
                i].conditions == None:
                diag = act["диагноз"]
                # print(" правило, удовлетворяющее цели: %s" % (arr_rules[i])) #неопределенный диагноз
                output += " правило, удовлетворяющее цели: %s\n" % (arr_rules[i])

    with open("output.txt", 'a+', encoding="utf-8") as file:
        file.write(output)
    file.close()

    return "_____________________\nINPUT: начало %s, температура %s - %s\nOUTPUT: диагноз %s" % (
        my_start, my_temp, my_templvl, diag)


#create_my_rules()
print(solving("постепенное", 36.9))
print(solving("нет", 36.9))
print(solving("лихорадочное", 38.9))
print(solving("постепенное", 37.9))

"""
def input_data(self):
    print("Начало заболевания")
    start = input()
    print("Введите температуру")
    temp = int(input())
    return start, temp
"""

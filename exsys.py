import json
from operator import itemgetter

filepath = "rules1.txt"


class Rule():
    def __init__(self, name, priority, conditions, acts):
        self.name = name
        self.priority = priority
        self.conditions = conditions  # if
        self.acts = acts  # then

    def __str__(self):
        return "%s, %s, %s, %s" % (self.name, self.priority, self.conditions, self.acts)

    def totxt(self):
        data = fromtxt(filepath)
        data.append(self.__dict__)
        with open(filepath, 'w+', encoding="utf-8") as file:
            file.write(json.dumps(data, ensure_ascii=False))

        return True


class Fact():
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return "%s: %s" % (self.key, self.value)


def fromtxt(filepath):
    file = open(filepath, 'r+', encoding="utf-8")
    raw = file.readline()
    if len(raw) > 0:
        data = json.loads(raw)
    else:
        data = []
    return data


def to_code(string):
    code = "(" + string + ")"
    code = code.replace(",", ") and (")
    code = code.replace(";", " or ")
    return code


def create_my_rules():
    rules = []
    rules.append(Rule("Определение нормального уровня температуры", 10,
                      "$температура >= 35, $температура < 37.1",
                      json.dumps({"ур_темп": "нормальная"}, ensure_ascii=False)))
    rules.append(Rule("Определение среднего уровня температуры", 10,
                      "$температура >= 37.1, $температура < 38.3",
                      json.dumps({"ур_темп": "средняя"}, ensure_ascii=False)))
    rules.append(Rule("Определение высокого уровня температуры", 10,
                      "$температура >= 38.3, $температура <= 42",
                      json.dumps({"ур_темп": "высокая"}, ensure_ascii=False)))
    rules.append(Rule("Определение здорового диагноза", 10,
                      "$ур_темп == 'нормальная'",
                      json.dumps({"диагноз": "здоров"}, ensure_ascii=False)))
    rules.append(Rule("Определение ОРЗ", 10,
                      "$начало == 'постепенное', $ур_темп == 'средняя'",
                      json.dumps({"диагноз": "ОРЗ"}, ensure_ascii=False)))
    rules.append(Rule("Определение гриппа2", 10,
                      "$начало == 'лихорадочное', $ур_темп == 'высокая'",
                      json.dumps({"предиаг": "грипп2"}, ensure_ascii=False)))
    rules.append(Rule("Определение гриппа", 10,
                      "$предиаг == 'грипп2'",
                      json.dumps({"диагноз": "грипп3"}, ensure_ascii=False)))
    rules.append(Rule("Определение неопределенного диагноза", 9, "",
                      json.dumps({"диагноз": "не определен"}, ensure_ascii=False)))

    for rule in rules:
        rule.totxt()


def my_rules():
    rules = fromtxt(filepath)
    rules = sorted(rules, key=itemgetter('priority'), reverse=True)  # сортировка по приоритету
    # print(rules)
    arr_rules = []
    for rule in rules:
        arr_rules.append(Rule(rule['name'], rule['priority'], rule['conditions'], rule['acts']))
    return arr_rules


def input_data():
    facts = []
    while True:
        print("Введите факт в формате ключ-значение с каждой новой строки")
        key, value = input().split()
        if value.isdecimal():
            value = int(value)

        facts.append(Fact(key, value))

        print("Вы закончили?\n1. Да\n2. Нет")
        answer = int(input())
        if answer == 1:
            return facts
        else:
            continue


def solving(facts):
    arr_rules = my_rules()

    output = "\n###############\nСписок правил:\n"
    for rule in arr_rules:
        output += str(rule) + "\n"

    for i in range(len(arr_rules)):  # проход по каждому правилу
        fact_keys = [fact.key for fact in facts]  # ключи, которые есть. БУДУТ ДОПОЛНЯТЬСЯ
        fact_values = [fact.value for fact in facts]
        #print(fact_keys, fact_values)
        output += "\nИтерация %s:\n проход правила: %s\n" % (i, arr_rules[i])
        act = json.loads(arr_rules[i].acts)  # подгужаем действия из одного правила
        act_as_fact = ""
        for item in act:
            act_as_fact = Fact(item, act[item])  # представление действия, как факт
        # [print(fact) for fact in act_as_fact]
        if act_as_fact.key in fact_keys:  # если факт-действие уже есть, то прожолжаем
            output += " пропускаем, так как факт уже имеется\n"
            continue
        else:
            condition = arr_rules[i].conditions  # иначе, подгружаем условия
            # print(to_code(condition))
            if len(condition) == 0:
                facts.append(Fact(act_as_fact.key, act_as_fact.value))  # если условие пустое, то добавляем этот факт
                output += " правило удовлетворяет\n"
            else:
                for j in range(len(facts)):
                    #print(i, j, facts[j].key, facts[j].value)
                    if facts[j].key in condition:
                        if isinstance(facts[j].value, float):
                            condition = condition.replace("$" + facts[j].key, str(facts[j].value))
                        elif isinstance(facts[j].value, str):
                            condition = condition.replace("$" + facts[j].key, "'" + str(facts[j].value) + "'")
                code = to_code(condition)
                #print(code)
                if "$"in code:
                    continue
                elif eval(code):
                    facts.append(Fact(act_as_fact.key, act_as_fact.value))
                    output += " правило удовлетворяет\n"

        continue

    output += "\n###############\nСписок фактов:\n"
    for fact in facts:
        output += str(fact) + "\n"

    with open("output.txt", 'a+', encoding="utf-8") as file:
        file.write(output)
    file.close()


if __name__ == "__main__":
    #create_my_rules()
    # facts=input_data()

    facts = [Fact("температура", 37.2), Fact("начало", "постепенное")]
    solving(facts)

    facts = [Fact("температура", 34.2), Fact("начало", "постепенное")]
    solving(facts)

    facts = [Fact("температура", 37.2)]
    solving(facts)

    facts = [Fact("температура", 36.2)]
    solving(facts)

    facts = [Fact("температура", 39.5), Fact("начало", "лихорадочное")]
    solving(facts)

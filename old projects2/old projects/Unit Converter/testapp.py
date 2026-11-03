def main():
    units = {
    "millimeter": 1,
    "centimeter": 10,
    "meter": 1000,
    "kilometer": 1_000_000,
    "inch": 25.4,
    "foot": 304.8,
    "yard": 914.4,
    "mile": 1_609_344}
    if input("print convert ") == "convert":
        amount = int(input("amount "))
        base_unit = input("base_unit ")
        end_unit = input("end_unit ")
        value3 = 0
        value4 = 0
        for unit, value in units.items():
            if unit == end_unit:
                value3 = value
        for unit2, value2 in units.items():
            if unit2 == base_unit:
                value4 = value2
        result=amount*(value4/value3)
        print(result)
main()
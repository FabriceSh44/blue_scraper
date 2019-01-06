import re
import unicodedata
import pint

vulgars = {unicodedata.lookup("VULGAR FRACTION " + x[1]): x[0] for x in [(0.125, "ONE EIGHTH"),
                                                                         (0.2, "ONE FIFTH"),
                                                                         (0.25, "ONE QUARTER"),
                                                                         (0.33, "ONE THIRD"),
                                                                         (0.375, "THREE EIGHTHS"),
                                                                         (0.4, "TWO FIFTHS"),
                                                                         (0.5, "ONE HALF"),
                                                                         (0.6, "THREE FIFTHS"),
                                                                         (0.66, "TWO THIRDS"),
                                                                         (0.625, "FIVE EIGHTHS"),
                                                                         (0.75, "THREE QUARTERS"),
                                                                         (0.8, "FOUR FIFTHS"),
                                                                         (0.875, "SEVEN EIGHTHS")]}


def add_quantity(quantity_str_1, quantity_str_2, name):
    quantity1, suffix1 = parse_name_quantity(quantity_str_1)
    quantity2, suffix2 = parse_name_quantity(quantity_str_2)
    if suffix1 == suffix2:
        quantity_res_str = f'{quantity1+quantity2}{suffix1}'
    else:
        ureg = pint.UnitRegistry()
        unit1 = ureg.parse_units(suffix1)
        unit2 = ureg.parse_units(suffix2)
        quantity_res = unit1 * quantity2 + quantity1 * unit2
        quantity_res_str = f'{quantity_res.to(unit1).m}{unit1}'
    print(f'Merging {quantity_str_1} and {quantity_str_2} of {name} to [{quantity_res_str}]')
    return quantity_res_str


def parse_name_quantity(ingredient):
    pattern = r'^([\d\.]*)([^a-zA-Z]?)([a-zA-Z]*)$'
    r = re.search(pattern, ingredient)
    quantity_as_float = 0
    if r:
        groups = r.groups()
        quantity_as_float += float(groups[0]) if groups[0].strip() != '' else 0
        quantity_as_float += vulgars[groups[1]] if groups[1].strip() != '' else 0
        units = groups[2]
        return quantity_as_float, units
    raise Exception(f'Unable to parse {ingredient}')

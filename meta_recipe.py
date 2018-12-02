import re
from fractions import Fraction
import unicodedata

vulgars = {unicodedata.lookup("VULGAR FRACTION " + x[1]): x[0] for x in [(0.125, "ONE EIGHTH"),
                                                                         (0.2, "ONE FIFTH"),
                                                                         (0.25, "ONE QUARTER"),
                                                                         (0.375, "THREE EIGHTHS"),
                                                                         (0.4, "TWO FIFTHS"),
                                                                         (0.5, "ONE HALF"),
                                                                         (0.6, "THREE FIFTHS"),
                                                                         (0.625, "FIVE EIGHTHS"),
                                                                         (0.75, "THREE QUARTERS"),
                                                                         (0.8, "FOUR FIFTHS"),
                                                                         (0.875, "SEVEN EIGHTHS")]}


class MetaRecipe:
    def __init__(self) -> None:
        self.url = None
        self.ingredient_list = []
        self.servings = None

    def to_str(self, nb_serving):
        coeff = nb_serving / self.servings
        result = [self.url, f"Original serving : {self.servings:g}. Serving : {nb_serving}"]
        for ingredient in self.ingredient_list:
            result.append(self.apply_coeff(coeff, ingredient))

        return '\n'.join(result)

    def apply_coeff(self, coeff, ingredient):
        quantity, suffix = self.parse_quantity(ingredient[0])
        return f'{quantity * coeff:g}{suffix} {ingredient[1]}'

    def parse_quantity(self, ingredient):
        pattern = r'^([0-9]*)([^a-zA-Z]?)([a-zA-Z]*)$'
        r = re.search(pattern, ingredient)
        quantity_as_float = 0
        if r:
            groups = r.groups()
            quantity_as_float += float(groups[0]) if groups[0] != "" else 0
            quantity_as_float += vulgars[groups[1]] if groups[1] != "" else 0
            return (quantity_as_float, groups[2])
        raise Exception(f'Unable to parse {ingredient}')

from bs_parser import parse_name_quantity, add_quantity


class MetaRecipe:
    def __init__(self, category_dico) -> None:
        self.url_list = []
        self.ingredient_list = []
        self.ingredient_dico = {}
        self.category_dico = category_dico
        self.servings = None
        self.coeff = None

    def add_ingredient(self, name, quantity, apply_coeff=False):
        if apply_coeff:
            quantity_float, units = parse_name_quantity(quantity)
            quantity = f'{self.coeff* quantity_float:g}{units}'
        category = self.get_or_create_category(name)
        if name in self.ingredient_dico:
            self.ingredient_dico[name] = (category, add_quantity(self.ingredient_dico[name], quantity, name))
        else:
            self.ingredient_dico[name] = (category, quantity)

    def merge(self, other):
        self.url_list.append(other.url_list[0])
        for name, (category, quantity) in other.ingredient_dico.items():
            self.add_ingredient(name, quantity)

    def to_str(self):
        result = ['\n'.join(self.url_list),
                  f"Serving : {self.servings* self.coeff:g}"]
        list_ing = sorted(list(self.ingredient_dico.items()), key=lambda x: x[1][0])
        for name, (category, quantity) in list_ing:
            result.append(category + ">" + f'{quantity} {name}')
        return '\n'.join(result)

    def get_or_create_category(self, name):
        for category, name_list in self.category_dico.items():
            for ingredient in name_list:
                if ingredient in name.lower():
                    return category
        category_list = list(self.category_dico.keys())
        category_avali = '\n'.join([str(x) for x in zip(range(len(category_list)), category_list)])
        number = int(input(
            f'Unknown category for "{name}".\nWhich one do you want to assign ?\n{category_avali}\nYour choice : '))
        clean_name = input('Under which (clean) name?').lower()
        new_category = category_list[number]
        self.category_dico[new_category].append(clean_name.lower())
        print(f'Added [{clean_name}] to [{category_list[number]}]0')
        return new_category

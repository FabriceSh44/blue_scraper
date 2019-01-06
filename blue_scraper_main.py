#!/usr/bin/env python3
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from meta_recipe import MetaRecipe
import pyperclip
import argparse
import json


def simple_get(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    print(e)


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-number', help='number in recipe', type=int, default=4)
parser.add_argument('-url_list', nargs='+', help='url list')
parser.add_argument('-category_json', default='rsrc/ingredients.json', help='json path containing category definition')

args = parser.parse_args()

print(str.center('BLUE APRON SCRAPER', 80, '#'))
print(f'Loading file {args.category_json}')
with open(args.category_json, 'r') as fout:
    data = fout.read()
category_dico = json.loads(data)

print(f'Processing {len(args.url_list)} url(s) for {args.number} people(s)...')
meta_recipe_list = []
for url in args.url_list:
    raw_html = simple_get(url)
    html = BeautifulSoup(raw_html, 'html.parser')
    servings = float([x for x in html.find_all('span') if x.get('itemprop') == 'recipeYield'][0].contents[0])

    meta_recipe = MetaRecipe(category_dico)
    meta_recipe_list.append(meta_recipe)
    meta_recipe.url_list = [url]
    meta_recipe.servings = servings
    meta_recipe.coeff = args.number / servings

    for t in [x for x in html.find_all('li') if x.get('itemprop') == 'ingredients']:
        ingredient_lines = t.contents[1].contents
        quantity_str = ingredient_lines[1].contents[0].replace("\n", "")
        name = ingredient_lines[2].strip()
        meta_recipe.add_ingredient(name, quantity_str, apply_coeff = True)

print(f'Dumping {args.category_json}')
new_category_dico = {}
for category,list_el in category_dico.items():
    new_category_dico[category] = list(sorted(list(set(list_el))))
with open(args.category_json, 'w') as fout:
    fout.write(json.dumps(new_category_dico, indent=2))

for meta_recipe in meta_recipe_list[1:]:
    meta_recipe_list[0].merge(meta_recipe)

recipe_to_str = meta_recipe_list[0].to_str()
print(recipe_to_str)
pyperclip.copy(recipe_to_str)

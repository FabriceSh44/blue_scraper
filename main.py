from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from meta_recipe import MetaRecipe
import pyperclip


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


url = r"https://www.blueapron.com/recipes/panko-crusted-chicken-maple-dipping-sauce-with-roasted-brussels-sprouts-sweet-potatoes"
raw_html = simple_get(url)

html = BeautifulSoup(raw_html, 'html.parser')

servings = float([x for x in html.find_all('span') if x.get('itemprop') == 'recipeYield'][0].contents[0])

meta_recipe = MetaRecipe()
meta_recipe.url = url
meta_recipe.servings = servings

for t in [x for x in html.find_all('li') if x.get('itemprop') == 'ingredients']:
    ingredient_lines = t.contents[1].contents
    quantity = ingredient_lines[1].contents[0].replace("\n", "")
    name = ingredient_lines[2].strip()
    meta_recipe.ingredient_list.append([quantity, name])

print(meta_recipe.to_str(50))
pyperclip.copy(meta_recipe.to_str(50))

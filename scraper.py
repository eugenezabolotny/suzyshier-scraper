from bs4 import BeautifulSoup
import requests
import oembed
import json
import re

URL_BOTTOMS = 'https://suzyshier.com/collections/sz_bottoms_shop-all-bottoms'
URL_WEB_EXCLUSIVES = 'https://suzyshier.com/collections/sz_trend_online-exclusives'

result_data = {'bottoms': [], 'web_exclusives': []}
sale_list = {}


def get_oembed(url):
    """ Get oembed object, convert it to dict and get products list.

    :param url: string, page URL
    :return: list, list of products
    """
    consumer = oembed.OEmbedConsumer()
    endpoint = oembed.OEmbedEndpoint(url + '.oembed', ['https://suzyshier.com/*'])
    consumer.addEndpoint(endpoint)
    response = consumer.embed(url)
    return response.getData()['products']


def get_bottoms():
    """ Get data from 'bottoms' page and append to result dict.

    :return: null
    """
    for item in get_oembed(URL_BOTTOMS):
        # if any offered items of current product is in stock:
        if any([offer['in_stock'] for offer in item['offers']]):
            new_item = {
                'title': item['title'],
                'price': item['offers'][0]['price'],
                'colors': list({offer['title'].partition(' / ')[0] for offer in item['offers']}),
                'sizes': list({offer['title'].partition(' / ')[2] for offer in item['offers']}),
                'specs': [spec.replace('</li>', '').strip() for spec in
                          item['description'].split('<li>')[1:]],
                'description': item['description'].split('<li>', 1)[0].strip(),
            }
            result_data['bottoms'].append(new_item)


def get_web_exclusives():
    """ Get data from 'web exclusives' page and append to result dict.

    :return: null
    """
    for item in get_oembed(URL_WEB_EXCLUSIVES):
        # if any offered items of current product is in stock:
        if any([offer['in_stock'] for offer in item['offers']]):
            new_item = {
                'title': item['title'],
                'price': item['offers'][0]['price'],
            }
            # if product has discount price:
            if item['product_id'] in sale_list:
                new_item['discount_price'] = new_item['price']
                new_item['price'] = sale_list[item['product_id']]
            result_data['web_exclusives'].append(new_item)


def get_html(url):
    """ Get html page from URL and return it in text format. """
    r = requests.get(url)
    return r.text


def get_web_exclusives_sales():
    """ Get products with discount price from 'web exclusives' page
        and append it's id and discount price to special dict.

    :return: null
    """
    soup = BeautifulSoup(get_html(URL_WEB_EXCLUSIVES), 'lxml')
    sale_items = soup.find_all('div', {'data-promo-message': re.compile('"sale": true')})
    for item in sale_items:
        product_id = item \
            .find_next_sibling('div', {'class': 'selector-wrapper js product__option-selector'}) \
            .find('input').attrs['data-product-handle']
        product_price = item \
            .find_next_sibling('div', {'class': 'featured-collection__product-price'}) \
            .find('p', {'class': 'grid-item-compare'}).text.replace('$', '').strip()
        sale_list[product_id] = float(product_price)


def write_to_json():
    """ Writes result object to file. """
    with open('result.json', 'w') as fp:
        json.dump(result_data, fp, indent=4)


def main():
    """ lights, camera, action! """
    get_bottoms()
    get_web_exclusives_sales()
    get_web_exclusives()
    write_to_json()


if __name__ == '__main__':
    main()

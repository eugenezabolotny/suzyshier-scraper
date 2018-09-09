# Scraper of suzyshier-dot-com

## Goal

Parse data from the site [https://suzyshier.com/](https://suzyshier.com/)

Parsing algorithm:
- Open [https://suzyshier.com/collections/sz_shop-all](https://suzyshier.com/collections/sz_shop-all)
- Select BOTTOMS category and parse all closes followed data:
    - title
    - price
    - color
    - sizes
    - specs
    - description
- Select WEB EXCLUSIVES and parse data:
    - title
    - price
    - discount_price
- Save data in any format (JSON for example)

## Description

The app uses Python3 language, oEmbed and BeautifulSoup4 libs.
For getting product's information it uses [oEmbed](https://oembed.com/) file from site by `python-oembed` library, for getting discount price, that missing in oEmbed object, it uses scraping with `beautifulsoup4` library.

To take up the project:

```
$pip install -r requirements.txt
```

To run the app:

```
$python3 scraper.py
```

Results of scraping in `result.json`
# loonflow document
This is mult-language document, default language is English.

## quick start

### 1. install dependencies
```bash
cd sphinx_doc
pip install -r requirements.txt
```

### 2. build html
```bash

# get latest pot files
make gettext

# gen po files
make update-translations

# update po files

# build English document
make html
# build Chinese document
make html-zh

# review document
# English: open _build/html/index.html in browser
# Chinese: open _build/html-zh/index.html in browser
```






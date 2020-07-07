### 0.0.1

- initial commit from `wol_code_blog`

### 0.0.2

- added the following to `setup.py` to ensure non- py assets are included
    
```
    setup_requires=['setuptools_scm'],
    include_package_data=True
```

- https://stackoverflow.com/questions/1612733/including-non-python-files-with-setup-py

### 0.0.3

- moved `BrowserHeaders` to `weeblog.tools`
- now only rendering `pinned` and `links` if they are not empty
- not only creating and rendering `paginator` if `len(posts) > 1`

### 0.0.4

- added back try/catch protection to `weeblog.tools.watcher`

### 0.0.5

???

### 0.0.6

- add `tools/search_and_replace.py`
- watcher to watch `assets`
- rename `deploy/clean_app.py` as `deploy/clean_site.py`

### 0.0.7

- changed page title to make instapaper- friendly
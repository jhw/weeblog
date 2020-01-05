### sunvox 5/1/20

- https://www.warmplace.ru/soft/sunvox/jsplay/
- need hidden file `lib/sunvox.wasm`
- need to hack `application/wasm` mimetype -

```python
""" blog/tools/server.py """
extensions_map.update({
    '.wasm': 'application/wasm'
    })
```

```python
""" blog/aws/deploy_app.py """
def guess_content_type(filename):
    if filename.endswith(".wasm"):
        return "application/wasm"
    else:
        contenttype=mimetypes.guess_type(filename)[0]
        if not contenttype:
            contenttype="application/octet-stream"
        return contenttype
```
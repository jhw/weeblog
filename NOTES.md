### sunvox 14/1/20

- actually this may be way simpler
- just use different sunvox slots and load data into them at outset
- Sunvox.Load takes filename and slot
- is called initially to load data into slot
- then hello_world.js just needs to reference a particular slot position
- simples :-)

- maybe the only thing that can then be improved is the way playing songs are detected - is there a sunvox API to determine track status ? Could you save this state in localstorage ?
- can't find the API doc, but think things would be improved if current status was set in localstorage

### sunvox 14/1/20

- workflow
- slot 0 opened on loading `assets/js/lib/sunvox_play.js`
- same file defines Sunvox.start which takes a file reference, loads via AJAX and plays automatically (slot 0) on AJAX callback
- Sunvox.stop stops slot 0
- `demo/assets/js/posts/2020-01/hello_world.js` is then a wrapper around Sunvox module
- in particular it tracks song state via button state
- doesn't allow a song to be played if another song is playing; specifically it stops that song before starting the next one

- specifically to get around iOS problem, songs will have to be loaded into localstorage and played from there
- so will need Sunvox.load to accept a song or list of songs and load into locat storage
- separately, Sunbox.play will need to accept a filename and play from localstorage
- SVDemo will need an init() routine which not only does existing button binding, but also calls Sunvox.load
- you probably need the filenames as localstorage keys but maybe don't need the full filenames

- https://stackoverflow.com/questions/21008732/javascript-save-blob-to-localstorage
- https://gist.github.com/robnyman/1875344

### sunvox 14/1/20

- so current problem is that Sunvox.start (in weeblog/assets/js/) loads file using ajax and then immediately starts to play it
- this clearly isn't going to work with ios due to ajax restrictions
- solution probably involved splitting loading and playing, as loading into localstorage
- https://stackoverflow.com/questions/21008732/javascript-save-blob-to-localstorage
- https://gist.github.com/robnyman/1875344


### git tagging 5/1/20

- remember to update version in `setup.py` first!

- git tag -a 0.0.1
- [message is required]
- git tag -l [list local]
- git push origin 0.0.1
- git ls-remote --tags

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
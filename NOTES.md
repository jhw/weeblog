### meta properties

- https://ogp.me/
- https://www.w3schools.com/tags/tag_meta.asp

--

https://www.bbc.com/russian/features-53425651

<title>Допрос следователя, шифрование и интерес силовиков: главные подробности дела Сафронова - BBC News Русская служба</title>
<meta name="description" content="Мосгорсуд в четверг рассмотрит апелляцию на арест обвиняемого в госизмене бывшего журналиста и советника главы &quot;Роскосмоса&quot; Ивана Сафронова. Русская служба Би-би-си рассказывает, что известно об уголовном деле Сафронова к настоящему моменту.">
<meta property="og:title" content="Допрос следователя, шифрование и интерес силовиков: главные подробности дела Сафронова" />
<meta property="og:type" content="article" />
<meta property="og:description" content="Мосгорсуд в четверг рассмотрит апелляцию на арест обвиняемого в госизмене бывшего журналиста и советника главы &quot;Роскосмоса&quot; Ивана Сафронова. Русская служба Би-би-си рассказывает, что известно об уголовном деле Сафронова к настоящему моменту." />
<meta property="og:site_name" content="BBC News Русская служба" />
<meta property="og:locale" content="ru_RU" />
<meta property="article:author" content="https://www.facebook.com/bbcnews" />
<meta property="article:section" content="Подробности" />
<meta property="og:url" content="https://www.bbc.com/russian/features-53425651" />
<meta property="og:image" content="https://ichef.bbci.co.uk/news/1024/branded_russian/2833/production/_113419201_gettyimages-1225251775.jpg" />
<meta property="og:image:alt" content="BBC News Русская служба. Иван Сафронов" />

---

https://www.themoscowtimes.com/ru/2020/07/16/chislo-sluchaev-zarazheniya-koronavirusom-v-rossii-previsilo-750-tisyach-a117

<meta property="og:site_name" content="The Moscow Times in Russian"/>
<title>Число случаев заражения коронавирусом в России превысило 750 тысяч</title>
<meta name="keywords" content="коронавирус">
<meta name="news_keywords" content="коронавирус">
<meta name="description" content="Количество смертельных случаев превысило 11 тысяч ">
<meta name="thumbnail" content="https://static.themoscowtimes.com/ru/image/320/cb/510081.jpg">
<meta name="author" content="The Moscow Times in Russian">
<meta property="og:url" content="https://www.themoscowtimes.com/ru/2020/07/16/chislo-sluchaev-zarazheniya-koronavirusom-v-rossii-previsilo-750-tisyach-a117">
<meta property="og:title" content="Число случаев заражения коронавирусом в России превысило 750 тысяч">
<meta property="og:type" content="article">
<meta property="og:description" content="Количество смертельных случаев превысило 11 тысяч ">
<meta property="og:image" content="https://static.themoscowtimes.com/ru/image/1360/cb/510081.jpg">
<meta property="og:image:width" content="1360">
<meta property="og:image:height" content="765">
<meta property="article:author" content="The Moscow Times in Russian">
<meta property="article:content_tier" content="free">
<meta property="article:modified_time" content="2020-07-16T11:45:57+02:00">
<meta property="article:published_time" content="2020-07-16T09:30:00+02:00">
<meta property="article:publisher" content="https://www.facebook.com/MoscowTimes">
<meta property="article:section" content="news">
<meta property="article:tag" content="Коронавирус">

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
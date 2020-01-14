### short

- sunvox separate load/play to handle ios bug
  - or load assets on page load ?

### medium

- watcher doesn't appear to be watching `assets/js`

- full set of pre/postprocessor tests
- tools to use argsparse.py
- tools/search_and_replace.py

- twitter processor to remove widgets.js
- gist and tweet button alignment
- pinned links to use text colour from body
- script to clean bucket

### thoughts

- preprocessor to convert Google Keep punctuation ?
  - remove spaces before `?|!` ?
  - probably not worth it ?
- clean up linkrot ?
  - not worth it
- remove `links` key from pinned, links ?
  - no; jinja requires dict to be passed to sub- template
  - paginator is not the same as dict (prev, next) is passed
- favicon not rendering on localhost ?
  - seems to work fine in production :-/
- ensure `posts` not required in local assets ?
  - no you need this because you will be merging with weeblog assets

### done

- sunvox demo
- javascript table demo
- bump to 0.0.3
- extend README.md
- only show pinned, links if links exist
- moved browser headers to tools
- paginator fails when only one post

- pip package
- tagged deployent
- CHANGES.md
- refactor posts to include youtube, twitter embeds
- remove icons.yaml and importing into site builder
- add `config/icons.yaml`
- add watcher protection against site.yaml not found
- allow google to be optional
- check directories watched by watcher
- fix refs to blog in weeblog/aws
- updated notes
- check spellchecker, linkrot checker
- github project
- add logo to test local demo assets
- undo watcher exception handling
- check why watcher failing
- check app.props refs [no longer in config]
- move aws stuff back in weeblog
- rename REAMDE
- check for `blog` in Path
- demo
- test scripts
- run `test.py`
- add index.css to assets
- check `from blog` refs
- check `blog/` refs


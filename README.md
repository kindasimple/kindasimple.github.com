

Get a shell into the container
```
docker run --rm -it -w $PWD -v $PWD:$PWD -p4000:4000 -p35729:35729 jekyll/jekyll bash
```

bundle the gems in the Gemfile

```
bundle
```

Run jekyll
```
jekyll serve -w --drafts --config _config.yml,_config-dev.yml
```

In a separate terminal, open the browser to the site
```
open http://localhost:4000
```
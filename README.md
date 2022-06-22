# Bible Commentary

## Building locally

```console
$ sudo apt install ruby-dev
$ bundle install

$ bundle exec jekyll serve -H 0.0.0.0 -lw

$ chrome http://localhost:4000
```

## Docker
Alternatively, use Docker:

```console
$ docker run --rm --volume="$PWD:/srv/jekyll:Z" --publish 4000:4000 jekyll/jekyll:3.8 jekyll serve
```

Also use:

* `jekyll build` to build once
* `--volume="$PWD/vendor/bundle:/usr/local/bundle:Z"` to cache vendors

# Grab Framework Project

[![Grab Test Status](https://github.com/lorien/grab/actions/workflows/test.yml/badge.svg)](https://github.com/lorien/grab/actions/workflows/test.yml)
[![Code Quality](https://github.com/lorien/grab/actions/workflows/check.yml/badge.svg)](https://github.com/lorien/grab/actions/workflows/test.yml)
[![Type Check](https://github.com/lorien/grab/actions/workflows/mypy.yml/badge.svg)](https://github.com/lorien/grab/actions/workflows/mypy.yml)
[![Grab Test Coverage Status](https://coveralls.io/repos/github/lorien/grab/badge.svg)](https://coveralls.io/github/lorien/grab)
[![Pypi Downloads](https://img.shields.io/pypi/dw/grab?label=Downloads)](https://pypistats.org/packages/grab)
[![Grab Documentation](https://readthedocs.org/projects/grab/badge/?version=latest)](https://grab.readthedocs.io/en/latest/)

## Status of Project

I myself have not used Grab for many years. I am not sure it is being used by anybody at present time.
Nonetheless I decided to refactor the project, just for fun. I have annotated
whole code base with mypy type hints (in strict mode). Also the whole code base complies to
pylint and flake8 requirements. There are few exceptions: very large methods and classes with too many local
atributes and variables. I will refactor them eventually.

The current and the only network backend is [urllib3](https://github.com/urllib3/urllib3).

I have refactored a few components into external packages: [proxylist](https://github.com/lorien/proxylist),
[procstat](https://github.com/lorien/procstat), [selection](https://github.com/lorien/selection),
[unicodec](https://github.com/lorien/unicodec), [user\_agent](https://github.com/lorien/user_agent)

Feel free to give feedback in Telegram groups: [@grablab](https://t.me/grablab) and [@grablab\_ru](https://t.me/grablab_ru)

## Things to be done next

* Refactor source code to remove all pylint disable comments like:
    * too-many-instance-attributes
    * too-many-arguments
    * too-many-locals
    * too-nany-lines
    * too-many-public-methods
* Make 100% test coverage, it is about 90% now
* Release new version to pypi
* Refactor more components into external packages
* More abstract interfaces
* More data structures and types
* Decouple connections between internal components

## Installation

You need pythoon version >= 3.8

Run: `pip install -U grab`

See details about installing Grab on different platforms here https://grab.readthedocs.io/en/latest/usage/installation.html


## Documentation

Documenations is located here https://grab.readthedocs.io/en/latest/

Documentation for old Grab version 0.6.41 (released in 2018 year) is here https://grab.readthedocs.io/en/v0.6.41-doc/

## About Grab (very old description)

Grab is a python web scraping framework. Grab provides a number of helpful methods
to perform network requests, scrape websites and process the scraped content:

* Automatic cookies (session) support
* HTTPS/SOCKS proxy support with/without authentication
* Keep-Alive support
* IDN support
* Tools to work with web forms
* Easy multipart file uploading
* Flexible customization of HTTP requests
* Automatic charset detection
* Powerful API to extract data from DOM tree of HTML documents with XPATH queries

Grab provides an interface called Spider to develop multithreaded website scrapers:

* Rules and conventions to organize crawling logic
* Multiple parallel network requests
* Automatic processing of network errors (failed tasks go back to a task queue)
* You can create network requests and parse responses with Grab API (see above)
* Different backends for task queue (in-memory, redis, mongodb)
* Tools to debug and collect statistics

## Deprecated Usage Examples

Following examples were written many years ago. In those times many of websites could
be scraped with bare network and html libraries, without using browser engines. I guess
following examples do not work anymore.


## Grab Usage Example

```python
    import logging

    from grab import Grab

    logging.basicConfig(level=logging.DEBUG)

    g = Grab()

    g.request('https://github.com/login')
    g.doc.set_input('login', '****')
    g.doc.set_input('password', '****')
    g.doc.submit()

    g.doc.save('/tmp/x.html')

    g.doc('//ul[@id="user-links"]//button[contains(@class, "signout")]').assert_exists()

    home_url = g.doc('//a[contains(@class, "header-nav-link name")]/@href').text()
    repo_url = home_url + '?tab=repositories'

    g.request(repo_url)

    for elem in g.doc.select('//h3[@class="repo-list-name"]/a'):
        print('%s: %s' % (elem.text(),
                          g.make_url_absolute(elem.attr('href'))))
```

## Grab::Spider Usage Example

```python
    import logging

    from grab.spider import Spider, Task

    logging.basicConfig(level=logging.DEBUG)


    class ExampleSpider(Spider):
        def task_generator(self):
            for lang in 'python', 'ruby', 'perl':
                url = 'https://www.google.com/search?q=%s' % lang
                yield Task('search', url=url, lang=lang)

        def task_search(self, grab, task):
            print('%s: %s' % (task.lang,
                              grab.doc('//div[@class="s"]//cite').text()))


    bot = ExampleSpider(thread_number=2)
    bot.run()
```

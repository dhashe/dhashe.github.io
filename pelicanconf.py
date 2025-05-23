AUTHOR = "David Hashe"
SITENAME = "David Hashe | Personal website and blog"
SITEURL = ""

THEME = "theme"

PATH = "content"
PAGE_PATHS = ["pages"]
ARTICLE_PATHS = ["articles"]
STATIC_PATHS = ["images", "files", "extra/CNAME"]

TIMEZONE = "America/New_York"

DEFAULT_LANG = "en"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = ()

# Social widget
SOCIAL = (
    ("github", "https://github.com/dhashe"),
    ("linkedin", "https://www.linkedin.com/in/dhashe"),
    ("mastodon", "https://mastodon.social/@dhashe"),
    ("hackernews", "https://news.ycombinator.com/user?id=dhashe"),
)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

MARKDOWN = {
    "extension_configs": {
        "markdown.extensions.codehilite": {"css_class": "highlight"},
        "markdown.extensions.extra": {},
        "markdown.extensions.meta": {},
        "markdown.extensions.md_in_html": {},
        "markdown.extensions.toc": {
            "permalink": "#",
        },
    },
    "output_format": "html5",
}

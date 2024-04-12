AUTHOR = "David Hashe"
SITENAME = "David Hashe | Personal website and blog"
SITEURL = ""

PATH = "content"
PAGE_PATHS = ["pages"]
ARTICLE_PATHS = ["articles"]
STATIC_PATHS = ["images", "files"]

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
    },
    "output_format": "html5",
}

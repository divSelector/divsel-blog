from pathlib import Path
from sys import exit

# Theme-specific settings
SITENAME = 'divsel'
DOMAIN = 'divsel.neocities.org/blog'
ASSET_ROOT = '/blog/'
BIO_TEXT = 'Blog'
FOOTER_TEXT = 'This site is statically generated with Python.'

SITE_AUTHOR = 'div'
# TWITTER_USERNAME = ''
INDEX_DESCRIPTION = 'Latest posts by div'

GITHUB_URL = 'http://github.com/divSelector/'
SOCIAL_ICONS = [
    ('/blog/atom.xml', 'Atom Feed', 'fa-feed'),
    ('https://github.com/divSelector', 'GitHub', 'fa-github'),
    ('https://hackers.town/@shaen', 'Mastodon', 'fa-twitter'),
    ('https://divsel.neocities.org', 'Neocities', 'fa-share'),
]

#THEME_COLOR = '#FF8000'

# Pelican settings
RELATIVE_URLS = True
SITEURL = f'https://{DOMAIN}'
TIMEZONE = 'America/Chicago'
DEFAULT_DATE = 'fs'
DEFAULT_DATE_FORMAT = '%B %d, %Y'
DEFAULT_PAGINATION = False
SUMMARY_MAX_LENGTH = 42

# ARTICLE SAVES
ARTICLE_URL = '{date:%Y}/{date:%m}/{slug}/'
ARTICLE_SAVE_AS = ARTICLE_URL + 'index.html'

# PAGE SAVES
PAGE_URL = '{slug}/'

# ARCHIVE SAVES
ARCHIVES_SAVE_AS = 'archive/index.html'
YEAR_ARCHIVE_SAVE_AS = '{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = '{date:%Y}/{date:%m}/index.html'
TAG_SAVE_AS = 'tag/{slug}.html'
TAGS_SAVE_AS = 'tags/index.html'

# Disable authors, categories, tags, and category pages
DIRECT_TEMPLATES = ('index', 'archives', 'tags')

# Disable Atom feed generation
FEED_ATOM = 'atom.xml'
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

TYPOGRIFY = True

MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.admonition': {},
        'markdown.extensions.codehilite': {'linenums': None},
        'markdown.extensions.extra': {},
    },
    'output_format': 'html5',
}

CACHE_CONTENT = False
DELETE_OUTPUT_DIRECTORY = False

# TEMPLATES
templates = ['404.html']
TEMPLATE_PAGES = {page: page for page in templates}

extras = ['robots.txt', 'favicon.ico']
EXTRA_PATH_METADATA = {'extra/%s' % file: {'path': file} for file in extras}  # 'extra/robots.txt': {'path': 'robots.txt'},

# PLUGINS
PLUGIN_PATHS = ['plugins']
PLUGINS = ['assets', 'neighbors', 'optimize_images']

# ASSETS PLUGIN
ASSET_SOURCE_PATHS = ['static']
ASSET_CONFIG = [
    ('cache', False),
    ('manifest', False),
    ('url_expire', False),
    ('versions', False),
]

# EXCLUDES
PAGE_EXCLUDES = ['other', 'images']
ARTICLE_EXCLUDES = ['other', 'images']

GOOGLE_ANALYTICS = False

# PELICAN SETTINGS PATHS
OUTPUT_PATH = 'output'
PATH = 'content'
IMAGES_PATH = f'images'
ICONS_PATH = f'images/icons'
THEME = 'theme'
STATIC_PATHS = ['images', 'files', 'extra']
IGNORE_FILES = ['.DS_Store', 'pneumatic.scss', 'pygments.css', 'old_content', 'other']

MD_EXTENSIONS = ['codehilite(linenums=None)']
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.admonition': {},
        'markdown.extensions.codehilite': {'linenums': None},
        'markdown.extensions.extra': {},
    },
    'output_format': 'html5',
}

DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_PAGES_ON_MENU = False

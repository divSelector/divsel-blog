from pathlib import Path
from string import Template
from datetime import datetime
from jinja2.environment import Environment
from jinja2.filters import environmentfilter
from sys import exit
from typing import Any, Callable


class PostDate:
    def __init__(self, date=None):
        self.date = date if date is not None else datetime.now()
        self.modified = None
        self.output_meta_str = self.get_output_metadata_str()

    def __str__(self):
        return f"created: {self.format_datetime()}" if self.modified is None else \
            f"created: {self.format_datetime()}, modified: {self.format_datetime(self.modified)}"

    def __repr__(self):
        return self.__str__()

    def handle_modified_time(self, new_mod):
        """
        Pass the str "init" to clear modified time.
        Pass the str "now" to set new modified time to now.
        """
        new_mod = datetime.now() if new_mod == "now" else new_mod
        self.modified = None if new_mod == "init" else new_mod

    @staticmethod
    def _format_time(time):
        """
        Use format_datetime()
        """
        return "{:02d}:{:02d}".format(time.hour, time.minute)

    @staticmethod
    def _format_date(date):
        """
        Use format_datetime()
        """
        # return f"{date.year}-{date.month}-{date.day}"
        return "{:04d}-{:02d}-{:02d}".format(
            date.year, date.month, date.day
        )

    def format_datetime(self, mod_date=None):
        """
        To add a modified date, pass mod_date = self.modified
        """
        return f"{self._format_date(self.date.date())} {self._format_time(self.date.time())}" \
            if mod_date is None else f"{self._format_date(mod_date.date())} {self._format_time(mod_date.time())}"

    def get_output_metadata_str(self):
        d = f"Date: {self.format_datetime()}\n"
        return d if self.modified is None else \
            d + f"Modified: {self.format_datetime(self.modified)}"


class NewPost:
    DEFAULT_TITLE = "This needs a title"
    DEFAULT_AUTHOR = "shaenr"
    DEFAULT_STATUS = "published"  # "hidden" and "draft" are other options

    def __init__(self, file_path):
        """
        pass a file_path from pelicanconf: NEWPOST_FILE
        pass an author from pelicanconf: MY_DEFAULT_AUTHOR
        """
        self.path = file_path
        self.out_path = None
        self.raw_post_data = self._read_file_lines()
        self.metadata_lines = [line for line in self._read_metadata_lines().split('\n') if line]
        self.metadata = self.build_metadata_dict()
        self.content = "".join(self._read_content_lines())
        self.post_date = PostDate(
            self._get_key_else_get("Date")
        )  # Object for managing timestamps Use to output to self.date and self.modified

        self.title = self._get_key_else_get("Title", lambda *args: NewPost.DEFAULT_TITLE)
        self.date = self.post_date.format_datetime()
        self.modified = None
        self.tags = self._get_key_else_get("Tags")
        self.category = self._get_key_else_get("Category")
        self.slug = self._get_key_else_get("Slug", self.get_slug_from_title)
        self._authors = self._get_key_else_get("Authors")  # Do not use this value; use self.author
        self.author = self._get_key_else_get("Author", lambda *args: NewPost.DEFAULT_AUTHOR) \
            if self._authors is None else self._authors  # force self._authors to self.author if present

        self.summary = self._get_key_else_get("Summary")
        self.lang = self._get_key_else_get("Lang", lambda *args: "en")
        self.translation = self._get_key_else_get("Translation", lambda *args: "false")
        self.status = self._get_key_else_get("Status", lambda *args: NewPost.DEFAULT_STATUS)

        # Not Being Used
        # self.template = self._get_key_else_get("Template")
        # self.save_as = self._get_key_else_get("Save_as")
        # self.url = self._get_key_else_get("Url")
        # self.keywords = self._get_key_else_get("Keywords")

    def __str__(self):
        return f"NewPost: {self.path}"

    def __repr__(self):
        return self.__str__()

    def get_out_file_name(self):
        date, time = self.post_date.format_datetime().split()
        date_time = "".join(date.split('-') + time.split(':'))
        return f"{date_time}_{self.slug}.md"

    def _get_key_else_get(self, key: str, else_func: Callable[..., Any] = lambda *args: None) -> Any:
        """
        key should be the string for a key in self.metadata
        If it exists, it will return it... if it doesn't, it will use else_func to return another value
        The default else_func will return None.
        """
        return self.metadata[key] if else_func is not None and self.metadata.__contains__(key) else else_func(key)

    def add_modified_date(self):
        return self.post_date.format_datetime(self.post_date.modified)

    def get_slug_from_title(self, title):
        return "-".join(self.title.split()).lower() if self.title else ""

    def _read_file_lines(self):
        """
        Use self.raw_post_data
        Reads file in by lines. Returns raw information.
        """
        with self.path.open("r") as read_file:
            return read_file.readlines()

    def _read_metadata_lines(self, return_str=None):
        """
        Use self.metadata_lines
        Fines which lines are metadata lines from the total file lines.
        Uses the first empty space line to determine this
        """
        metadata = ""
        for line in self.raw_post_data:
            if line != '\n':
                metadata += line
            else:
                break
        return metadata

    def _read_content_lines(self):
        content = ""
        metadata_passed = False
        for line in self.raw_post_data:
            if metadata_passed:
                content += line
            elif not metadata_passed and not line == '\n':
                pass
            elif not metadata_passed and line == '\n':
                metadata_passed = True
        return content

    def build_metadata_dict(self, add_dict=None):
        """
        Initialized dict and splits each line by a colon to get the key and value from the markdown metadata
        In case there are colons in the value, each item after the first colon is joined by a colon to a string
        which is used as cleaned value.

        You can pass dict to add_dict to add these values to the metadata
        """
        d = {} if add_dict is None else add_dict
        for line in self.metadata_lines:
            colon_split_str = line.split(':')
            k = colon_split_str[0].strip()
            v = ":".join([
                string.strip() for string in colon_split_str[1:]
            ])
            d[k] = v
        return d

    def create_outfile(self):
        try:
            if self.out_path.exists():
                print("New Post file exists")
                exit()
            else:
                # shutil.copy(self.path, self.out_path)
                with self.out_path.open("w") as out_file:
                    out_file.write(self.post_date.output_meta_str)
                    out_file.write(
                        self.output_metadata_to_out_file()
                    )
                    out_file.write("\n" + self.content)
                self.path.unlink()
                self.path.touch()
        except ValueError:
            pass

    def output_metadata_to_out_file(self):
        metadata = ""
        for k, v in self.metadata.items():
            line = f"{k.capitalize()}: {v}\n"
            metadata += line
        return metadata


# GENERATE LINKS
class MenuLinks(dict):
    def __init__(self, ad):
        super().__init__(ad)
        self.elems = []
        self.attrs = ['text', 'href', 'rel']
        self.template_string = r'<a href="$href"$rel>$text</a>'
        self.posts = ad['markdown']['posts']
        self.external = ad['strings']['external']
        self.pages = ad['markdown']['pages']
        self.strings = ad['strings']['internal']
        self.sidebar_names = [f_name.stem for f_name in self.pages] + self.strings

        num_of_rels = len(self.sidebar_names)

        self.get_templated_elems([None for rel in range(num_of_rels)], self.sidebar_names, None)

    def print_attrs(self):
        return [self.elems, self.attrs, self.template_string, self.posts,
                self.external, self.pages, self.strings, self.sidebar_names]

    def get_templated_elems(self, rel_values, page_names, hrefs):
        """Assembly of anchor tags from markdown files and other strings via Template"""
        rels = [
            None for _ in range(len(page_names))
        ] if rel_values is None else rel_values

        print(page_names)
        print(rel_values)

        for page, r in zip(page_names, rels):
            text = page.title()
            if not page == 'blog':
                href = f" {page} ".replace(' ', '/')
            else:
                href = '/'
            rel = '' if r is None else f' rel="{r}"'

            temp = Template(self.template_string)
            elem = temp.safe_substitute(text=text, href=href, rel=rel)

            self.elems.append(elem)

    def sort_links(self):
        """A simple sort, could be more interesting"""
        first_items = []
        middle_items = []
        last_items = []
        print(f"sort links: {self.elems}")
        for elem in self.elems:
            if elem == '<a href="/archive/">Archive</a>':
                last_items.append(elem)
            elif elem == '<a href="/blog/">Home</a>':
                first_items.append(elem)
            else:
                middle_items.append(elem)

        concat_items = first_items + sorted(middle_items) + last_items
        assert len(concat_items) == len(self.elems)

        self.elems = concat_items
        return self.elems


# UTILS
def get_files_by_pattern(dir_path: Path, pattern: str = "*.md") -> list:
    return [f for f in dir_path.iterdir()
            if f.glob(pattern)
            and not f.is_dir()]


def get_new_post_file_paths_by_prefix():
    glob_str = f'{NEWPOST_INFILE_PREFIX}*'
    return [new_post_md for new_post_md
            in PROJECT_DIR.glob(glob_str)]


def check_posts():
    posts = [NewPost(post_path) for post_path in get_new_post_file_paths_by_prefix()]
    for p in posts:
        fname = p.get_out_file_name()
        p.out_path = CONTENT_DIR / fname
        p.create_outfile()


# CUSTOM FILTERS
@environmentfilter
def divide_iter(environment: Environment, inputs: list, n: int) -> zip:
    """Divides Items into Paired Tuples"""
    iters = [iter(inputs)] * n
    return zip(*iters)


# Theme-specific settings
SITENAME = 'shaenr'
DOMAIN = 'shaenr.github.io'
BIO_TEXT = 'Python/JavaScript<br>Command Line Cowboy<br>San Antonio, TX'
FOOTER_TEXT = 'This site is statically generated with Python.'

SITE_AUTHOR = 'shaenr'
# TWITTER_USERNAME = ''
INDEX_DESCRIPTION = 'Latest posts by python developer shaenr'

ICONS_PATH = 'images/icons'
GITHUB_URL = 'http://github.com/shaenr/'
SOCIAL_ICONS = [
    ('/atom.xml', 'Atom Feed', 'fa-feed'),
    ('https://github.com/shaenr', 'GitHub', 'fa-github'),
    ('https://hackers.town/@shaen', 'Mastodon', 'fa-mastodon'),
    ('https://divsel.neocities.org', 'Neocities', 'fa-share'),
]

#THEME_COLOR = '#FF8000'

# Pelican settings
RELATIVE_URLS = True
SITEURL = f'https://{DOMAIN}'
TIMEZONE = 'America/Chicago'
DEFAULT_DATE = 'fs'
DEFAULT_DATE_FORMAT = '%B %d, %Y'
DEFAULT_PAGINATION = True
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

# Disable authors, categories, tags, and category pages
# DIRECT_TEMPLATES = ['index', 'archives']
DIRECT_TEMPLATES = ('index', 'tags', 'categories', 'archives')

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
DELETE_OUTPUT_DIRECTORY = True

# TEMPLATES
templates = ['404.html']
TEMPLATE_PAGES = {page: page for page in templates}

extras = ['CNAME', 'favicon.ico', 'robots.txt']
EXTRA_PATH_METADATA = {'extra/%s' % file: {'path': file} for file in extras}  # understand this line

# PLUGINS
PLUGIN_PATHS = ['plugins']
PLUGINS = ['assets', 'neighbors', 'render_math']

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

JINJA_FILTERS = {'divide_iter': divide_iter}

GOOGLE_ANALYTICS = False

# PELICAN SETTINGS PATHS
OUTPUT_PATH = 'output'
PATH = 'content'
THEME = 'theme'
STATIC_PATHS = ['images', 'files', 'extra']
IGNORE_FILES = ['.DS_Store', 'pneumatic.scss', 'pygments.css', 'old_content', 'other']

# PATHLIB PATHS
PROJECT_DIR = Path(".")
CONTENT_DIR = PROJECT_DIR / PATH
PAGES_DIR = CONTENT_DIR / 'pages'
MD_EXTENSIONS = ['codehilite(linenums=None)']
NEWPOST_INFILE_PREFIX = PROJECT_DIR / "newpost_"

EXTERNAL_LINKS = [
    ('ProtonMail', 'https://www.protonmail.com', 'external'),
    ('hackers.town', 'https://www.hackers.town', 'external')
]

# AUTOMATE ADDING SIDEBAR LINKS
links = MenuLinks(
    {'markdown': {
        'posts': get_files_by_pattern(CONTENT_DIR),
        'pages': get_files_by_pattern(PAGES_DIR)},
        'strings': {
            'internal': ['archive'],
            'external': EXTERNAL_LINKS}})

links.elems.append('<a href="/">Home</a>')
links.sidebar_names.append('blog')

assert len(links.elems) % 2 == 0

SIDEBAR_LINKS = links.sort_links()

MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.admonition': {},
        'markdown.extensions.codehilite': {'linenums': None},
        'markdown.extensions.extra': {},
    },
    'output_format': 'html5',
}

DISPLAY_CATEGORIES_ON_MENU = True
DISPLAY_PAGES_ON_MENU = False

MENUITEMS = [
    ("Test", "https://www.duckduckgo.com")
]

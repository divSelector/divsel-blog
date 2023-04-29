Title: This Site Is Statically Generated
Date: 2023-04-28
Slug: pelican-static-site-generator
Tags: webdev, python

Back in March I talked about [dynamically rendering content on NeoCities pages using JavaScript]({filename}dynamic-render-neocities.md) and I suggested that the technique is probably inferior to other methods, one of which I said was static site generation. You might have noticed that at the bottom of these pages, there is a footer note that says "This site is statically generated with Python." Today we're going to look at how I do that using the [pelican python library](https://getpelican.com/).

## What is Static Site Generation

Static Site Generation is a website development approach that involves generating HTML, CSS, and JavaScript files locally on the developer's computer. Unlike dynamic sites that traditionally generate content on the server-side (or on the client-side with JS), static site generators prepare pre-built files that are directly served to the client in a fully rendered state, resulting in faster loading times, lower hosting costs, and improved security.

### What Are The Downsides?

1. Generating the site is done from command line, which is difficult for non-developers.
2. Configuring the site to look the way you want requires some experience with programming languages.
3. Working on the site with multiple people requires familiarity with version control systems, which is difficult for...

I think you get the idea. They're really cool, but they're not really easy to set up.

However once set up, adding new content is easier than ever.

## Download, Install and Build This Site

I'm not going to walk you through [quickstarting your own blog](https://getpelican.com/#quickstart) or [developing your own pelican theme](https://docs.getpelican.com/en/latest/themes.html), because you'd be much better off just reading the documentation if you wanted to do this.

Instead I'm going to walk you through installing my theme and my config. What you'll need to get started is python, git, and make. Technically, you also need sass, but I've handled that for you in an install script. 

### Download

```bash
git clone https://github.com/divSelector/divsel-blog.git
cd divsel-blog
```

### Install on Linux

```bash
bash install-linux.sh
```

While you can set all this up on Windows, I have not written an install script to do that yet.

### Build

```bash
. venv/bin/activate
make clean && make html
```

These commands will build the site in a new directory called `blog/`

### Serve

To test out the site, throw a local development server up with this command:

```bash
python -m http.server
```

Now you can navigate to [http://0.0.0.0:8000/blog/](http://0.0.0.0:8000/blog/) and have a look.

## Structure of the Codebase

Let's look at some of the important files and directories.

```bash
.
├── blog
├── content
│   ├── extra
│   ├── images
│   │   ├── icons
│   │   ├── responsive
│   │   └── retroarch
│   └── pages
├── plugins
├── theme
    ├── static
    └── templates
└── pelicanconf.py
```

### `blog`

As we just explained, the `blog` directory is created when we build the site. This is literally the folder that you upload to a web server so that people can view it.

### `plugins`

The `plugins` directory is where additional code used in the build process aside from the standard pelican code is kept. 

I might eventually show you my plugins, but you can mostly ignore what's in here if you don't understand it.

### `theme`

The `theme` directory contains two directories: 

1. `theme/static` is scss, css, and javascript that will be needed in the final output.
2. `theme/templates` is jinja2 html -- that is, they are otherwise normal HTML files except they contain special syntax that python uses to programatically render additional HTML.

If you're interested in learning about themes, you'll want to start with [learning jinja2](https://realpython.com/primer-on-jinja-templating/) and perhaps [developing your own pelican theme](https://docs.getpelican.com/en/latest/themes.html). That is kind of outside the scope of this little blog post, but there it is.

### `content`

Luckily, if you're feeling like stealing my config and theme to use with your own writing, the `content` directory is primarily what you're going to be interested in tinkering around with.

1. `content/extra` contains files that are going to be copied as-is into the root directory of `blog` on build.
2. `content/images` contains icons and directories of images to be used in blog posts. NOTE: Any images placed in here will be passed to `plugins/optimize_images.py`. As I mentioned above, I'll probably elaborate on this up in another blog post.
3. `content/pages` is an empty directory, but you could put markdown files inside of here if you wanted an about page, or a contact page, or something like that. I do not use this feature and currently the config is not even set up to support it.

And then it's just a list of markdown files. Each one of those markdown files is a blog post. If I wanted to add a new post, I would just add a new `.md` file and fill it out. If I wanted to remove some posts, I would remove them.
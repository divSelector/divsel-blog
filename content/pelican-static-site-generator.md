Title: This Site Is Statically Generated
Date: 2023-04-28
Slug: pelican-static-site-generator
Tags: webdev, python

Back in March I talked about [dynamically rendering content on NeoCities pages]({filename}dynamic-render-neocities.md) using JavaScript and I suggested that the technique is probably inferior to other methods, one of which I said was static site generation. You might have noticed that at the bottom of these pages, there is a footer note that says `This site is statically generated with Python.` Today we're going to look at how I do that using the [pelican python library](https://getpelican.com/).

## What is Static Site Generation

Static Site Generation is a website development approach that involves generating HTML, CSS, and JavaScript files locally on the developer's computer. Unlike dynamic sites that traditionally generate content on the server-side (or on the client-side with JS), static site generators prepare pre-built files that are directly served to the client in a fully rendered state, resulting in faster loading times, lower hosting costs, and improved security.

### What Are The Downsides?

1. Generating the site is done from command line, which is difficult for non-developers.
2. Configuring the site to look the way you want requires some experience with programming languages.
3. Working on the site with multiple people requires familiarity with version control systems, which is difficult for...

I think you get the idea. They're really cool, but they're not really easy to set up.

However once set up, adding new content is easier than it's ever been.

## Try Out My Config

I'm not going to walk you through [quickstarting your own blog](https://getpelican.com/#quickstart) or [developing your own pelican theme](https://docs.getpelican.com/en/latest/themes.html), because you'd be much better off just reading the documentation if you wanted to do this.

Instead I'm going to walk you through installing my theme and my config. What you'll need to get started is python, git, and make. That's it.

```bash
git clone https://github.com/divSelector/divsel-blog.git
cd divsel-blog
python3 -m pip install virtualenv
python3 -m virtualenv venv
. venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
make html
python -m http.server
```

Now you can navigate to [http://0.0.0.0:8000/blog/](http://0.0.0.0:8000/blog/) and have a look.
Title: Converting the Site to Pelican
Date: 2020-05-12
Slug: convert-pelican

Moving this page over to using Pelican has been a long time coming. Though it might appear that this is a first post, this GitHub page has already seen a few iterations.

Sometime last year, after spending a lot of time reading programming books, I set out to write my first real program, [simpai-spg](https://github.com/shaenr/simpai-spg/blob/master/old_version/simpai.py), which was supposed to be a simple static page generator written in python3. 

The primary motivation for writing it was that I had been working on a design [virulence.css]({static}other/virulence.html), which was a fork of [serenity.scss](https://hale.su/serenity.html), and ultimately, I couldn't figure out how to easily use it as a theme.

At the time, I didn't know what a templating engine was, let alone how to write jinja2. I suppose using Pelican seemed a lot more complicated to me than it needed to be. I felt like, "I already know HTML, I already know CSS, why do I have to learn this program to abstract away from it as much as possible?"

### Failings of Simpai

It wasn't as simple to assemble my content the way I imagined it would be. And though the first version worked, it truly was a "simple" page generator. It took the text from your post and inserted it into a page. It took every post and listed it with articles. The pagination worked in the end. And it was all strung together with `string.Template`.

The primary problem with the program was that... it could only generate one post at a time through an executable `new_post.py`, after which point, it would never be able to generate the page again. After that point, I started saving the data into json to solve this problem, but it was clearly going to become a very not-maintainable project upon getting bigger.

The end result of building simpai-spg was that, the moment I wanted to add some feature to my site design, the entire thing broke. I planned a new version each time I changed the design, and each time, the automated process of building the site broke. Eventually I stopped using it and I started updating pages manually. And very quickly after that, I quit writing posts, because they were no longer being automated into pages.


It was entirely too simple to be useful, but it taught me a lot.


### Two Things I Learned

You need to do better research before you begin a project.

1. There are libs out there that will solve the problem you have already. Search for them.
2. There are projects out there that have extensively covered the problem you have already. Use them before trying to improve them.

### Moving Forward

Looking back over virulence.css: While it may have taught me to write my own CSS without bootstrap, it was a kind of a huge mess. The fonts were overzealous and often clashing. The spacing and general typography settings were not very professional. The colors were pretty. And that's about what it had going for it.

Moving forward, we are using [Pelican](https://github.com/getpelican/pelican) and [pneumatic](https://github.com/iKevinY/pneumatic). It's possible that at some point I will give my own generator/theme another shot, but I won't be doing it until I've got a much better understanding of how this tool works, what its failings are, and what is worth taking the time to improve about it.

## Don't start from the bottom for the sake of it. 

Unless you have some fundamental lessons to learn, there's a better way.
That being said, there is no better way than failure to learn those fundamental things.

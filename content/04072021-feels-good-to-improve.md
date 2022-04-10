Title: Feels Good to Improve
Date: 04/07/2021
Status: Published
Slug: feels-good-to-improve

It's funny to look back on [this post](/2020/06/bbatch/) about "[bbatch](https://github.com/shaenr/bbatch)" now that I've been working on a better and more thorough solution after having long forgotten about that old script.

If you look back at that code, it was mostly about looking inside of directories, pulling out the files into a temporary root, comparing the file names and determining the namespaces, and attempting to remove as many duplicate files and unnecessary files as possible before renaming them to be better organized the next time.

But it was only able to remotely accomplish this goal if the circumstaanaces were exactly so. As a result, I ended up using it once, cleaning up a particular mess, and storing that project away to never be executed again.

I hadn't been thinking about this until I saw that page and remembered, but bbatch is basically the precursor to something I've been developing more recently that does more or less the same thing, but more systematically.

Let's look at both a little.

### The lines that kicked off bbatch

```py
def get_files_and_dirs(get_generator=False):
    if get_generator:
        dirs =  (d for d in PROOT.iterdir() if d.is_dir())
        files = (f for f in PROOT.iterdir() if f.is_file())
        return dirs, files
    else:
        dirs =  [d for d in PROOT.iterdir() if d.is_dir()]
        files = [f for f in PROOT.iterdir() if f.is_file()]
        if len(dirs) != 0:
            print(f'LENGTH OF DIRS: {len(dirs)}')
        print(f'LENGTH OF FILES: {len(files)}')
        return dirs, files
```

### The lines that kick off the new project

```py
def Main():
    ...
    conn = create_connection()
    with conn:
        try:
            create_files_table(conn)
        except Error:
            pass
        dirs = {
            f.name: Directory(f) 
            for f in Path.cwd().iterdir() 
            if f.is_dir()
        }
        files = {
            f.name: File(f) 
            for f in Path.cwd().iterdir() 
            if f.is_file()
        }
```

They're both more or less starting off the same way except in this new program, we have these thorough classes.

Here's part of one for example.

```py
class Directory(F):
    def init(self):
        self.files = {f.name: File(f) for f in self.path.iterdir() if f.is_file()}
        self.dirs = {f.name: f for f in self.path.iterdir() if f.is_dir()}
        self.symlinks = {f.name: f for f in self.path.iterdir() if f.is_symlink()}
        self.check_if_empty()
        ...
```

For every directory, we instantiate one of these, which results in a recursion through the entire file system as each file becomes processed not just for how it relates to some other files but everything about it I could ever need to know. All manner of factors will result in various methods like these: which will tell us many things about many different files.

```py
    def add_image_props(self):
        img = cv2.imread(self.path_str)
        self.img_height, self.img_width, self.img_channels = img.shape

    def add_vid_props(self):
        vid = cv2.VideoCapture(self.path_str)
        self.img_height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.img_width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.nframes = vid.get(cv2.CAP_PROP_FRAME_COUNT)
        self.fps = vid.get(cv2.CAP_PROP_FPS)
```

The other key difference is that in bbatch, the goal was to serialize the data (either into dicts or json) to do something with it later -- or to use it immediately for a specific task that was the only task it was fit to accomplish.

The biggest improvement by far is that, if you noticed, in the new solution, we begin with `conn = create_connection()`, which means that were are recording everything into a relational database, where we will be able to process and determine many things about these files for (hopefully) years to come.

## Right now its called Toshiorg.

Its named after a Toshiba drive that needs to be analyzed for what can be done with its contents. The project is moving along well but I don't yet have it on a public repository.

I didn't even plan on writing about it, but it was so crazy to see I had been trying to solve the same problem back a year ago, except I had really not solved that problem very well.

That is not to say that Toshiorg doesn't have its issues to be worked out but already it is more capable of doing everything that bbatch could ever do again and again in any context.

It's good to see that I've been improving.

### I'm not ready to show of Toshiorg...

This is mainly because, while it does work, there are features that are not ready and much of what is done can be cleaned out, so that what the code is doing is easier to read. I would prefer to get to that point before I share it here.

But fuck it. [Here's a repo.](https://github.com/shaenr/toshiorg/tree/main/app)

I can't promise you'll be able to make sense of it in this state. You'll notice there is an sql table and a django ORM table. I'm trying to replace one with the other -- the Django one doesn't work yet. That's just an experiment. The SQL written table does work though -- to some effect.

The most messy file of all is probably `main.py` so good luck. But if you can figure out what is important and what needs to be refactored out on your own, you'll see its so much better than the 'bbatch' from my older post..

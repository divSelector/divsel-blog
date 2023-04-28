Title: Fun with Retroarch on Linux
Date: 2023-03-23
Slug: retroarch-linux
Tags: retroarch, linux, emulation, video games
  
[Retroarch](https://www.retroarch.com/) is a frontend for emulators. It basically merges multiple systems into a customizable interface with unified settings. I'm going to show you how I build and configure my classic game box and we'll look at the scripts I use to get roms onto it.  By the end we will have a complete collection of games, thumbnails, screenshots, and database info about every game ever released for multiple classic gaming consoles. Then we'll do some other fun things like organizing a random game picker.

BTW, I am not affiliated with RetroArch.

## Building from Source

RetroArch supports recording game footage in real-time using libavcodec, but in order to do so, it requires a very current version of FFmpeg, which means that we have to build Retroarch, FFmpeg, and all its dependencies from source in order to use them. If you're not interested in using the recording feature, you can skip this step and simply [download](https://www.retroarch.com/?page=platforms) RA.

The following script is a robust compilation of suggestions from both [the libretro docs on Recording and Streaming](https://docs.libretro.com/guides/recording-and-streaming/) and the [FFmpeg compilation for Ubuntu guide](https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu).

With that in mind, I am assuming that you are doing this from an Ubuntu system, although it should work on other Debian based systems with `apt`.

I recommend taking a look at [the build script](https://github.com/divSelector/ra-sh/blob/main/build.sh). When you're satisfied that it's not going to hack your Gibson, just run it.

### build.sh

```bash
SCRIPT="https://raw.githubusercontent.com/divSelector/ra-sh/main/build.sh"
curl "$SCRIPT" > build.sh
sudo bash build.sh
```

It will take a while for it to build. When it's finished, test that it worked with `retroarch`.

Right. So I know that I promised there would be fun with Retroarch on Linux and we started with building software and dependencies from source. I'm deeply sorry about that, but this next part will be better.


## The No-Intro Rom Set from Internet Archive

### No-Intro

[No-Intro](https://no-intro.org/) catalogs the best available copies of ROMs and digital games, providing DAT files for ROM managers and an online database. A lot of work went into organizing this information so that if we have our roms organized and named by certain conventions, we will be able to just say, "Download all the thumbnails, screenshots, and database information about these roms please"

[![RetroArch Game Library with Thumbnails and Screenshots]({static}/images/retroarch/0.webp)]({static}/images/retroarch/0.png)

You might be noticing that yours looks nothing like mine, but don't worry. We're going to get there.

---

### Internet Archive

In order for this work, we can't just source our roms individually from some weird piracy site. We need a library -- a site with a ["DMCA Exemption To Help Archive Vintage Software"](https://archive.org/about/dmca.php) -- a library that is familiar with the structure of the No-Intro data. And there's only one site like that that I know of: [archive.org](archive.org)

Specifically, I like to pull from [no-intro_romsets on archive.org](https://archive.org/details/no-intro_romsets). There are plenty of archives on the site that contain these roms, but this is the one I like to go to first because it's the one that the most number of people are using and it has pretty much every cartridge based system.

[![No-Intro Romset on Internet Archive]({static}/images/retroarch/1.webp)]({static}/images/retroarch/1.png)

As you can see, it's a lot of stuff. And as you might imagine, a lot of bandwidth is used providing this service. That's why you can see the little lock icon to the right in the image. You won't be able to download these unless you make a free Internet Archive account. For some, this might be too much effort, but I think it's easy and completely worth it.

### Batch Downloading

Once you have made an account and are logged in, you can start downloading. I'm going to show you how to do it from command line, although you can do it however you'd like.

- **Install `internetarchive`**

```bash
sudo apt install internetarchive
```

This is going to let us use the command `ia`.

- **Login using `ia configure`**

```bash
$ ia configure
Enter your Archive.org credentials below to configure 'ia'.

Email address: youraccount@whatever.com
Password: 

Config saved to: /home/you/.config/internetarchive/ia.ini
```

Something like this is what you should see.

- **View Contents of Archive**

```bash
ia list no-intro_romsets
```

- **Glob Specific Contents from Archive**

It's going to be a lot of stuff. While you could download all of it, I prefer to just add one system at a time.

```bash
$ ia list no-intro_romsets --glob "*Super Nintendo*"                     
no-intro romsets/Nintendo - Super Nintendo Entertainment System (20230318-120602).zip
```

Now you should only see files that contain `"Super Nintendo"`. You could use the same approach to grab all files that are by Nintendo. by doing `--glob "*Nintendo*"`. But in this case, we're just going to grab that one zip file.

- **Get the URL to the file**

```bash
ia download no-intro_romsets --glob "*Super Nintendo*" --dry-run
```

Two thing have changed here. We change `list` to `download` and we add `--dry-run` to the end. This shows us the exact url that we're going to be getting from. If we were globbing up a lot of files, we would want to check to make sure we're getting what we think we're asking for.

Note that if we try using this url in a browser or with `wget`, it might return a `403: Forbidden` because it's only available to users that are logged in.

- **Smash that Download Button**

```bash
mkdir roms && cd roms
mkdir snes && cd snes
ia download no-intro_romsets --glob "*Super Nintendo*"
```

Make a roms directory and put a snes directory inside it. Then we just take off the `--dry-run` part and hit enter.

This is about 3.4 gigs worth of roms. It contains every release from Japan, Europe, the US. It contains licensed, unlicensed, aftermarket, and homebrew games. It has everything. You can see why you'd want to be somewhat selective about which systems you wanted to have all this for.

### Unzipping the Archive?

If you're concerned about space, you can leave the entire SNES library zipped up into one file. RetroArch is capable of reading from it, however, the larger that individual games become (such as with ISO based systems), the longer it will take to start up the game.

It's really a personal call whether or not to unzip them. Personally, I like to unzip rom archives when file sizes are small enough that unzipping isn't going to dramatically increase the storage space used. It's also worth noting that the random game script I'm going to show you at the end of this article isn't going to work unless you unzip the archive. So I'm warning you about this now.

If you'd like to do what I do, just:

```bash
unzip *.zip
```

## RetroArch Setup

### Initial Updates

So, let's talk about how ugly your RetroArch is going to be looking when we start it up and maybe fix that up a bit.

[![Ugly Retroarch Interface]({static}/images/retroarch/2.webp)]({static}/images/retroarch/2.png)

There's no way to automate setting all this up with commands so we have to just open up the software and do some clicking around.

- Navigate to `Main Menu > Online Updater`

[![Retroarch Interface at Online Updater Menu]({static}/images/retroarch/3.webp)]({static}/images/retroarch/3.png)

- Do `Update Core Info Files` 
- Do `Update Assets`
- Do... 
- Just update all the stuff.

You should immediately notice the icons and fonts have changed.

[![Retroarch Interface after Updating Assets]({static}/images/retroarch/4.webp)]({static}/images/retroarch/4.png)

### Importing ROMs

There's a lot of things we could do to adjust the appearance more if this is not to our liking, but let's focus on importing our roms.

Navigate to `Import Content > Scan Directory` and select the `roms/snes` directory that we made.

[![Retroarch Scan Directory Interface]({static}/images/retroarch/5.webp)]({static}/images/retroarch/5.png)

This can take a bit of time. When it's done, restart Retroarch. You should have a playlist of SNES games. 

Navigate back out to `Main Menu > Online Updater` and do `Playlist Thumbnails Updater`. Select your SNES playlist.

This can take a significantly larger bit of time. 

You can add as many rom sets as you want and eventually have a filled out group of playlists like this one.

[![Retroarch Playlists with Thumbnails Example]({static}/images/retroarch/6.webp)]({static}/images/retroarch/6.png)

### Downloading Emulators

In Retroarch an emulator is called a "core". Without a SNES emulator core, we can't play any of these SNES roms. You may be asking, "What is the correct core to use for this system," and the answer to the question is complicated and one that you'll only decide for yourself after using several of them.

In this article, I'm going to assume it's best to start with an emulator that is going to work for most people. That doesn't mean it's the best. It's just one I'm pretty sure will work.

Navigate to `Main Menu > Online Updater > Core Downloader`

Scroll down and select `Nintendo - SNES / SFC (Snes9x - Current)`.

[![Retroarch Playlists with Thumbnails Example]({static}/images/retroarch/7.webp)]({static}/images/retroarch/7.png)

### Starting Up a Game

Now, you should be able to select a game from your SNES playlist. Once selected, you can just hit `Run` and it will try to guess which core you would like to load that game with. If you have more than one SNES core, you can tell it which one to use with `Set Core Association`.

## Random Game Picker

Two sections into this article titled "Fun with Retroarch on Linux", and the only thing we've done is install/configure software, download stuff, and register for accounts. Let's try to do at least one fun thing.

---

It's possible to start up a game from the `retroarch` command by supplying it these argument:

```bash
retroarch -L {CORE_PATH} {ROM_PATH}
```

So in order for this work, we need to:

1. Organize ROMs into a directory structure
2. Associate a core file with a console directory
3. Write the script to grab a game and play it with the correct core.

### Organize ROMs into a Directory Structure

If you repeat the steps above that got you that nice SNES playlist, you could eventually have a roms directory that looks like this one.

```bash
$ tree /mnt/hdd/roms -d -L 1
/mnt/hdd/roms
├── gba
├── msx
├── n64
├── nes
├── sega
└── snes
```

Each one of these directories represents a console and is filled with roms.

Inside the snes folder, it looks like this:

```txt
$ ls /mnt/roms/snes | head -n 10
16 BIT XMAS 2011 - Christmas Craze (World) (RetroUSB.com) (Homebrew).zip
16 BIT XMAS 2011 - Christmas Craze (World) (Romhacking.net) (Homebrew).zip
16 BIT XMAS 2012 - Snowball Fight (World) (Homebrew).zip
2020 Super Baseball (Japan).zip
240p Test Suite (World) (v1.03) (NTSC) (Program) (Homebrew).zip
240p Test Suite (World) (v1.03) (PAL) (Program) (Homebrew).zip
240p Test Suite (World) (v1.061) (NTSC) (Program) (Homebrew).zip
240p Test Suite (World) (v1.061) (PAL) (Program) (Homebrew).zip
3-jigen Kakutou Ballz (Japan) (Sample).zip
3-jigen Kakutou Ballz (Japan).zip
```

### Associate a core file with a console directory

Solving this problem begs the question, where are the core files kept?

Open up Retroarch and navigate to `Settings > Directory` and find `Core Info`. It should have a path. In my case, the path is

`/home/$USER/.config/retroarch/cores`

So let's have a look at what is there; specifically, we're looking for `.so` files. We're not interested in any `.info` files, which there will be a lot of them. So let's filter them out.

```bash
ls /home/$USER/.config/retroarch/cores | egrep *.so
bluemsx_libretro.so
genesis_plus_gx_libretro.so
mesen_libretro.so
mgba_libretro.so
mupen64plus_next_libretro.so
snes9x_libretro.so
```

That is exactly the information we want. You may recall that we downloaded the snes9x core for our SNES games, and we see it right there, along with all the cores I downloaded for the other consoles I added later.

Let's put this information into a python data structure so that we can use it in a script.

#### **ra_cores.py**

Make a file called ra_cores.py.

```python
CORES = {
    'gba': 'mgba_libretro.so',
    'msx': 'bluemsx_libretro.so',
    'n64': 'mupen64plus_next_libretro.so',
    'snes': 'snes9x_libretro.so',
    'nes': 'mesen_libretro.so',
    'sega': 'genesis_plus_gx_libretro.so'
}
```

Now you're not going to just be able to use mine. You would have associate your `.so` files with your roms directories. But this is how mine looks. If you're following along and so far all you have is the SNES roms, this is all you need:

```python
CORES = {
    'snes': 'snes9x_libretro.so'
}
```

Save the file.

### Write the script

So make another file.

#### **ra_random.py**

```python
from pathlib import Path
from random import choice
from sys import argv
import os, subprocess

from ra_cores import CORES

ROMS_PATH = "/mnt/hdd/roms"
CORE_PARENT = Path(
  "/home/username/.config/retroarch/cores/"
)
GLOB_PATTERN = '*(USA)*'
EXCLUDED_CONSOLES = ['gba']


def print_choice(console, rom):
    print(f"Console: {console}")
    print(f"ROM: {rom}")


try:
    script, console_name = argv
except ValueError:
    script = argv[0]
    console_name = None

roms = Path(ROMS_PATH)
os.chdir(roms)

if console_name is None:
    console_pool = [c for c in CORES.keys() if c not in EXCLUDED_CONSOLES]
    console_name = choice(console_pool)

roms_dirs = [d.stem for d in roms.glob('*') if d.is_dir()]
if not console_name in roms_dirs:
    print(f"Argument {console_name} not a directory in {roms}")
    exit(1)

core_path = CORE_PARENT / CORES[console_name]
try:
    rom_path = choice(list(roms.joinpath(console_name).glob(GLOB_PATTERN)))
    print_choice(console_name, rom_path.stem)
    subprocess.run(['retroarch', '-L', f"{core_path}", f"{rom_path}"])
except IndexError:
    subprocess.run(["python3", script])
```

Let's look more closely at these lines:

```python
ROMS_PATH = "/mnt/hdd/roms"
CORE_PARENT = Path(
  "/home/username/.config/retroarch/cores/"
)
GLOB_PATTERN = '*(USA)*'
EXCLUDED_CONSOLES = ['gba']
```

You're going to have make this stuff match your directory paths.

1. `ROMS_PATH` is where your roms directories are located.
2. `CORE_PARENT` is the folder where we found the `.so` files.
3. `GLOB_PATTERN` is used in this case to only select games that were released in the USA. This works because every rom in No-Intro set that is a USA release has `(USA)` in the filename. You might not want this, in which case you could just change it to `*` to include every game in the item pool. Or maybe you could try `*(Homebrew)*` and see what that is like.
4. `EXCLUDED_CONSOLES` is used to list our consoles that we don't want to select from. You could change it to `[]` if you wanted to include everything.

### FUN!

Try it out with:

`python3 ra_random.py` 

...or you could tell it you only want it to pick from a specific console:

`python3 ra_random.py snes`

## So, Did We Have Fun?

I don't know if we did or not... But if this inspires you to set up something like this of your own, you'll eventually get to the fun. Good luck.
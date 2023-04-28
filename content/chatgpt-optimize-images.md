Title: ChatGPT Optimizes Images for Web
Date: 2023-04-02
Slug: chatgpt-optimize-images
Tags: chatgpt, ai, webdev, python

In five prompts, ChatGPT writes fully functional code to optimize images for the web and then a story about how Case from Neuromancer uses the code to stop a hacker.

## Code

---

### "Give me a Python function using PIL that optimizes a directory of images for the web and outputs them to a new directory."

---

```py
from PIL import Image
import os

def optimize_images(input_dir, output_dir):
    # Check if output directory exists and create it if it doesn't
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate through all files in input directory
    for filename in os.listdir(input_dir):
        # Check if file is an image
        if filename.endswith('.jpg') \
            or filename.endswith('.jpeg') \
                or filename.endswith('.png'):

            # Open image using PIL
            img = Image.open(os.path.join(input_dir, filename))

            # Optimize image for web
            img = img.convert('RGB')
            img.save(os.path.join(
                output_dir, filename), 
                optimize=True, quality=85
            )

            print(f'Optimized {filename}')
```

---

### "Make it convert the images to webp and resize them to a width of 500 px and maintain aspect ratio"

---

```py
from PIL import Image
import os

def optimize_images(input_dir, output_dir):
    # Check if output directory exists and create it if it doesn't
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate through all files in input directory
    for filename in os.listdir(input_dir):
        # Check if file is an image
        if filename.endswith('.jpg') \
            or filename.endswith('.jpeg') \
                or filename.endswith('.png'):

            # Open image using PIL
            img = Image.open(os.path.join(input_dir, filename))

            # Resize image while maintaining aspect ratio
            max_width = 500
            width, height = img.size
            if width > max_width:
                new_height = int(height * max_width / width)
                img = img.resize((max_width, new_height), resample=Image.LANCZOS)

            # Convert image to WebP format and save to output directory
            output_path = os.path.join(
                output_dir, 
                os.path.splitext(filename)[0] + '.webp'
            )
            img.save(output_path, 'webp', quality=85)

            print(f'Optimized {filename}')
```

---

### "Update the function to compare the file sizes in human readable format"

---

```py
import os
from PIL import Image
import math

def convert_bytes(num):
    """
    Helper function to convert a number of bytes to a human-readable format
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return f"{num:.2f} {x}"
        num /= 1024.0

def optimize_images(input_dir, output_dir):
    # Check if output directory exists and create it if it doesn't
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate through all files in input directory
    for filename in os.listdir(input_dir):
        # Check if file is an image
        if filename.endswith('.jpg') \
            or filename.endswith('.jpeg') \
                or filename.endswith('.png'):

            # Open image using PIL
            img = Image.open(os.path.join(input_dir, filename))

            # Resize image while maintaining aspect ratio
            max_width = 500
            width, height = img.size
            if width > max_width:
                new_height = int(height * max_width / width)
                img = img.resize((max_width, new_height), resample=Image.LANCZOS)

            # Convert image to WebP format and save to output directory
            output_path = os.path.join(
                output_dir, 
                os.path.splitext(filename)[0] + '.webp'
            )
            img.save(output_path, 'webp', quality=85)

            # Get file sizes of original and optimized images
            orig_size = os.path.getsize(os.path.join(input_dir, filename))
            opt_size = os.path.getsize(output_path)

            # Print message indicating optimization results
            print(f'{filename}: Original size = {convert_bytes(orig_size)}, '+\
                f'Optimized size = {convert_bytes(opt_size)}')
```

---

### "Update `optimize_images` function to recursively work through directories inside the input_dir"

---

```py
import os
from PIL import Image
import math

def convert_bytes(num):
    """
    Helper function to convert a number of bytes to a human-readable format
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return f"{num:.2f} {x}"
        num /= 1024.0

def optimize_images(input_dir, output_dir):
    # Check if output directory exists and create it if it doesn't
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate through all files and directories in input directory
    for filename in os.listdir(input_dir):
        filepath = os.path.join(input_dir, filename)
        # Check if file is a directory and recurse into it if it is
        if os.path.isdir(filepath):
            optimize_images(filepath, os.path.join(output_dir, filename))
        # Check if file is an image
        elif filename.endswith('.jpg') \
            or filename.endswith('.jpeg') \
                or filename.endswith('.png'):
            # Open image using PIL
            img = Image.open(filepath)

            # Resize image while maintaining aspect ratio
            max_width = 500
            width, height = img.size
            if width > max_width:
                new_height = int(height * max_width / width)
                img = img.resize((max_width, new_height), resample=Image.LANCZOS)

            # Convert image to WebP format and save to output directory
            output_path = os.path.join(
                output_dir, 
                os.path.splitext(filename)[0] + '.webp'
            )
            img.save(output_path, 'webp', quality=85)

            # Get file sizes of original and optimized images
            orig_size = os.path.getsize(filepath)
            opt_size = os.path.getsize(output_path)

            # Print message indicating optimization results
            print(f'{filename}: Original size = {convert_bytes(orig_size)}, '+\
                f'Optimized size = {convert_bytes(opt_size)}')
```

---

### "Allow the script to accept command line arguments for the input and output directories and pass them to optimize_images"

---

```py
import os
from PIL import Image
import math
import argparse

def convert_bytes(num):
    """
    Helper function to convert a number of bytes to a human-readable format
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return f"{num:.2f} {x}"
        num /= 1024.0

def optimize_images(input_dir, output_dir):
    # Check if output directory exists and create it if it doesn't
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate through all files and directories in input directory
    for filename in os.listdir(input_dir):
        filepath = os.path.join(input_dir, filename)
        # Check if file is a directory and recurse into it if it is
        if os.path.isdir(filepath):
            optimize_images(filepath, os.path.join(output_dir, filename))
        # Check if file is an image
        elif filename.endswith('.jpg') \
            or filename.endswith('.jpeg') \
                or filename.endswith('.png'):
            # Open image using PIL
            img = Image.open(filepath)

            # Resize image while maintaining aspect ratio
            max_width = 500
            width, height = img.size
            if width > max_width:
                new_height = int(height * max_width / width)
                img = img.resize((max_width, new_height), resample=Image.LANCZOS)

            # Convert image to WebP format and save to output directory
            output_path = os.path.join(
                output_dir, 
                os.path.splitext(filename)[0] + '.webp'
            )
            img.save(output_path, 'webp', quality=85)

            # Get file sizes of original and optimized images
            orig_size = os.path.getsize(filepath)
            opt_size = os.path.getsize(output_path)

            # Print message indicating optimization results
            print(f'{filename}: Original size = {convert_bytes(orig_size)}, '+\
                f'Optimized size = {convert_bytes(opt_size)}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Optimize images in a directory for web use.'
    )
    parser.add_argument('input_dir', metavar='INPUT_DIR', type=str,
                        help='the directory containing the images to optimize')
    parser.add_argument('output_dir', metavar='OUTPUT_DIR', type=str,
                        help='the directory where the optimized images will be saved')
    args = parser.parse_args()

    input_dir = args.input_dir
    output_dir = args.output_dir

    optimize_images(input_dir, output_dir)
```

---

## Story

---

### "Tell a story where Case from Neuromancer uses this function to stop a hacker from destroying The Boston-Atlanta Metropolitan Axis"

---

Case had been hired by the Tessier-Ashpool family to infiltrate The Boston-Atlanta Metropolitan Axis, one of the largest and most complex data networks in the world. His mission was to steal valuable data and deliver it to his employers in exchange for a hefty sum of money.

As he made his way through the system, Case noticed that something was off. The network seemed slower than usual and he kept encountering strange glitches and errors. It didn't take him long to realize that someone was trying to sabotage the network from the inside.

Determined to stop the hacker before it was too late, Case decided to use his knowledge of image optimization to his advantage. He quickly wrote a Python script that could optimize all of the images on the network, making them smaller and more efficient without sacrificing quality.

Case knew that if he could run the script on all of the images, it would significantly reduce the load on the network, making it more difficult for the hacker to carry out their attack.

With the script ready, Case began to execute it on every image he could find on the network. As he worked, he could see the network start to stabilize and the glitches and errors started to disappear.

It wasn't long before the hacker realized what Case was doing and tried to stop him. But it was too late - the network had been stabilized and the attack had been thwarted.

Thanks to his quick thinking and knowledge of image optimization, Case had saved The Boston-Atlanta Metropolitan Axis from destruction and completed his mission for the Tessier-Ashpool family.

As he sat back and watched the network return to normal, Case couldn't help but feel a sense of satisfaction. He had used his skills to not only complete his mission, but also to prevent a disaster that could have affected thousands of people.
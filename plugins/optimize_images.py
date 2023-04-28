import os
from PIL import Image
from pelican import signals

def convert_bytes(num):
    """
    Helper function to convert a number of bytes to a human-readable format
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return f"{num:.2f} {x}"
        num /= 1024.0

def optimize_image(filepath, output_path, filename):
    # Open image using PIL
    img = Image.open(filepath)

    # Resize image while maintaining aspect ratio
    max_width = 608
    width, height = img.size
    if width > max_width:
        new_height = int(height * max_width / width)
        img = img.resize((max_width, new_height), resample=Image.LANCZOS)

    # Convert image to WebP format and save to output directory
    img.save(output_path, 'webp', quality=85)

    # Get file sizes of original and optimized images
    orig_size = os.path.getsize(filepath)
    opt_size = os.path.getsize(output_path)

    # Print message indicating optimization results
    print(f'{filename}: Original size = {convert_bytes(orig_size)}, Optimized size = {convert_bytes(opt_size)}')


def optimize_images(pelican, fp=None):
    images_path = os.path.join(pelican.settings['PATH'], pelican.settings['IMAGES_PATH']) # content/images
    icons_path = os.path.join(pelican.settings['PATH'], pelican.settings['ICONS_PATH'])  # content/images/icons
    if fp is None:
        input_dir = output_dir = images_path
    else:
        input_dir = output_dir = fp
    # Check if output directory exists and create it if it doesn't
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate through all files and directories in input directory
    for filename in os.listdir(input_dir):
        output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.webp')
        filepath = os.path.join(input_dir, filename)

        # Skip icons
        if icons_path in filepath:
            continue

        # Check if file is a directory and recurse into it if it is
        if os.path.isdir(filepath):
            optimize_images(pelican, fp=filepath)
        # Check if file is an image
        elif filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
            # Skip if it exists
            if os.path.exists(output_path):
                continue
            optimize_image(filepath, output_path, filename)


def register():
    signals.generator_init.connect(optimize_images)

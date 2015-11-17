#! /home/lubuntu/anaconda/envs/image-edit/bin/python

from optparse import OptionParser
from PIL import Image


def blend_two_images(overlay_image, background_image, overlay_strength,
                     output_file):
    """ Blend two images and save to a .png file.

    Keyword arguments:
    overlay_image -- overlay_strength transparency in output_file
    background_image -- (1 - overlay_strength) transparency in output_file
    overlay_strength -- alpha channel multiplier
    output_file -- file to save to
    """

    # Open images
    background = Image.open(background_image)
    overlay = Image.open(overlay_image)

    # Match image sizes
    background_width, background_height = background.size
    overlay_width, overlay_height = overlay.size

    if (background_width > overlay_width) and \
       (background_height > overlay_height):
        background = background.resize((overlay_width, overlay_height))
    elif (background_width > overlay_width) and \
         (overlay_height > background_height):
        background = background.resize((overlay_width, background_height))
        overlay = overlay.resize((overlay_width, background_height))
    else:
        if (background_height > overlay_height):
            background = background.resize((background_width, overlay_height))
            overlay = overlay.resize((background_width, overlay_height))
        else:
            overlay = overlay.resize((background_width, background_height))

    # Convert images to RGBA
    background = background.convert("RGBA")
    overlay = overlay.convert("RGBA")

    new_img = Image.blend(background, overlay, 0.5)
    new_img.save(output_file, "PNG")

if __name__ == "__main__":
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("--background", dest="background_image",
                      help="(1 - overlay_strength) transparency \
                      in output_file")
    parser.add_option("--overlay", dest="overlay_image",
                      help="overlay_strength transparency in output_file")
    parser.add_option("--strength", dest="overlay_strength",
                      help="alpha channel level to apply", default="0.5")
    parser.add_option("--out", dest="output_file",
                      help="name of .png file to save to", default="out.png")
    options, args = parser.parse_args()

    if not (options.background_image or options.overlay_image):
        parser.error("Must provide images.")

    blend_two_images(options.overlay_image, options.background_image,
                     options.overlay_strength, options.output_file)

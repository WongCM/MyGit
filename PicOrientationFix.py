from PIL import Image # Pillow (http://python-pillow.github.io/) is a great python3-supporting PIL fork

# def FixImage(img, max_width=None, max_height=None):
def FixImage(img):
    '''
    Strips an image of everything but its basic data (nasty EXIF tags, gif animations, etc.), first correcting orientation if necessary.

    'img' must be a PIL.Image.Image instance. Returns a new instance. Requires the PIL.Image (Python Image Library) or equivalent to be imported as Image; image formats supported depend on PIL prereqs installed on the system (see http://pillow.readthedocs.io/en/3.0.x/installation.html).

    If max_width and/or max_height are supplied (pixels as int), the image is proportionally downsized to fit the tighter of the two constraints using a high-quality downsampling filter.
    '''

    ORIENT = { # exif_val: (rotate degrees cw, mirror 0=no 1=horiz 2=vert); see http://www.sno.phy.queensu.ca/~phil/exiftool/TagNames/EXIF.html
              2: (0, 1),
              3: (180, 0),
              4: (0, 2),
              5: (90, 1),
              6: (270, 0),
              7: (270, 1),
              8: (90, 0),
             }

    assert isinstance(img, Image.Image), "Invalid 'img' parameter to fix_image()"
    img_format = img.format

    # fix img orientation (issue with jpegs taken by cams; phones in particular):
    try:
        orient = img._getexif()[274]
    except (AttributeError, KeyError, TypeError, ValueError):
        orient = 1 # default (normal)
    if orient in ORIENT:
        (rotate, mirror) = ORIENT[orient]
        if rotate:
            img = img.rotate(rotate)
        if mirror == 1:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
        elif mirror == 2:
            img = img.transpose(Image.FLIP_TOP_BOTTOM)

    # strip image
    data = img.getdata()
    palette = img.getpalette()
    img = Image.new(img.mode, img.size)
    img.putdata(data)
    if palette:
        img.putpalette(palette)

    # resize image (if necessary):
    # (width, height) = img.size
    # if max_width and width > max_width and (not max_height or width*max_height >= height*max_width): # width is constraint
    #     img = img.resize((max_width, round(height*max_width/width)), Image.LANCZOS)
    # elif max_height and height > max_height: # height is constraint
    #     img = img.resize((round(width*max_height/height), max_height), Image.LANCZOS)

    img.format = img_format # preserve orig format
    return img

if __name__ == "__main__": # run this script as-is for a basic test
    # *****************
    # * Usage Example *
    # *****************
    infile = '/Users/apple/Downloads/2018-02-06/902040201/IMG_4390.JPG'
    try:
        img = Image.open(infile)
    except IOError as err:
        print('Error opening file:', str(err))
        img = None
    if img:
        if img.format:
            print('Image format:', img.format) # use in Content-Type: image/format header when returning image over the web)
            outfile = '/Users/apple/Downloads/2018-02-06/902040201/IMG_4390Fixed2.JPG'
            # max_width = int(input('New max width (0 for none): '))
            # max_height = int(input('New max height (0 for none): '))
            # FixImage(img, max_width, max_height).save(outfile, img.format)

            # FixImage(img).save(outfile, img.format)

            FixImage(img).save(outfile)
            
            # alternatively, to get the image binary instead of writing it back to a file (python3):
            # > from io import BytesIO
            # > new_img = BytesIO()
            # > FixImage(img, max_width, max_height).save(new_img, img.format)
            # > new_image_binary = new_img.getvalue()
            print('New image saved.')
        else:
            print('Unrecognized image format.')
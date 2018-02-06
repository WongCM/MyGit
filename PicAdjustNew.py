#coding=utf-8
import PIL.Image
from PIL import Image
import shutil
import os
# 不加以下代码会出现IO错误
from PIL import ImageFile
import PicOrientationFix
ImageFile.LOAD_TRUNCATED_IMAGES = True


# infile = '/Users/apple/Desktop/12041_P_1504160793305.JPG'
# outfile = '/Users/apple/Desktop/12041_P_1504160793305_Adjust.JPG'

# @classmethod
def fixed_size(infile,outfile,width,height): 
    """按照固定尺寸处理图片"""
    im = PIL.Image.open(infile)
    print 'i am picture format ' + im.format
    imFixedOrient = PicOrientationFix.FixImage(im)
    # out = im.resize((width, height),PIL.Image.ANTIALIAS)
    out = imFixedOrient.resize((width, height),PIL.Image.ANTIALIAS)
    out.save(outfile)

# # @classmethod
def FixImage2(img):
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

    # assert isinstance(img, Image.Image), "Invalid 'img' parameter to fix_image()"
    # img_format = img.format

    # fix img orientation (issue with jpegs taken by cams; phones in particular):
    try:
        orient = img._getexif()[274]
        print 'the orient is -->' + orient
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

    # img.format = img_format # preserve orig format
    return img

if __name__ == '__main__':
    print 'begin now'

    picInPath = '/Users/apple/Downloads/2018-02-05/PicAdjustTest/'
    picToPath = '/Users/apple/Downloads/2018-02-05/PicAdjustTestTo/'

    # nowNum用来计数当前处理了几次
    nowNum = 1

    listLength = len(os.listdir(picInPath))

    for i in os.listdir(picInPath):
        # j为PicAdjustTest文件夹下的子文件夹路径
        j = picInPath + i + '/'
        if i == '.DS_Store':
            continue
        newFolder = '/Users/apple/Downloads/2018-02-05/PicAdjustTestTo/' + i
        isExists=os.path.exists(newFolder)
        if not isExists:
            os.makedirs(newFolder)
        listLengthJ = len(os.listdir(j))
        print 'the lenth of j is ' + str(listLengthJ)
        print 'the lenth of i is ' + str(listLength)
        print os.listdir(j)
        for x in os.listdir(j):
            if x == '.DS_Store':
                continue
            if os.path.splitext(x)[1] == '.MOV':
                continue
            print x
            shuchulujin = picToPath + i + '/' + x
            print shuchulujin
            print '共需要处理' + str((listLength-1)*(listLengthJ-1)) + '次，现在是第' + str(nowNum) + '次'
            nowNum = nowNum + 1
            # print '---->' + os.path.splitext(x)[1]
            str1 = picInPath + i + '/' + os.path.splitext(x)[0] + os.path.splitext(x)[1]
            # print 'str1 is ++++>>>>>>' + str1
            str2 = shuchulujin

            print  'the str1 is ' + str1
            print 'the str2 is ' + str2

            fixed_size(str1,str2,760,760)
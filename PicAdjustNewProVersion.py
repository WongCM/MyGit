#coding=utf-8
import PIL.Image
from PIL import Image
import shutil
import os
# 不加以下代码会出现IO错误
from PIL import ImageFile
import PicOrientationFix
ImageFile.LOAD_TRUNCATED_IMAGES = True

# @classmethod
def fixed_size(infile,outfile,width,height): 
    """按照固定尺寸处理图片"""
    im = PIL.Image.open(infile)
    print 'i am picture format ' + im.format
    imFixedOrient = PicOrientationFix.FixImage(im)
    # out = im.resize((width, height),PIL.Image.ANTIALIAS)
    out = imFixedOrient.resize((width, height),PIL.Image.ANTIALIAS)
    print '----????----????'
    out.save(outfile)

# 遍历文件夹
def listDir(toList):
	return os.listdir(toList)

# 根据文件名判断是否是目录，如果是目录，则返回true，否则返回false
def isDir(target):
	if os.path.splitext(target)[1] == '' :
		return True
	else :
		return False

def showAll(picInPath,picToPath):
	# print type(len(listDir(toShow)))
	# cutoffline = ''
	if not len(listDir(picInPath)):
		print '目标文件夹下无文件'
		return
	for i in listDir(picInPath):
		print i
		if i == '.DS_Store':
			print '这是.DS_Store文件'
			continue
		if isDir(i):
			print '这是个目录'
			# 在输出文件夹里创建对应的目录，不然压缩后输出会报错
			newFolder = picToPath + i
			isExists=os.path.exists(newFolder)
			if not isExists:
				os.makedirs(newFolder)
			showAll(picInPath + i + '/',picToPath + i + '/')
		else :
			print 'i 的路径是 : ' + picInPath + i
			print 'i 的输出路径是 : ' + picToPath + i
			print '这是个文件-----'
			if os.path.splitext(i)[1] == '.MOV':
				shutil.copy(picInPath + i, picToPath + i)
				pass
			if os.path.splitext(i)[1] == '.png':
				shutil.copy(picInPath + i, picToPath + i)
				pass
			if os.path.splitext(i)[1] == '.PNG':
				shutil.copy(picInPath + i, picToPath + i)
				pass
			if os.path.splitext(i)[1] == '.db':
				shutil.copy(picInPath + i, picToPath + i)
				pass
			if os.path.splitext(i)[1] == '.JPG' or os.path.splitext(i)[1] == 'jpg':
				fixed_size(picInPath + i,picToPath + i,760,760)
				pass

if __name__ == '__main__':

	picInPath = '/Users/apple/Downloads/2018-02-13/Feb12/'
	picToPath = '/Users/apple/Downloads/2018-02-13/TestProYasuo/'

	showAll(picInPath,picToPath)
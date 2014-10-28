import os
import re

IMG_REGEX = '^.+\.(png|jpg|jpeg|tif|tiff|gif|bmp)$'

def compile_index(dir_path, image_files):
	index_path = os.path.join(dir_path, 'imageme.html')
	index = open(index_path, 'w')
	index.write('<!DOCTYPE html>\n')
	index.write('<head></head>\n')
	index.write('<body>\n')
	for f in image_files:
		index.write('<div><img\n')
	index.write('</body>\n')
	index.close()
	print('Index file available at %s' % index_path)

def get_image_files(path):
	all_files = os.listdir(path)
	print('All files:')
	for f in all_files: print(' ' + f)
	image_files = [f for f in all_files if re.match(IMG_REGEX, f)]
	print('Image files:')
	for f in image_files: print(' ' + f)
	return image_files

if __name__ == '__main__':
	path = '.'
	image_files = get_image_files(path)
	compile_index(path, image_files)

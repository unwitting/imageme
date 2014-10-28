import os
import re
import SimpleHTTPServer
import SocketServer
import sys

CSS_FILE_NAME = '../imageme.css'
IMAGE_REGEX = '^.+\.(png|jpg|jpeg|tif|tiff|gif|bmp)$'
IMAGES_PER_ROW = 3
INDEX_FILE_NAME = 'imageme.html'

def compile_index(dir_path, image_files):
	index_path = os.path.join(dir_path, INDEX_FILE_NAME)
	index = open(index_path, 'w')
	index.write('<!DOCTYPE html>\n')
	index.write('<head>\n')
	css_file = open(CSS_FILE_NAME)
	css = css_file.read()
	css_file.close()
	index.write('<style>%s</style>' % css)
	index.write('</head>\n')
	index.write('<body><div class="content"><table>\n')
	row_count = 0
	for f in image_files:
		if row_count == 0:
			index.write('<tr>\n')
		index.write('<td>\n')
		index.write('<a href="%s"><img src="%s"></a>\n' % (f, f))
		index.write('</td>\n')
		row_count += 1
		if row_count == IMAGES_PER_ROW:
			row_count = 0
			index.write('</tr>\n')
	index.write('</table></div></body>\n')
	index.close()
	print('Index file available at %s' % index_path)

def get_image_files(path):
	all_files = os.listdir(path)
	print('All files:')
	for f in all_files: print(' ' + f)
	image_files = [f for f in all_files if re.match(IMAGE_REGEX, f)]
	print('Image files:')
	for f in image_files: print(' ' + f)
	return image_files

def run_server():
	port = get_server_port()
	server = SocketServer.TCPServer(
		('', port),
		SimpleHTTPServer.SimpleHTTPRequestHandler
	)
	print('Your images are at http://127.0.0.1:%d/%s' % (
		port,
		INDEX_FILE_NAME
	))
	server.serve_forever()
	return server

def get_server_port():
	port = int(sys.argv[1]) if len(sys.argv) > 2 else 8000
	return port

if __name__ == '__main__':
	path = '.'
	image_files = get_image_files(path)
	compile_index(path, image_files)
	run_server()

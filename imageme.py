#!/usr/bin/python
import os, re, sys, SimpleHTTPServer, SocketServer

INDEX_FILE_NAME = 'imageme.html'
IMAGE_FILE_REGEX = '^.+\.(png|jpg|jpeg|tif|tiff|gif|bmp)$'
IMAGES_PER_ROW = 3

def _create_index_file(root_dir, location, image_files, dirs):
	html = [
		'<!DOCTYPE html>',
		'<html>',
		'	<head>',
		'		<title>imageMe</title>'
		'		<style>',
		'			html, body {margin: 0;padding: 0;}',
		'			.header {text-align: right;}',
		'			.content {padding: 3em;	padding-left: 4em; padding-right: 4em;}',
		'			.image {max-width: 100%; border-radius: 0.3em;}',
		'			td {width: ' + str(100.0 / IMAGES_PER_ROW) + '%;}',
		'		</style>',
		'	</head>',
		'	<body>',
		'	<div class="content">',
		'		<h2 class="header">imageMe: ' + location + ' [' + str(len(image_files)) + ' image(s)]</h2>',
		'		<hr>'
	]
	directories = []
	if root_dir != location: directories = ['..']
	directories += dirs
	for directory in directories:
		link = directory + '/' + INDEX_FILE_NAME
		html += [
			'	<h3 class="header">',
			'	<a href="' + link + '">' + directory + '</a>',
			'	</h3>'
		]
	table_row_count = 1
	html += ['<hr>', '<table>']
	for image_file in image_files:
		if table_row_count == 1: html.append('<tr>')
		html += [
			'	<td>',
			'	<a href="' + image_file + '">',
			'		<img class="image" src="' + image_file + '">',
			'	</a>',
			'	</td>'
		]
		if table_row_count == IMAGES_PER_ROW:
			table_row_count = 0
			html.append('</tr>')
		table_row_count += 1
	html += ['</tr>', '</table>']
	html += [
		'	</div>',
		'	</body>',
		'</html>'
	]
	index_file_path = _get_index_file_path(location)
	print('Creating index file %s' % index_file_path)
	index_file = open(index_file_path, 'w')
	index_file.write('\n'.join(html))
	index_file.close()
	return index_file_path

def _get_index_file_path(location):
	return os.path.join(location, INDEX_FILE_NAME)

def _get_server_port():
	port = int(sys.argv[1]) if len(sys.argv) > 2 else 8000
	return port

def clean_up(paths):
	print('Cleaning up')
	for path in paths:
		print('Removing %s' % path)
		os.unlink(path)

def create_index_files(root_dir):
	created_files = []
	for here, dirs, files in os.walk(root_dir):
		dirs = sorted(dirs)
		print('Processing %s' % here)
		image_files = [f for f in files if re.match(IMAGE_FILE_REGEX, f)]
		image_files = sorted(image_files)
		created_files.append(
			_create_index_file(root_dir, here, image_files, dirs)
		)
	return created_files

def run_server():
	port = _get_server_port()
	SocketServer.TCPServer.allow_reuse_address = True
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

if __name__ == '__main__':
	created_files = create_index_files('.')
	try:
		run_server()
	except KeyboardInterrupt:
		print('User interrupted, stopping')
	except Exception as e:
		print(e)
		print('Unhandled exception in server, stopping')
	clean_up(created_files)

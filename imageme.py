#!/usr/bin/python

# Dependencies
import os, re, sys, SimpleHTTPServer, SocketServer

# Constants / configuration
## Filename of the generated index files
INDEX_FILE_NAME = 'imageme.html'
## Regex for matching only image files
IMAGE_FILE_REGEX = '^.+\.(png|jpg|jpeg|tif|tiff|gif|bmp)$'
## Images per row of the gallery tables
IMAGES_PER_ROW = 3

def _create_index_file(root_dir, location, image_files, dirs):
	"""
	Create an index file in the given location, supplying known lists of
	present image files and subdirectories.

	@param {String} root_dir - The root directory of the entire crawl. Used to
		ascertain whether the given location is the top level.

	@param {String} location - The current directory of the crawl. The index
		file will be created here.

	@param {[String]} image_files - A list of image file names in the location.
		These will be displayed in the index file's gallery.

	@param {[String]} dirs - The subdirectories of the location directory.
		These will be displayed as links further down the file structure.

	@return {String} The full path (location plus filename) of the newly
		created index file. Intended for usage cleaning up created files.
	"""
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
	"""
	Get the full file path to be used for an index file in the given location.
	Yields location plus the constant INDEX_FILE_NAME.

	@param {String} location - A directory location in which we want to create
		a new index file.

	@return {String} A file path for usage with a new index file.
	"""
	return os.path.join(location, INDEX_FILE_NAME)

def _get_server_port():
	"""
	Get the port specified for the server to run on. If given as the first
	command line argument, we'll use that. Else we'll default to 8000.

	@return {Integer} The port to run the server on. Default 8000, overridden
		by first command line argument.
	"""
	port = int(sys.argv[1]) if len(sys.argv) >= 2 else 8000
	return port

def clean_up(paths):
	"""
	Clean up after ourselves, removing created files.

	@param {[String]} A list of file paths specifying the files we've created
		during run. Will all be deleted.

	@return {None}
	"""
	print('Cleaning up')
	for path in paths:
		print('Removing %s' % path)
		os.unlink(path)

def create_index_files(root_dir):
	"""
	Crawl the root directory downwards, generating an index HTML file in each
	directory on the way down.

	@param {String} root_dir - The top level directory to crawl down from. In
		normal usage, this will be '.'.

	@return {[String]} Full file paths of all created files.
	"""
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
	"""
	Run the image server. This is blocking. Will handle user KeyboardInterrupt
	and other exceptions appropriately and return control once the server is
	stopped.

	@return {None}
	"""
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
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		print('User interrupted, stopping')
	except Exception as e:
		print(e)
		print('Unhandled exception in server, stopping')

if __name__ == '__main__':
	created_files = create_index_files('.')
	run_server()
	clean_up(created_files)

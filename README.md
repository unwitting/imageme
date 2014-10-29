# imageMe

imageMe is a super simple image gallery server.

Think `python -m SimpleHTTPServer` for pictures.

## Super Duper Easy One Line Usage

To run the image server on port 8000:

```bash
curl https://raw.githubusercontent.com/unwitting/imageme/master/imageme.py | python
```

## Manual Usage

### Step 1: Get the file

Get hold of a copy of `imageme.py`. For _really_ easy use put it in your `PATH`.

You could clone this repo:

```bash
> git clone https://github.com/unwitting/imageme.git
```

Or just grab the file directly:

```bash
> wget https://raw.githubusercontent.com/unwitting/imageme/master/imageme.py
```

### Step 2: Run imageMe

Run `imageme.py` from the root directory to serve from:

```bash
> cd /path/to/my/pics
> imageme.py
Processing .
Creating index file ./imageme.html
Processing ./photos
Creating index file ./photos/imageme.html
Processing ./photos/holiday
Creating index file ./photos/holiday/imageme.html
Processing ./photos/family
Creating index file ./photos/family/imageme.html
Processing ./super_secret_stay_out
Creating index file ./super_secret_stay_out/imageme.html
Your images are at http://127.0.0.1:8000/imageme.html
```

You can specify a port, just like you can with `SimpleHTTPServer`:

```bash
> imageme.py 5678
Processing .
...
Your images are at http://127.0.0.1:5678/imageme.html
```

### Step 3: Browse and enjoy

Hit the URL imageMe tells you in your browser, and have fun exploring.

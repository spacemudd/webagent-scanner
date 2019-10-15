# What is it about?

Allows your web application to communicate with a scanner and receive scanned images.

# Installation

1. Make sure you have Python 2.7 is installed.
2. Make sure cmd `pip` is recognized, else, add Python to your system's PATH.
3. Download & install the [TWAIN python module](https://pypi.python.org/pypi/twain#downloads).
4. Execute `pip install image` (responsible for serving images)
5. Execute `pip install tornado` (responsible for opening a web server) 
6. Execute `pip install wxPython` (responsible for the app to become a tray icon)
7. pip install http://sourceforge.net/projects/py2exe/files/latest/download?source=files
8. `pip install .`
9. Navigate to the project folder and execute `app.py`.

# Usage

1. In command prompt, navigate to the project's root and run `app.py`.

2. Make sure `app.py` is serving.

2. In your web application(s), call a simple Ajax GET request to localhost:8087 (see below section).

# API

All communicaction are in HTTPS GET requests format.

> /scan

**Description**

Selects the **first** scanner the app finds and begins the scanning call.

**Request example**

    $.support.cors = true;

    $.ajax({
        crossDomain: true,
        type : "GET",
        url : "https://localhost:8087/scan",
        dataType : "json",
        success : function(response) {
            console.log(response.data) // base64 encoded image
        },
    });

**Response example**

String. Base64 encoded string of a single JPEG image.

> /multi-scan

**Description**

Selects the **first** scanner the app finds and begin scanning until all papers are scanned.

**Request example**

    $.support.cors = true;

    $.ajax({
        crossDomain: true,
        type : "GET",
        url : "https://localhost:8087/multi-scan",
        success : function(response) {
            console.log(response.data.images); // An array of base64 encoded strings.
            console.log('total:' + response.data.total); // Total images scanned.
        },
    });


**Example response**

    {
        'images': {
            base64 encoded string,
            base64 encoded string,
            ...
        },
        'total': 10
    }

> /get-scanners

**Description**

Gets a list of scanners detected.

**Request example**

    {
        'scanner-name': 'scanner-name',
        'scanner-name1': 'scanner-name1',
        ...
    }

# How to build

1. Run `python setup.py py2exe`
2. Once compiled, navigate to `dist`, and open `app.exe`.

If you plan to take app.exe somewhere else, it must have the folder 'cert' next to it 
with the certificate files.

# Questions

### 1. How do I set the scanner?

In `app.py`, you will find the function `setScanner`, use that.

### 2. Can I see a list of the scanners connected?

Call the route `/get-scanners`.

# Reason this repo exists

Often times web-applications need to benefit from connecting to scanners.

It's virtually impossible if we take a direct route to a scanner via DLL located on clients' computers,
because web browsers don't have permission to utilize those resources.

Sometimes it is often suggested to use:

1. **ActiveX**: Allows you to communicate directly with DLLs. It propriety code, *limited to IE*, and
has security problems.

2. **Java applets**: Communicate directly with DLLs. Except, the support of Java
applets is dying. Chrome/FF don't support this anymore.

3. Silverlight / Flash... no.

# Solution

Have a 'Web Agent' which acts as a local server that accepts HTTP requests.

Based on the HTTP requests, we call the appropiate DLL or execute commands.

**A web agent is a link between the browser and the internals of the computer.**

Further read: https://wicg.github.io/webusb/ - Chrome's WebUSB API. This also limited to Chrome.

# Roadmap

- Allow user to select which scanner to choose from.
- A GUI for the web agent.
- Web agent can be minimized to tray.
- Allow web agent to be added to the system's startup & be minimized on boot.
- Work on API.

# Code documentation style

This project will use [Sphinx](https://pythonhosted.org/an_example_pypi_project/sphinx.html).

# License

This package is open-sourced software licensed under the MIT license.

# Credit

[saochishti](https://github.com/soachishti) - https://github.com/soachishti/pyScanLib

[chmuche](https://github.com/chmuche) - https://github.com/ndp-systemes/pyScanLib (multi-page scan code)

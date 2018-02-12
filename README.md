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


# How to build

1. Run `python setup.py py2exe`
2. Once compiled, navigate to `dist`, and open `app.exe`.

If you plan to take app.exe somewhere else, it must have the folder 'cert' next to it 
with the certificate files.

# Reason this repo exists

Often times web-applications would benefit from the ability to connect to a scanner.

This is virtually impossible if we take a direct route to the scanner via a DLL located in 
the client's computer, because a web browser does not have permission to utilize such resources.

1. However, Internet Explorer has ActiveX features which allows you to communicate directly
with DLLs. But that is propriety code and limited to IE, not to mention all the security 
problems with it.

2. Using Java applets, we can communicate directly with DLLs. Except, the support of Java
applets is dying and as of lately Google totally removed the support for it, rendering it useless.

3. Silverlight / Flash... no.

# Solution

Have a 'Web Agent' which acts as a local server that accepts HTTP requests.

Based on the HTTP requests, we call the appropiate DLL or execute commands.

**A web agent is a link between the browser and the internals of the computer.**

Further read: https://wicg.github.io/webusb/ - Chrome's WebUSB API. This also limited to Chrome.

# What is happening

This web agent, when executed, opens a web server on port `8087`, such as navigating to
`https://localhost:8087` will allow you to communicate with the app and return the
appropriate response.

# Roadmap

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

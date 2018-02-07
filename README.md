
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

# How to build

1. Run `python setup.py py2exe`
2. Once compiled, navigate to `dist`, and open `app.exe`.

If you plan to take app.exe somewhere else, it must have the folder 'cert' next to it 
with the certificate files.

# Usage

In your web applications, call an ajax GET request to:

`https://localhost:8087/scan`

The response will be a base64 encoded JPG image.
  

# Disclaimer

Be warned, I'm a rookie in Python.

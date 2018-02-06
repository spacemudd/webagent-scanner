Be warned, I'm a rookie in Python.

The plan is to have a Web Agent which would allow web applications served in internet browsers to call via Ajax a scan command.

For example, calling `https://localhost:8087/scan` via Ajax will call the TWAIN DLL and actually trigger the scanner to scan. The returned reuslt of that route would be the scanned image.

Usage:

1. Navigate to the folder and execute `setup.py install`
2. Navigate to the folder and execute `app.py`
3. In your web application, call `https://localhost:8087/scan`
4. The HTTP response is an image type of jpeg, it is the scanned image.

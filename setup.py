from distutils.core import setup
import py2exe

setup(
  name = 'webagent-scanner',
  packages = ['webagent-scanner'], # this must be the same as the name above
  version = 'v1.0',
  description = 'Web-agent scanner allowing web applications to take advantage of USB scanners via TWAIN',
  author = 'Shafiq al-Shaar',
  author_email = 'shafiqalshaar@gmail.com',
  url = 'https://github.com/spacemudd/webagent-scanner',
  install_requires = ['pyinstaller', 'image', 'tornado', 'wxPython'],
  license='MIT',
)

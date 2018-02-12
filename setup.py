from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')

setup(
  name = 'pyScanLib',
  packages = ['pyScanLib'], # this must be the same as the name above
  version = 'v1.0',
  description = 'An combination of Twain and SANE API',
  author = 'soachishti',
  author_email = 'soachishti@outlook.com',
  url = 'https://github.com/soachishti/pyScanLib', # use the URL to the github repo
  download_url = 'https://github.com/soachishti/pyScanLib/archive/v1.0.tar.gz', # I'll explain this in a second
  keywords = ['scanning', 'scanner', 'twain', 'sane'], # arbitrary keywords
  classifiers = [],
)

setup_dict = dict(
    options={'py2exe': {'bundle_files': 1, 'compressed': True, 'dll_excludes': ["MSVCP90.dll"]}},
    windows=[{'script': "app.py", 'icon_resources': [(1, '24x24.ico')]}],
    # console = ['app.py'],
    zipfile=None,
)
setup(**setup_dict)
setup(**setup_dict)

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

setup(
    #options = {'py2exe': {'bundle_files': 1, 'compressed': True}},
    # windows = [{'script': "app.py"}],
    console = ['app.py'],
    #zipfile = None,
)

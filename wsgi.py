import os

from deals import create_app


path = os.path.abspath(os.path.dirname(__file__))
config = os.path.join(path, 'config.py')
app = create_app(config)


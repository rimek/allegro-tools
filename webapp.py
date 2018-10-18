import os

from web.app import run

run(port=os.environ.get('PORT', 8000))

import logging
import sys

# This is running via apache, so reroute stream to stderr
logging.basicConfig(stream=sys.stderr)

from bestsellers import app as application

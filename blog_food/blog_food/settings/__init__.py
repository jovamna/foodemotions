from .base import *
import os


if os.environ.get("ENV_NAME") == 'production':
    from .production import *
elif os.environ.get("ENV_NAME") == 'test':
    from .test import *
else:
    from .development import *

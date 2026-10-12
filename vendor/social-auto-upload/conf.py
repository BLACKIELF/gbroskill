import os
from pathlib import Path
BASE_DIR = Path(__file__).parent.resolve()
XHS_SERVER = os.environ.get('GBRO_XHS_SERVER', 'http://127.0.0.1:11901')
LOCAL_CHROME_PATH = os.environ.get('GBRO_CHROME', '')
LOCAL_CHROME_HEADLESS = True
DEBUG_MODE = False
YT_PROXY = os.environ.get('GBRO_YT_PROXY') or None

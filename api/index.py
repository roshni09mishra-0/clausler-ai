import os
import sys

# Add parent directory to path so engine and modules are found
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import app

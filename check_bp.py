import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

try:
    from app.routes import main
    print(f"Main is: {main}")
    print(f"Type: {type(main)}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

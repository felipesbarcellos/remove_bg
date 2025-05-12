"""
Preload models for rembg to improve startup time
"""

import os
import sys
import time
from pathlib import Path


def preload_models():
    """
    Preload rembg models to avoid timeout during first request
    Uses a timeout to avoid hanging the startup process
    """
    start_time = time.time()
    print("Preloading rembg models...")

    try:
        # Import rembg and preload the model
        from rembg import new_session

        # Create a session which will load the model - u2net is mais leve que u2netp
        _ = new_session("u2net")

        elapsed = time.time() - start_time
        print(f"Models preloaded successfully in {elapsed:.2f} seconds")
        return True
    except Exception as e:
        print(f"Error preloading models: {e}")
        return False


if __name__ == "__main__":
    success = preload_models()
    sys.exit(0 if success else 1)

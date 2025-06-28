import importlib
import sys

REQUIRED_PACKAGES = [
    'boto3',
    'yaml'  # This refers to PyYAML; imported as 'yaml'
]

def check_dependencies():
    missing = []
    for pkg in REQUIRED_PACKAGES:
        try:
            importlib.import_module(pkg)
        except ModuleNotFoundError:
            missing.append(pkg)

    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print("➡️ Install them using:")
        print(f"   pip install {' '.join('pyyaml' if p == 'yaml' else p for p in missing)}")
        sys.exit(1)
    else:
        print("✅ All required dependencies are installed.")

if __name__ == '__main__':
    check_dependencies()
import sys
import importlib

def check_python_version():
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("Попередження: потрібна версія Python >= 3.10")

def check_package(package_name: str) -> bool:
    try:
        module = importlib.import_module(package_name)
        version = getattr(module, '__version__', 'невідома')
        print(f"  {package_name}: {version} ✓")
        return True
    except ImportError:
        print(f"  {package_name}: НЕ ВСТАНОВЛЕНО ✗")
        return False

def main():
    check_python_version()
    print("\nВстановлені пакети:")
    packages = ['django', 'flask']
    results = {pkg: check_package(pkg) for pkg in packages}
    installed_count = sum(results.values())
    missing_count = len(packages) - installed_count
    print(f"\nВстановлено: {installed_count}, Відсутні: {missing_count}")
    if missing_count > 0:
        print("Команда для встановлення: pip install django flask")

if __name__ == "__main__":
    main()

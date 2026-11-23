import subprocess
import sys
import json
import importlib

def get_installed_packages() -> list[dict]:
    result = subprocess.run(
        [sys.executable, '-m', 'pip', 'list', '--format=json'],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)

def generate_requirements(packages: list[dict], filename: str = 'requirements.txt'):
    skip = {'pip', 'setuptools', 'wheel'}
    with open(filename, 'w', encoding='utf-8') as f:
        for pkg in packages:
            if pkg['name'].lower() not in skip:
                f.write(f"{pkg['name']}=={pkg['version']}\n")

def check_package(package_name: str) -> bool:
    try:
        importlib.import_module(package_name.replace('-', '_'))
        return True
    except ImportError:
        return False

def verify_requirements(filename: str = 'requirements.txt') -> bool:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                pkg_name = line.split('==')[0].strip()
                if not check_package(pkg_name):
                    return False
        return True
    except FileNotFoundError:
        return False

def main():
    packages = get_installed_packages()
    print(f"Знайдено {len(packages)} встановлених пакетів\n")
    for pkg in packages[:10]:
        print(f"  {pkg['name']}=={pkg['version']}")
    if len(packages) > 10:
        print(f"  ... та ще {len(packages) - 10}")
    
    generate_requirements(packages)
    print(f"\nФайл requirements.txt створено")
    
    ok = verify_requirements()
    print(f"Перевірка залежностей: {'✓ Усе OK' if ok else '✗ Є розбіжності'}")

if __name__ == "__main__":
    main()

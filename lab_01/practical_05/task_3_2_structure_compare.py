import os

def scan_directory(path: str, prefix: str = '') -> list[str]:
    tree = []
    ignore = {'__pycache__', '.pyc', 'venv', 'venv2', 'db.sqlite3', '.git'}
    try:
        items = sorted(os.listdir(path))
    except PermissionError:
        return tree
    
    for i, item in enumerate(items):
        if item in ignore or item.endswith('.pyc'):
            continue
        is_last = (i == len(items) - 1)
        connector = "└── " if is_last else "├── "
        tree.append(f"{prefix}{connector}{item}")
        
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            extension = "    " if is_last else "│   "
            tree.extend(scan_directory(item_path, prefix + extension))
    return tree

def analyze_project(path: str) -> dict:
    stats = {'py_files': 0, 'html_files': 0, 'css_files': 0, 'total_size': 0, 'directories': 0}
    ignore = {'__pycache__', 'venv', 'venv2', '.git'}
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in ignore]
        stats['directories'] += len(dirs)
        for file in files:
            if file.endswith('.pyc'):
                continue
            file_path = os.path.join(root, file)
            stats['total_size'] += os.path.getsize(file_path)
            if file.endswith('.py'):
                stats['py_files'] += 1
            elif file.endswith('.html'):
                stats['html_files'] += 1
            elif file.endswith('.css'):
                stats['css_files'] += 1
    return stats

def compare_projects(django_path: str, flask_path: str):
    print("=" * 60)
    print("ПОРІВНЯННЯ СТРУКТУРИ ПРОЕКТІВ")
    print("=" * 60)
    
    print(f"\n--- Django ({django_path}) ---")
    for line in scan_directory(django_path):
        print(line)
    django_stats = analyze_project(django_path)
    
    print(f"\n--- Flask ({flask_path}) ---")
    for line in scan_directory(flask_path):
        print(line)
    flask_stats = analyze_project(flask_path)
    
    print("\n" + "=" * 60)
    print(f"{'Характеристика':<20} | {'Django':<10} | {'Flask':<10}")
    print("-" * 60)
    print(f"{'Файли .py':<20} | {django_stats['py_files']:<10} | {flask_stats['py_files']:<10}")
    print(f"{'Файли .html':<20} | {django_stats['html_files']:<10} | {flask_stats['html_files']:<10}")
    print(f"{'Файли .css':<20} | {django_stats['css_files']:<10} | {flask_stats['css_files']:<10}")
    print(f"{'Каталоги':<20} | {django_stats['directories']:<10} | {flask_stats['directories']:<10}")
    print(f"{'Розмір (байт)':<20} | {django_stats['total_size']:<10} | {flask_stats['total_size']:<10}")

def main():
    django_path = 'mysite'
    flask_path = 'myflaskapp'
    for path in [django_path, flask_path]:
        if not os.path.isdir(path):
            print(f"Каталог '{path}' не знайдено.")
            return
    compare_projects(django_path, flask_path)

if __name__ == "__main__":
    main()

import os
import sys
import re

def analyze_settings(settings_path: str) -> dict:
    with open(settings_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    debug_match = re.search(r"DEBUG\s*=\s*(True|False)", content)
    apps_match = re.search(r"INSTALLED_APPS\s*=\s*\[(.*?)\]", content, re.DOTALL)
    db_match = re.search(r"DATABASES\s*=\s*\{.*?'ENGINE':\s*'(.*?)'.*?\}", content, re.DOTALL)
    lang_match = re.search(r"LANGUAGE_CODE\s*=\s*['\"](.*?)['\"]", content)
    tz_match = re.search(r"TIME_ZONE\s*=\s*['\"](.*?)['\"]", content)

    return {
        "DEBUG": debug_match.group(1) if debug_match else "Не знайдено",
        "INSTALLED_APPS": "Список додатків" if apps_match else "Не знайдено",
        "DATABASES": db_match.group(1).split('.')[-1] if db_match else "Не знайдено",
        "LANGUAGE_CODE": lang_match.group(1) if lang_match else "Не знайдено",
        "TIME_ZONE": tz_match.group(1) if tz_match else "Не знайдено",
    }

def check_security(settings_path: str) -> list[str]:
    warnings = []
    with open(settings_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if re.search(r"DEBUG\s*=\s*True", content):
        warnings.append("DEBUG = True (небезпечно для production)")
    if not re.search(r"os\.environ\.get\(['\"]SECRET_KEY['\"]", content) and re.search(r"SECRET_KEY\s*=\s*['\"].*?['\"]", content):
        warnings.append("SECRET_KEY захардкоджений у файлі")
    if re.search(r"ALLOWED_HOSTS\s*=\s*\[\s*\]", content):
        warnings.append("ALLOWED_HOSTS порожній")
    
    return warnings

def main():
    settings_path = 'mysite/mysite/settings.py'
    if not os.path.exists(settings_path):
        print(f"Файл {settings_path} не знайдено")
        sys.exit(1)
    
    config = analyze_settings(settings_path)
    print("=== Аналіз конфігурації Django ===\n")
    for key, value in config.items():
        print(f"  {key}: {value}")
    
    print("\n=== Перевірка безпеки ===\n")
    warnings = check_security(settings_path)
    if warnings:
        for w in warnings:
            print(f"  ⚠ {w}")
    else:
        print("  Попереджень не знайдено")

if __name__ == "__main__":
    main()

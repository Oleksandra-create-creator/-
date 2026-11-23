import random
import urllib.request


def generate_code():
    return f"BK-{random.randint(1000, 9999)}"


def notify_external(title: str) -> int:
    with urllib.request.urlopen(f"https://api.example.com/notify?title={title}", timeout=5) as response:
        return response.status

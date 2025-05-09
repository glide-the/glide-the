import requests
from datetime import datetime

API_URL = "https://zenquotes.io/api/random"

def fetch_online_motto():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            quote = data[0]["q"]
            author = data[0]["a"]
            return f'{quote} — {author}'
        else:
            return "Be kind. Stay curious."
    except Exception as e:
        print(f"[ERROR] Fetching motto failed: {e}")
        return "Fallback to local wisdom."

def update_readme():
    with open("README.md", "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_motto = fetch_online_motto()
    start, end = None, None

    for i, line in enumerate(lines):
        if line.strip().startswith(">") and start is None:
            start = i
        elif start is not None and (line.strip() == "" or line.strip().startswith("*(Want")):
            end = i
            break

    if start is not None and end is not None:
        lines[start:end] = [f'> “{new_motto}”\n']

    with open("README.md", "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"[{datetime.now()}] Updated motto: {new_motto}")

if __name__ == "__main__":
    update_readme()

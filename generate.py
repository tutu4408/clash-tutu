import requests
import yaml

BASE = yaml.safe_load(open("base.yaml", encoding="utf-8"))
BASE["proxies"] = []
group = BASE["proxy-groups"][0]["proxies"]

def load_yaml(url):
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    return yaml.safe_load(r.text)

with open("sources.txt", encoding="utf-8") as f:
    urls = [i.strip() for i in f if i.strip() and not i.startswith("#")]

for url in urls:
    try:
        data = load_yaml(url)
        proxies = data.get("proxies", [])
        for p in proxies:
            BASE["proxies"].append(p)
            group.append(p["name"])
        print("OK:", url)
    except Exception as e:
        print("FAIL:", url, e)

with open("clash.yaml", "w", encoding="utf-8") as f:
    yaml.dump(BASE, f, allow_unicode=True)

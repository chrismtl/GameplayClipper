import json

_cache = {}

def load(json_path):
    global _cache
    if json_path not in _cache:
        with open(json_path, "r", encoding="utf-8") as f:
            _cache[json_path] = json.load(f)
    return _cache[json_path]

def refresh(json_path):
    global _cache
    with open(json_path, "r", encoding="utf-8") as f:
        _cache[json_path] = json.load(f)

def update(json_path, data):
    global _cache
    _cache[json_path] = data
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def clear(json_path=None):
    global _cache
    if json_path:
        _cache.pop(json_path, None)
    else:
        _cache.clear()

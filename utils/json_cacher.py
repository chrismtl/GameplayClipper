import json

_js_cache = {}

def load(json_path):
    global _js_cache
    if json_path not in _js_cache:
        with open(json_path, "r", encoding="utf-8") as f:
            _js_cache[json_path] = json.load(f)
    return _js_cache[json_path]

def refresh(json_path):
    global _js_cache
    with open(json_path, "r", encoding="utf-8") as f:
        _js_cache[json_path] = json.load(f)

def update(json_path, data):
    global _js_cache
    _js_cache[json_path] = data
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def clear(json_path=None):
    global _js_cache
    if json_path:
        _js_cache.pop(json_path, None)
    else:
        _js_cache.clear()

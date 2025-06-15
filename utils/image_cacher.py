import cv2

_img_cache = {}

def load(image_path, flags=cv2.IMREAD_COLOR):
    """
    Load an image using imgc.load and cache it.
    If already cached, returns the cached version.
    """
    cached = _img_cache.get(image_path)
    if cached is not None:
        return cached

    img = cv2.imread(image_path, flags)
    if img is None:
        raise FileNotFoundError(f"❌ Could not load image: {image_path}")
    
    _img_cache[image_path] = img
    return img

def clear(image_path=None):
    """Clear the cache for one image or all."""
    global _img_cache
    if image_path:
        _img_cache.pop(image_path, None)
    else:
        _img_cache.clear()

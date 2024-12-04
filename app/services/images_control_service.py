def verify_image_size(image_bytes, max_size=5 * 1024 * 1024):
    if image_bytes and len(image_bytes) > max_size:
        raise ValueError("La imagen excede el tamaño máximo permitido.")
    return image_bytes

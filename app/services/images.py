def verify_image_size(image_bytes, max_size=5 * 1024 * 1024):
    if len(image_bytes) > max_size:
        raise ValueError("La imagen excede el tamaño máximo permitido.")
    print(f"tamaño de la imagen: {len(image_bytes)}")
    return image_bytes

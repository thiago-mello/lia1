def get_image_url(image_object):
    image = next(
        (i for i in image_object['sizes'] if i['type'] == 'display'), None)
    return image['url'] if image else None

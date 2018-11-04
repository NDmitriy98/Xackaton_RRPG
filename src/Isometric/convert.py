def cart_to_iso(cart_x, cart_y):
    return cart_x - cart_y, (cart_x + cart_y)/2


def iso_to_cart(iso_x, iso_y):
    return (iso_x + 2*iso_y)/2, (2*iso_y - iso_x)/2
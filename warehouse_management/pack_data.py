def pack(data_create, order_id):
    product_id_list = data_create.get("product_id[]")
    quantity_list = data_create.get("quantity[]")
    order_item_data = list(zip(product_id_list, quantity_list, strict=True))
    packed_data = []
    for product_id, quantity in order_item_data:
        order_element = {
            'product_id': int(product_id),
            'order_id': order_id,
            'quantity': int(quantity)
        }
        packed_data.append(order_element)
    return packed_data

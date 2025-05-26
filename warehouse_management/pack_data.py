def pack(data_create, order_id):
    product_id_data = data_create.get("product_ids_data")
    quantity_data = data_create.get("quantity_data")
    order_item_data = list(zip(product_id_data, quantity_data, strict=True))
    packed_data = []
    for product_id, quantity in order_item_data:
        order_item_data = {
            'product_id': int(product_id),
            'order_id': order_id,
            'quantity': int(quantity)
        }
        packed_data.append(order_item_data)
    return packed_data

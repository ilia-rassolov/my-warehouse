def validate(product_data):
    errors = ""
    price = int(product_data.get('price'))
    stock = int(product_data.get('stock', int))
    if not isinstance(price, int) or price > int(2**31 - 1) or price <= 0:
        errors = "Цена указана некорректно"
    elif not isinstance(stock, int) or stock > 2**31 - 1 or stock < 0:
        errors = " Остаток указан некорректно"
    return errors


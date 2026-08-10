raw_phones = [
    {"phone_code": "P301", "brand": "apple", "price": 25000000, "status": "available"},
    {"phone_code": " p101 ", "brand": "samsung", "price": 12000000, "status": "available"},
    {"phone_code": "P202", "brand": "xiaomi", "price": 8000000, "status": "sold"},
    {"phone_code": "P102", "brand": "samsung", "price": 9500000, "status": "reserved"},
    {"phone_code": "P302", "brand": "apple", "price": 28000000, "status": "available"}
]

def clean_and_validate_phones(raw_phones_data):
    valid_phones = []
    for phone in raw_phones_data:
        new_phone = phone.copy()
        code = new_phone.get("phone_code", "").strip().upper()
        if len(code) >= 2 and code[0] == 'P' and code[1].isdigit():
            new_phone["phone_code"] = code
            valid_phones.append(new_phone)
    return valid_phones

def search_phones(phones, max_price, status=None):
    result = []
    for phone in phones:
        if phone["price"] <= max_price:
            if status is None or phone["status"] == status:
                result.append(phone)
    return result

def sort_phones_by_price_desc(phones):
    n = len(phones)
    for i in range(n):
        for j in range(0, n - i - 1):
            if phones[j]["price"] < phones[j + 1]["price"]:
                phones[j], phones[j + 1] = phones[j + 1], phones[j]
    return phones
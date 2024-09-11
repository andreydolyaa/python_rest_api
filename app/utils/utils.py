def parse_objectid(item: dict) -> dict:
    if "_id" in item:
        item["_id"] = str(item["_id"])
        item["id"] = item["_id"]
    return item

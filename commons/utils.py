

def getdefault(data: dict, key, default):
    return default if not data.__contains__(key) else data[key]


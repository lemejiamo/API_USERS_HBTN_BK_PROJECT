import hashlib

def hash_attribute(value: str, type: str = 'md5') -> str:
    _hash: any
    if (type == 'md5'):
        _hash = hashlib.md5()
    elif (type == 'sha256'):
        _hash = hashlib.sha256()
    elif (type == 'sha512'):
        _hash = hashlib.sha512()
    else:
        print("invalid type of hash please  choose one of 'md5', 'sha256', 'sha512'")
        return None
    _hash.update(value.encode('utf-8'))
    hash_value =_hash.hexdigest()
    return hash_value
import mmh3
import xxhash
import hashlib

def murmurhash(input_value):
    hash_value = mmh3.hash(str(input_value))
    return hash_value


def sha_256(message):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(message.encode('utf-8'))
    hash_value = sha256_hash.hexdigest()
    return hash_value


def sha3_256(data):
    sha3_hash = hashlib.sha3_256()
    sha3_hash.update(data.encode('utf-8'))
    hash_value = sha3_hash.hexdigest()
    return hash_value


def xxhash32(data):
    hasher = xxhash.xxh32()
    hasher.update(data.encode('utf-8'))
    hash_value = hasher.intdigest()
    return hash_value

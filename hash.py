import hashlib
import string

def hash_url(url, precision=10):
    alphabet = string.digits + string.ascii_letters
    base = len(alphabet)

    def num62(num):
        if num // base > 0:
            return num62(num // base) + alphabet[num % base]
        else:
            return alphabet[num]

    return num62(int(hashlib.md5(url.encode("UTF-8")).hexdigest(), 16) % (10 ** precision))


if __name__ == "__main__":
    u = 'www.google.com'
    print(hash_url(u))

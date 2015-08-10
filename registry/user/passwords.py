
import base64
import hmac
import hashlib

def generate_sha512_hmac(password_salt, password):
    """
    Generate SHA512 HMAC
    """
    return base64.b64encode(hmac.new(password_salt, password.encode('utf8'), hashlib.sha512).digest())

def hash_password(user_manager, password):
    password = generate_sha512_hmac(user_manager.password_salt, password)
    hashed_password =  user_manager.password_crypt_context.encrypt(password)
    return hashed_password

def verify_password(user_manager, password, hashed_password):
    password = generate_sha512_hmac(user_manager.password_salt, password)
    return user_manager.password_crypt_context.verify(password, hashed_password)

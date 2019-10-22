"""
The cipher module: Encrypts and Decrypts any string using a key.

These functions help to create salt which is then used for creating secure
keys for ciphering using HMAC algorithm as described by RFC 2104. In
addition to that these functions help with encrypting and decrypting a string.

At a glance, the structure of the module is following:
 - keygen():            Generates key with salt and stores it within an
                        environment variable. This key or password is the
                        master password that would be used with the other
                        encrypt and decrypt functions. Hence do not forget.
 - encrypt():           Encrypts a string using the key generated by `keygen`
                        function. The encrypted output is in string format
                        instead of bytes. You can read how to change it in the
                        function docstring.
 - decrypt():           Decrypts an encrypted-string using the key generated
                        by `keygen` function. Function takes string input for
                        decryption. However if you pass bytes text you need to
                        change `encrypted_text.encode()` to `encrypted_text`.

See https://github.com/xames3/charlotte for cloning the repository.
"""
#   History:
#
#   < Checkout my github repo for history and latest stable build >
#
#   1.1.1 - Improved the type hints by using the typing module.
#   1.0.2 - Reduced unnecessary use of "`" in comments for simplicity.
#   1.0.0 - First code.

from inspect import stack
from sys import exc_info
from typing import Optional, Text, Union

# Constant used by `keygen`, `encrypt` and `decrypt` to use default UTF-8
# encoding.
_ENCODING = 'utf-8'
# Constant used by `keygen` to set default key name in environment variables
# if no key name is given.
_KEY_NAME = 'ADMIN_USER_KEY'


def keygen(key_name: Text,
           passcode: Text,
           return_key: Optional[bool] = None) -> Union[None, Text]:
    """Generates key.

    key_name:   The name with which the key needs to be stored in as an
                environment variable.
    passcode:   The password that you would like to encrypt using salt.
    return_key: If made True, it will return the key an then save it in
                an environment variable.

    Generates key with salt and stores it within an environment variable.

    Caution: This key or password is the master password that would be used
    with the other encrypt and decrypt functions. Hence do not forget.
    """
    # You can find the reference code here:
    # https://nitratine.net/blog/post/encryption-and-decryption-in-python/
    from base64 import urlsafe_b64encode
    from os import urandom
    from subprocess import PIPE, Popen
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.hashes import SHA512
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

    try:
        # Converting the input string into bytes.
        password = passcode.encode()
        # Creating a salt for encryption.
        # Using SHA512 hashing algorithm, you can use SHA128 or SHA256 as well.
        kdf = PBKDF2HMAC(algorithm=SHA512(),
                         length=32,
                         salt=urandom(128),
                         iterations=100000,
                         backend=default_backend())
        # Generating encrypted and salted key but changing it to str format so
        # that it can be stored in an environment variable. This is a personal
        # preference.
        key = urlsafe_b64encode(kdf.derive(
            password)).decode(encoding=_ENCODING)
        if key_name is None:
            key_name = _KEY_NAME
        Popen(f"setx {key_name} {key}",
              stdout=PIPE,
              shell=True)
        if return_key is True:
            return key
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} in function "{stack()[0][3]}" on line'
              f' {exc_info()[-1].tb_lineno}.')


def encrypt(message: Text, key: Text) -> Text:
    """Encrypts message.

    message: String to be encrypted.
    key:     Key that will be used for encrypting the message.

    Encrypts a string using the key generated by `keygen` function.
    The encrypted output is in string format instead of bytes.

    Note: You can choose to return the encrypted text if you want to. Just
    change `encode.decode()` to `encode` but make sure you update the code in
    `decrypt` function as well.
    """
    from cryptography.fernet import Fernet

    try:
        # Similar to `keygen`, converting the string message to bytes.
        to_encode = message.encode()
        # Encrypting the message using the Fernet key.
        fernet_key = Fernet(key.encode(encoding=_ENCODING))
        encode = fernet_key.encrypt(to_encode)
        super_encode = fernet_key.encrypt(encode)
        return super_encode.decode()
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} in function "{stack()[0][3]}" on line'
              f' {exc_info()[-1].tb_lineno}.')


def decrypt(encrypted_text: Text, key: Text) -> Text:
    """Decrypts message.

    encrypted_text: Encrypted text that needs to be decrypted.
    key:            Key that will be used for decrypting the message.

    Decrypts an encrypted-string using the key generated by `keygen` function.
    The decrypted output is in string format.

    Note: Function takes string input for decryption. However if you pass bytes
    text you need to change `encrypted_text.encode()` to `encrypted_text`.
    Make sure you update the code in `encrypt` function as well if you make any
    changes here.
    """
    from cryptography.fernet import Fernet

    try:
        # Decrypting the message using the Fernet key.
        fernet_key = Fernet(key.encode(encoding=_ENCODING))
        decode = fernet_key.decrypt(encrypted_text.encode())
        super_decode = fernet_key.decrypt(decode)
        return super_decode.decode()
    except Exception as error:
        print('An error occured while performing this operation because of'
              f' {error} in function "{stack()[0][3]}" on line'
              f' {exc_info()[-1].tb_lineno}.')

import os
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.padding import OAEP, MGF1
from cryptography.hazmat.backends import default_backend


class SLE:
    def __init__(self):
        # إنشاء مفتاح RSA
        self.private_key = rsa.generate_private_key(
            public_exponent=65537, key_size=2048, backend=default_backend()
        )
        self.public_key = self.private_key.public_key()

    def encrypt(self, data):
        """تشفير البيانات باستخدام AES وRSA"""
        aes_key = os.urandom(32)  # مفتاح AES
        iv = os.urandom(16)  # IV للتشفير

        # تشفير البيانات باستخدام AES
        cipher = Cipher(
            algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend()
        )
        padder = PKCS7(128).padder()
        padded_data = padder.update(data) + padder.finalize()
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        # تشفير مفتاح AES باستخدام RSA
        encrypted_aes_key = self.public_key.encrypt(
            aes_key,
            OAEP(
                mgf=MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

        # دمج البيانات (مفتاح AES المشفر + IV + النص المشفر)
        return encrypted_aes_key + iv + encrypted_data

    def save_to_file(self, filename, encrypted_data):
        """حفظ البيانات المشفرة في ملف بصيغة مخصصة"""
        with open(filename, "wb") as file:
            file.write(encrypted_data)

    def generate_file(self, filename, data):
        """إنشاء ملف يحتوي على بيانات مشفرة"""
        encrypted_data = self.encrypt(data)
        self.save_to_file(filename, encrypted_data)

    def read_file(self, filename):
        """قراءة البيانات من الملف"""
        with open(filename, "rb") as file:
            return file.read()

    def decrypt(self, encrypted_combined_data):
        """فك تشفير البيانات"""
        # استخراج مفتاح AES المشفر + IV + النص المشفر
        encrypted_aes_key = encrypted_combined_data[
            :256
        ]  # طول مفتاح RSA المشفر 256 بايت
        iv = encrypted_combined_data[256:272]  # IV طوله 16 بايت
        encrypted_data = encrypted_combined_data[272:]  # النص المشفر

        # فك تشفير مفتاح AES باستخدام RSA
        aes_key = self.private_key.decrypt(
            encrypted_aes_key,
            OAEP(
                mgf=MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

        # فك تشفير النص باستخدام AES
        cipher = Cipher(
            algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend()
        )
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

        unpadder = PKCS7(128).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()
        return data


# استخدام الكلاس
# if __name__ == "__main__":
#     sle = SLE()

#     # بيانات نصية لتحويلها إلى تنسيق مشابه للمثال
#     secret_data = b"""
#     filename = "secure_file.sle"
#     sle.generate_file(filename, secret_data)

#     print(f"done create {filename} successful")

#     encrypted_data = sle.read_file(filename)
#     decrypted_data = sle.decrypt(encrypted_data)

#     print(f"Original data:\n{decrypted_data.decode('utf-8')}")
# """

#     # إنشاء ملف بتنسيق خاص
#     filename = "secure_file.sle"
#     sle.generate_file(filename, secret_data)

#     print(f"done create {filename} successful!")

#     # قراءة وفك التشفير
#     encrypted_data = sle.read_file(filename)
#     decrypted_data = sle.decrypt(encrypted_data)

#     print(f"original data:\n{decrypted_data.decode('utf-8')}")

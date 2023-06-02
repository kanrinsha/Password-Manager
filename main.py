# !/usr/bin/env python3
import yaml
from cryptography.fernet import Fernet


class Vault:
    def vault_pass(self):
        self.name = input("Name: ")
        self.user = input("Username: ")
        self.password = input("Password: ")
        self.note = input("Note? (leave blank if N/A): ")

        while True:
            self.do_encrypt = input("Encrypt? Y/N: ").lower()
            if self.do_encrypt == "y":
                break
            elif self.do_encrypt == "n":
                break

        if self.do_encrypt == "y":
            is_encrypted = input("Encryption key: ")
            self.cipher_suite = Fernet(str.encode(is_encrypted))

            encoded_note = str(self.cipher_suite.encrypt(str.encode(self.note)).decode('utf-8'))
            encoded_user = str(self.cipher_suite.encrypt(str.encode(self.user)).decode('utf-8'))
            encoded_pass = str(self.cipher_suite.encrypt(str.encode(self.password)).decode('utf-8'))

            self.new_vault_entry = {
                self.name: {
                    'note': encoded_note,
                    'username': encoded_user,
                    'password': encoded_pass
                }
            }
        else:
            self.new_vault_entry = {
                self.name: {
                    'note': self.note,
                    'username': self.user,
                    'password': self.password
                }
            }
        # overwrite
        with open('vault.yml', 'r') as yaml_file_read:
            data = yaml.safe_load(yaml_file_read)
            if self.do_encrypt == "y":
                if data is not None and self.name in data:
                    while True:
                        do_overwrite = input("Name already exists, overwrite? Y/N: ").lower()
                        if do_overwrite == "y":
                            encoded_note = str(self.cipher_suite.encrypt(str.encode(self.note)).decode('utf-8'))
                            encoded_user = str(self.cipher_suite.encrypt(str.encode(self.user)).decode('utf-8'))
                            encoded_pass = str(self.cipher_suite.encrypt(str.encode(self.password)).decode('utf-8'))

                            data[self.name] = {
                                'note': encoded_note,
                                'username': encoded_user,
                                'password': encoded_pass
                            }

                            with open('vault.yml', 'w') as yaml_file:
                                yaml.safe_dump(data, yaml_file)
                            return
                        elif do_overwrite == "n":
                            return
            else:
                if data is not None and self.name in data:
                    while True:
                        do_overwrite = input("Name already exists, overwrite? Y/N: ").lower()
                        if do_overwrite == "y":
                            data[self.name] = {
                                    'note': self.note,
                                    'username': self.user,
                                    'password': self.password
                                }

                            with open('vault.yml', 'w') as yaml_file:
                                yaml.safe_dump(data, yaml_file)
                            return
                        elif do_overwrite == "n":
                            return
        # write
        with open('vault.yml', 'a') as yaml_file:
            yaml.safe_dump(self.new_vault_entry, yaml_file)

    def get_pass(self):
        self.key_to_get = input("Name to get: ")
        is_encrypted = input("Encryption key? (leave blank if none): ")

        with open('vault.yml', 'r') as file:
            data = yaml.safe_load(file)

        if len(is_encrypted) > 1:
            self.cipher_suite = Fernet(is_encrypted)

            if data is not None and self.key_to_get in data:
                for x in data[self.key_to_get]:
                    print(str(self.cipher_suite.decrypt(data[self.key_to_get][x]).decode('utf-8')))
            else:
                print(f"{self.key_to_get} is not found")
        else:
            if data is not None and self.key_to_get in data:
                print("\n" + yaml.safe_dump(data[self.key_to_get]))
            else:
                print(f"{self.key_to_get} is not found")

    def __init__(self):
        self.note = None
        self.password = None
        self.user = None
        self.name = None
        self.key_to_get = None
        self.do_encrypt = None
        self.cipher_suite = None
        self.new_vault_entry = None
        print("""   
   _____                     __  .__                
  /  _  \   ____   _______/  |_|__| ____    ____  
 /  /_\  \ /  _ \ /  ___/\   __\  |/    \  / ___\ 
/    |    (  <_> )\___ \  |  | |  |   |  \/ /_/  >
\____|__  /\____/____  > |__| |__|___|  /\___  / 
        \/           \/               \//_____/  

           """)


def generate_key():
    with open('key.yml', 'r') as file:
        data = yaml.safe_load(file)

    if data is not None:
        print("Key already exists.")
        return

    new_key = Fernet.generate_key().decode('utf-8')
    print(f"YOUR PASSKEY IS {new_key} DON'T FORGET THIS")
    with open('key.yml', 'w') as yaml_file:
        yaml.safe_dump(new_key, yaml_file)


def get_key():
    with open('key.yml', 'r') as file:
        data = yaml.safe_load(file)
        print(data)


if __name__ == '__main__':
    vault = Vault()

    print("""To use, follow the instructions below:
To vault a password, press 'v' and provide the necessary details.
To retrieve a password, press 'r' and enter the appropriate credentials.
Press 'g' to generate an encryption key
If using encryption, remember to keep your master password safe and secure, as it is the key to accessing your encrypted vault.
""")

    while True:
        user_input = input(": ").lower()
        if user_input == "v":
            vault.vault_pass()
            break
        elif user_input == "r":
            vault.get_pass()
            break
        elif user_input == "g":
            generate_key()
        elif user_input == "get key":
            get_key()
        else:
            print("Incorrect input.")

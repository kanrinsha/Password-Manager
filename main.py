# !/usr/bin/env python3
import yaml


class Vault:
    def vault_pass(self):
        encryption_key = get_config("key")
        try:
            self.name = input("Name: ")
            self.user = input("Username: ")
            self.password = input("Password: ")
            self.note = input("Note? (leave blank if N/A): ")

            new_vault_entry = {
                self.name: {
                    'note': self.note,
                    'username': self.user,
                    'password': self.password
                }
            }
            # overwrite
            with open('vault.yml', 'r') as yaml_file_read:
                data = yaml.safe_load(yaml_file_read)
                if data is not None and self.name in data:
                    while True:
                        do_overwrite = input("Name already exists, overwrite? Y/N: ")
                        if do_overwrite.lower() == "y":
                            data[self.name] = {
                                    'note': self.note,
                                    'username': self.user,
                                    'password': self.password
                                }

                            with open('vault.yml', 'w') as yaml_file:
                                yaml.safe_dump(data, yaml_file)
                            return
                        elif do_overwrite.lower() == "n":
                            return
                # write
                else:
                    with open('vault.yml', 'a') as yaml_file:
                        yaml.safe_dump(new_vault_entry, yaml_file)

        except Exception as e:
            print(e.args)

    def get_pass(self):
        self.key_to_get = input("Name to get: ")

        with open('vault.yml', 'r') as file:
            data = yaml.safe_load(file)
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
        print("""   
   _____                     __  .__                
  /  _  \   ____   _______/  |_|__| ____    ____  
 /  /_\  \ /  _ \ /  ___/\   __\  |/    \  / ___\ 
/    |    (  <_> )\___ \  |  | |  |   |  \/ /_/  >
\____|__  /\____/____  > |__| |__|___|  /\___  / 
        \/           \/               \//_____/  

           """)


def get_config(key):
    with open('config.yml', 'r') as file:
        return yaml.safe_load(file)[key]


if __name__ == '__main__':
    vault = Vault()

    print("""To use, follow the instructions below:
To vault a password, press 'v' and provide the necessary details.
To retrieve a password, press 'r' and enter the appropriate credentials.
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
        else:
            print("Incorrect input.")

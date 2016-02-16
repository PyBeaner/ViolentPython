import crypt


def testPassword(encrypted_password, salt):
    dictfFile = open('dictionary.txt')
    for word in dictfFile:
        word = word.strip()
        cryptWord = crypt.crypt(word, salt)
        if cryptWord == encrypted_password:
            print("[+] Found Password: ", word)
            return
    print("[-] Password not found.")


def main():
    passFile = open("passwd.txt")
    for line in passFile:
        if ":" in line:
            user = line.split(":")[0]
            encrypted_password = line.split(":")[1].strip()
            # $id$salt$encrypted
            # ID  | Method
            # ─────────────────────────────────────────────────────────
            # 1   | MD5
            # 2a  | Blowfish (not in mainline glibc; added in some Linux distributions)
            # 5   | SHA-256 (since glibc 2.7)
            # 6   | SHA-512 (since glibc 2.7)
            print("[*] Cracking Password for:", user)
            parts = encrypted_password.split("$")
            if len(parts) <= 1:
                print("Password is emtpy for user:", user)
                continue
            ctype = parts[1]
            if ctype == '6':
                print("Hash type SHA-512 detected...")
                salt = encrypted_password.split("$")[2]
                insalt = "$" + ctype + "$" + salt + "$"
                testPassword(encrypted_password, insalt)


if __name__ == '__main__':
    main()

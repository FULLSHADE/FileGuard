from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import gzip
import sys
import hashlib
import uuid
import os
import string
import random

def get_file_hashes(before_compress, after_compress):
    hash_1 = hashlib.md5(open(before_compress,'rb').read()).hexdigest()
    hash_2 = hashlib.md5(open(after_compress,'rb').read()).hexdigest()
    return hash_1, hash_2

def gzip_compress_files(input_file, output_file):
    with open(input_file, "rb") as file_to_compress:
        with gzip.open(output_file, "wb") as file_compressed_out:
            file_compressed_out.writelines(file_to_compress)
        
    hash_1, hash_2 = get_file_hashes(input_file, output_file)   
            
    print("[+] Successfully GZIP compressed file")
    print("[+] Original file - {}".format(hash_1))
    print("[+] Compressed file - {}".format(hash_2))
    
    file_to_compress.close()
    file_compressed_out.close()

def aes_encrypt_files(compressed_file): 
    random_iv = "f" * 16
    random_key = os.urandom(16)
    
    enc_file = AES.new(random_key, AES.MODE_CBC, random_iv.encode())
    
    print("[+] File to encrypt - {}".format(compressed_file))
    
    with open(compressed_file, "rb") as target_file:
        file_data = target_file.read()
        pad_file_data_encrypted = pad(file_data, AES.block_size)
        file_data_encrypted = enc_file.encrypt(pad_file_data_encrypted)
        
    enc_file_name = compressed_file + ".enc"    
    with open(enc_file_name, "wb") as output_file:
        output_file.write(file_data_encrypted)
     
    with open(enc_file_name,'rb') as enc_hash_check:
        enc_data = enc_hash_check.read()
        enc_file_hash = hashlib.md5(enc_data).hexdigest()
         
    print("\t[+] AES Key: {}".format(random_key.hex()))
    print("\t[+] AES IV: {}".format(random_iv))
    print("[+] Encrypted file - {}".format(enc_file_hash))
    print("[+] Encrypted file output - {}".format(enc_file_name))         
      
    target_file.close()
    output_file.close()
    enc_hash_check.close()
    
    return random_key.hex(), enc_file_name

#def xor(data, key): 
#    return bytearray(a^b for a, b in zip(*map(bytearray, [data, key]))) 
    
def enc_hash_append(hex_hash, filename):

    #xor_key = random.choice(string.ascii_letters)
    #xor_result = xor(hex_hash.encode("utf8"), xor_key.encode("utf8"))
    #print("\t[+] Protected AES key with XOR key - {}".format(xor_key))

    with open(filename, "a") as append_hash_file:
        append_hash_file.write(hex_hash)
    append_hash_file.close()
    
    print("[+] Appended AES key to the file")    
    
def main():

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    print("[+] Usage: python PeGuard.py <filein> <fileout>\n" + "_"* 60 + "\n")

    try:
        gzip_compress_files(input_file, output_file)
    except:
        print("[!] Failed to compress file")
    
    try:    
        hash_to_append, enc_filename = aes_encrypt_files(output_file)
    except:
        print("[!] Failed to encrypt file")

    try:    
        enc_hash_append(hash_to_append, enc_filename)
    except:
        print("[!] Failed to appened key")

if __name__ == "__main__":
    main()

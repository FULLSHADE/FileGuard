# PEGUARD

PEGUARD is a file crypter and packing utility. 

This project was originally included as a script in the WARFOX-C2 project found [here](). However, it can work as a standalone packer.

## Description

![image](https://user-images.githubusercontent.com/54753063/147796580-9d2bb0ea-a6a2-4bee-82b5-534e16e562b8.png)

## Technical Details

### PeGuard

PeGuard takes a file as input, compresses it via GZIP, encrypts it using AES-128 (CBC mode) and appends the AES key to the end of the file. This utility was designed to pack the WARFOX DLL implant to aid in its DLL sideloading execution process.

1. You provide an input file (technically any file type should work) as argv[1] and the expected output file as argv[2]
2. PeGuard compresses the input file using GZIP and writes a copy to disk
3. PeGuard encrypts the compressed file using AES-128 in CBC mode with a randomly generated key
    * The AES IV is hardcoded as `ffffffffffffffff` to make the key parsing process of the dropper utility easier, but it could be randomized
4. The AES key is appended to the file so it can be discovered by the dropper utility
5. A copy of the finalized binary is stored in an output text file; the binary is formatted as a BYTE array which can be embedded in the dropper process

### Dropper Utility

This utility is not yet included in this repository. The dropper utility is written in C++ and relies on C++ Boost libraries to perform GZIP decompression and decryption. The following example outlines how the dropper can be used to DLL-sideload the PeGuard packed binary, however PeGuard could be applied elsewhere.

1. The dropper locates the embedded (packed) payload
2. The AES key is recovered from the end of the encrypted file and the buffer is resized to remove the key
3. The key is used to decrypt the packed file via AES
4. Once decrypted, the compressed file is decompressed using Boost::Gzip
5. The final payload is written to disk along-side it's sibling binary
6. The sibling binary (a signed, legitimate binary) is used to DLL-sideload the associated DLL payload

## Example Usage

```
$ python3 PeGuard.py calc.exe calc_packed.exe

[+] Usage: python PeGuard.py <filein> <fileout>
____________________________________________________________

[+] Successfully GZIP compressed file
[+] Original file - 5da8c98136d98deec4716edd79c7145f
[+] Compressed file - 7d8bbaf40e671ef70ca4811007fb7f6e
[+] File to encrypt - calc_packed.exe
        [+] AES Key: 34f88c98cfd49e102c00064577328f3b
        [+] AES IV: ffffffffffffffff
[+] Encrypted file - d2cac6a07e13c4a39620239d0e3a93c8
[+] Encrypted file output - calc_packed.exe.enc
[+] Appended AES key to the file
```

## To-do

- [ ] Strip the GZIP header and set it during the unpacking routine of the dropper utility
- [ ] Fix the XOR routine that encrypts the appended AES key

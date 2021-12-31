# PEGUARD

PEGUARD is a file crypter and packing utility. 

This project was originally included as a script in the WARFOX-C2 project found [here](). However, it can work as a standalone packer.

## Description

![image](https://user-images.githubusercontent.com/54753063/147796026-e1e1679d-9042-4a27-876c-4654674074a5.png)

## Technical Details

PeGuard takes a file as input, compresses it via GZIP, encrypts it using AES-128 (CBC mode) and appends the AES key to the end of the file. This utility was designed to pack the WARFOX DLL implant to aid in its DLL sideloading execution process.

### PeGuard
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

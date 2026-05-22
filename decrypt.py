import sys
import os

def save_crypt(data: bytes) -> bytes:
    key = b"!8\x11`\x17G/S]7$\x0e\x0e\x0f`C/\x0e?\n'UK\x0bOY%8\x0b:D\x17"
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
        
    i = 0
    j = 0
    out = bytearray()
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        t = (S[i] + S[j]) % 256
        out.append(byte ^ S[t])
        
    return bytes(out)

if __name__ == '__main__':
    print("=============================================")
    print("   LEGO Save Encrypter & Decrypter    ")
    print("=============================================\n")

    # 1. Get the file path (Argument or manual input)
    if len(sys.argv) < 2:
        file_path = input("Drag and drop your save file here or past his filepath and press Enter:\n> ")
        # Clean up quotes automatically added by Windows during drag-and-drop
        file_path = file_path.strip('"').strip("'")
    else:
        file_path = sys.argv[1]

    if not file_path or not os.path.exists(file_path):
        print("\n[Error] File not found or path is invalid.")
        input("\nPress Enter to exit...")
        sys.exit(1)

    # 2. Read the source file
    try:
        input_data = open(file_path, "rb").read()
    except Exception as e:
        print(f"\n[Error] Failed to read file: {e}")
        input("\nPress Enter to exit...")
        sys.exit(1)
    isDecrypt = True
    if file_path.lower().endswith('.dec'):
        isDecrypt = False
    print(f"Processing {os.path.basename(file_path)}...")
    if isDecrypt:
        output_path = file_path + '.dec'
    else:
        output_path = file_path + '.enc'
    output_data = save_crypt(input_data)

    try:
        with open(output_path, "wb") as f:
            f.write(output_data)
        print(f"\n[Success] Operation completed successfully!")
        print(f"-> Created file: {os.path.basename(output_path)}")
    except Exception as e:
        print(f"\n[Error] Failed to write output file: {e}")

    input("\nPress Enter to exit...")

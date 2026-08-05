import struct

def parse_png_chunks(filename):
    with open(filename, 'rb') as f:
        magic = f.read(8)
        if magic != b'\x89PNG\r\n\x1a\n':
            print("Not a PNG file")
            return
            
        while True:
            length_bytes = f.read(4)
            if not length_bytes:
                break
            length = struct.unpack(">I", length_bytes)[0]
            chunk_type = f.read(4)
            data = f.read(length)
            crc = f.read(4)
            
            if chunk_type != b'IDAT':
                print(f"Chunk Type: {chunk_type.decode('ascii', errors='replace')} | Length: {length}")
                if length > 0 and length < 10000:
                    print(f"  Data: {data[:100]}")
            if chunk_type == b'IEND':
                break

if __name__ == "__main__":
    parse_png_chunks("junior_developer.png")

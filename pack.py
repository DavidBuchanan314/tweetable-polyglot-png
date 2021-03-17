import zlib
from struct import unpack_from
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"

if len(sys.argv) != 4:
	print(f"USAGE: {sys.argv[0]} cover.png content.bin output.png")

# this function is gross
def fixup_zip(data, start_offset):
	end_central_dir_offset = data.rindex(b"PK\x05\x06")
	cdent_count = unpack_from("<H", data, end_central_dir_offset+10)[0]
	cd_range = slice(end_central_dir_offset+16, end_central_dir_offset+16+4)
	central_dir_start_offset = int.from_bytes(data[cd_range], "little")
	data[cd_range] = (central_dir_start_offset + start_offset).to_bytes(4, "little")
	for _ in range(cdent_count):
		central_dir_start_offset = data.index(b"PK\x01\x02", central_dir_start_offset)
		off_range = slice(central_dir_start_offset+42, central_dir_start_offset+42+4)
		off = int.from_bytes(data[off_range], "little")
		data[off_range] = (off + start_offset).to_bytes(4, "little")
		central_dir_start_offset += 1

png_in = open(sys.argv[1], "rb")
content_in = open(sys.argv[2], "rb")
png_out = open(sys.argv[3], "wb")

png_header = png_in.read(len(PNG_MAGIC))
assert(png_header == PNG_MAGIC)
png_out.write(png_header)

idat_body = b""
while True:
	chunk_len = int.from_bytes(png_in.read(4), "big")
	chunk_type = png_in.read(4)
	chunk_body = png_in.read(chunk_len)
	chunk_csum = int.from_bytes(png_in.read(4), "big")
	
	if chunk_type not in [b"IHDR", b"PLTE", b"IDAT", b"IEND"]:
		exit("ERROR: non essential or unknown chunk: " + chunk_type.decode())
	
	if chunk_type == b"IDAT":
		idat_body += chunk_body
	
	if chunk_type == b"IEND":
		start_offset = png_out.tell()+8+len(idat_body)
		print("Embedded file starts at offset", hex(start_offset))
		
		idat_body += content_in.read()
		
		if sys.argv[2].endswith(".zip"):
			print("Fixing up zip offsets...")
			idat_body = bytearray(idat_body)
			fixup_zip(idat_body, start_offset)
		
		png_out.write(len(idat_body).to_bytes(4, "big"))
		png_out.write(b"IDAT")
		png_out.write(idat_body)
		png_out.write(zlib.crc32(b"IDAT" + idat_body).to_bytes(4, "big"))
	
	png_out.write(chunk_len.to_bytes(4, "big"))
	png_out.write(chunk_type)
	png_out.write(chunk_body)
	png_out.write(chunk_csum.to_bytes(4, "big"))
	
	if chunk_type == b"IEND":
		break

png_in.close()
content_in.close()
png_out.close()

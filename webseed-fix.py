import bencoder
import requests
import hashlib
import sys

if len(sys.argv) < 3:
	print("Usage: python3 webseed-fix.py [torrentfile] [filename] [httplink]")
	exit()

torrentfile = sys.argv[1]
localfile = sys.argv[2]
originalfilename = localfile
webseed = sys.argv[3]


with open(torrentfile, 'rb') as torrentf:
	torrent = bencoder.decode(torrentf.read())

chunksize = torrent[b'info'][b'piece length']

print("Chunk size: {} KB".format(int(chunksize / 1024)))

offset = 0

if b'files' in torrent[b'info']:
	for tfile in torrent[b'info'][b'files']:
		if '/'.join([fn.decode('utf-8') for fn in tfile[b'path']]) != originalfilename:
			offset += tfile[b'length']
		else:
			print("Filename found in torrent")
			break
	else:
		print("Couldn't find the filename in torrent")
		exit()
else:
	print("1 file torrent")

fails = []

startoffset = chunksize - (offset % chunksize)
pieceoffset = int(offset/chunksize)
if startoffset != 0:
	print("{} KB not possible to validate, must re-download".format(int(startoffset / 1024)))
	fails.append(startoffset - chunksize)

localf = open(localfile, "r+b")
localf.seek(startoffset)

pieces = torrent[b'info'][b'pieces']
hashes = list(pieces[i:i+20] for i in range(0, len(pieces), 20))
i = 0
total_download = 0
while True:
	chunk = localf.read(chunksize)
	if len(chunk) != chunksize:
		total_download += len(chunk)
		print("{} KB not possible to validate, must re-download".format(int(len(chunk)/1024)))
		fails.append(startoffset + i * chunksize)
		break

	filechunkhash = hashlib.sha1(chunk).digest().hex()
	torrentpiecehash = hashes[pieceoffset+i+1].hex()
	if filechunkhash != torrentpiecehash:
		total_download += chunksize
		print("{} KB hash mismatch".format(int(chunksize/1024)))
		fails.append(startoffset + i * chunksize)
	i += 1

print("Starting download of total {} KB".format(int(total_download/1024)))

for dlpos in fails:
	dlposfixed = 0 if dlpos < 0 else dlpos
	localf.seek(dlposfixed)
	data = requests.get(webseed, headers={"Range": "bytes={}-{}".format(dlposfixed, dlpos+chunksize-1)}).content
	localf.write(data)
	print("Downloaded {} KB".format(int(len(data)/1024)))



# Webseed fix
You have a partially downloaded torrent file and want to finish it from a HTTP source, aka webseed?
Webseed fix is the right tool!

I was watching a tv series and suddenly the torrent went very slow. Luckily I had it downloaded on my seedbox as well, but there was only a few hundred MBs missing. Still it was causing problems on playback. I said, instead of downloading the whole file again, let's make a script that will download the broken pieces!

Webseed fix will read the torrent file, get pieces' hash information, verify the file chunks (pieces) and download the failed chunks from HTTP source.

### Usage
Before, run
```
pip3 install bencoder
```
then,
```
python3 webseed-fix.py [torrentfile] [filename] [httplink]

example:
python3 webseed-fix.py something.torrent Something.S01E01.mp4 http://example.com/data/Something.S01E01.mp4
```

(http filename can be anything, but local filename must match the one in torrent)

Note that if torrent has multiple files, a small part of the file will _probably_ always be downloaded. Because, if filesize doesn't meet chunk size, let's say 1 MB chunk size and 10.5 MB files, first 10 pieces are for the first file, and 11th piece is for both 1st and 2nd file. In that case we (might) not verify it because we don't have the other file, so we make sure by downloading these impossible to verify parts.


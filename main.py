#!/usr/bin/env python3
"""news-23 b110 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only (no PIL). Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import hashlib
import os
import struct
import sys
import zlib

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
MIN_BYTES = 10000
MAX_BYTES = 1024 * 1024


def fail(msg):
    print("main.py: ERROR:", msg, file=sys.stderr)
    return 1


def validate_png(data):
    """Validate the PNG header and chunk structure (stdlib only)."""
    if len(data) < 8 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return "not a PNG file (bad signature)"
    if len(data) < 8 + 25:
        return "file too short for IHDR"
    ln, typ = struct.unpack(">I4s", data[8:16])
    if typ != b"IHDR" or ln != 13:
        return "first chunk must be a 13-byte IHDR"
    w, h, depth, ctype, comp, filt, inter = struct.unpack(">IIBBBBB", data[16:29])
    if (w, h) != (1024, 1024):
        return "expected 1024x1024, got %dx%d" % (w, h)
    if depth != 8 or ctype not in (2, 6):
        return "expected 8-bit RGB/RGBA, got depth %d type %d" % (depth, ctype)
    if comp != 0 or filt != 0 or inter != 0:
        return "unexpected compression/filter/interlace flags"
    if zlib.crc32(b"IHDR" + data[16:29]) & 0xFFFFFFFF != struct.unpack(">I", data[29:33])[0]:
        return "IHDR CRC mismatch"
    # Walk the chunk list. Each chunk is laid out as: 4-byte big-endian
    # length, 4-byte type, <length> bytes of data, 4-byte CRC — i.e. the
    # 8-byte header at `pos` holds length+type, data starts at pos+8 and
    # the CRC sits at pos+8+clen. Every chunk CRC must check out, IDAT
    # payloads must be non-empty, and IEND (0 bytes) must be the final chunk.
    pos, idat_total, seen_iend = 33, 0, False
    while pos + 8 <= len(data):
        clen, ctyp = struct.unpack(">I4s", data[pos:pos + 8])
        if pos + 12 + clen > len(data):
            return "truncated chunk %r" % ctyp
        crc_stored = struct.unpack(">I", data[pos + 8 + clen:pos + 12 + clen])[0]
        if zlib.crc32(ctyp + data[pos + 8:pos + 8 + clen]) & 0xFFFFFFFF != crc_stored:
            return "CRC mismatch in chunk %r" % ctyp
        if ctyp == b"IDAT":
            if clen == 0:
                return "empty IDAT chunk"
            idat_total += clen
        if ctyp == b"IEND":
            if clen != 0:
                return "IEND must be empty"
            seen_iend = True
            if pos + 12 + clen != len(data):
                return "trailing data after IEND"
            break
        pos += 12 + clen
    if not seen_iend:
        return "no IEND chunk found"
    if idat_total < 1000:
        return "IDAT payload suspiciously small (%d bytes)" % idat_total
    return None


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not outdir:
        return fail("MAKEFUN_OUTPUT_DIR is empty")
    repo = os.path.dirname(os.path.abspath(__file__))
    outdir_abs = os.path.abspath(outdir)
    if outdir_abs == repo or outdir_abs.startswith(repo + os.sep):
        return fail("MAKEFUN_OUTPUT_DIR must be outside the repo: %s" % outdir)
    if os.path.exists(outdir_abs) and not os.path.isdir(outdir_abs):
        return fail("MAKEFUN_OUTPUT_DIR is a file, not a directory: %s" % outdir)
    try:
        with open(SRC, "rb") as f:
            data = f.read()
    except OSError as e:
        return fail("cannot read entry.png: %s" % e)
    if len(data) < MIN_BYTES:
        return fail("entry.png too small: %d bytes" % len(data))
    if len(data) > MAX_BYTES:
        return fail("entry.png over 1 MiB: %d bytes" % len(data))
    err = validate_png(data)
    if err:
        return fail(err)
    os.makedirs(outdir_abs, exist_ok=True)
    out_path = os.path.join(outdir_abs, "entry.png")
    if os.path.abspath(out_path) == os.path.abspath(SRC):
        return fail("output path would overwrite the source entry.png")
    with open(out_path, "wb") as f:
        f.write(data)
    with open(out_path, "rb") as f:
        back = f.read()
    if back != data:
        return fail("re-read mismatch after writing output")
    print("wrote %s (%d bytes, sha256 %s)" % (out_path, len(data),
                                              hashlib.sha256(data).hexdigest()))
    return 0


if __name__ == "__main__":
    sys.exit(main())

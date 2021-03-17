# [tweetable-polyglot-png](https://github.com/DavidBuchanan314/tweetable-polyglot-png)
Pack up to 3MB of data into a tweetable PNG polyglot file.

## How?

Twitter strips unnecessary data from PNG uploads, however, they do not strip
trailing data from the DEFLATE stream inside the IDAT chunk, provided that the
overall image file meets the requirements to avoid being re-encoded.

## Why?

Dunno.

## Cover image requirements

The cover image must compress well, such that the compressed filesize is less than
`(width * height) - size_of_embedded_file`. If the cover image does not have a
palette, then it must have at least 257 unique colours (otherwise twitter will
optimise it to use a palette).

The resolution can be up to 4096x4096, however, be aware that twitter will serve
a downscaled version by default, for images greater than 680x680 (depending on your display DPI, etc.).

## Embedded file requirements

The total output file size must be less than 3MB (maybe 5MB?), otherwise
twitter will convert the PNG to a JPEG.

If the embedded file is a `.zip`, then the offsets are automatically adjusted
so that the overall file is still a valid zip. For any other file formats, you're
on your own (many will work without any special handling, notably `.pdf`, `.mp3`).

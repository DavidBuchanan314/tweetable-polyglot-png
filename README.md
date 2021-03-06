# [tweetable-polyglot-png](https://github.com/DavidBuchanan314/tweetable-polyglot-png)
Pack up to 3MB of data into a tweetable PNG polyglot file.

See it in action here: https://twitter.com/David3141593/status/1371974874856587268

![image](https://pbs.twimg.com/media/Ewo7CpJW8AMjVZt?format=png&name=small)

Other image hosts I've verified this technique to work on:

 - Imgur (https://i.imgur.com/kNhGrN3.png)

 - Github repo thumbnail/header image (https://repository-images.githubusercontent.com/348501512/06710f00-8886-11eb-95d1-3f416fa3853a)

 - Discord (Not a huge surprise, since they surport arbitrary files anyway) (https://cdn.discordapp.com/attachments/464905259261755392/823171702170845199/06710f00-8886-11eb-95d1-3f416fa3853a.png)

Image hosts I've confirmed it *doesn't* work on:

 - Reddit (Perhaps it could be made to work by embedding data *within* the DEFLATE stream, rather than appending?)

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

The image should not have any unecessary metadata chunks. I used these export settings in GIMP:

![image](https://user-images.githubusercontent.com/13520633/111412860-1990ad00-86d5-11eb-9c2f-3a88db84fdf4.png)


## Embedded file requirements

The total output file size must be less than 3MB (maybe 5MB?), otherwise
twitter will convert the PNG to a JPEG.

If the embedded file is a `.zip`, then the offsets are automatically adjusted
so that the overall file is still a valid zip. For any other file formats, you're
on your own (many will work without any special handling, notably `.pdf`, `.mp3`).

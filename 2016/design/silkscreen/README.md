# Adding Logo's to the Silkscreen

```bash
$ make
convert rombit.png -colors 2 -type bilevel +antialias rombit.bmp
convert fri3d.pdf fri3d.png
convert fri3d.png -colors 2 -type bilevel +antialias fri3d.bmp
rm fri3d.png
```

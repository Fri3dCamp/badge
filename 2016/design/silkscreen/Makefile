all: rombit.bmp fri3d.bmp

%.bmp: %.png
	convert $< -colors 2 -type bilevel +antialias $@

%.png: %.pdf
	convert $< $@

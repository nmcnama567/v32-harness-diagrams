all: svg png

svg:
	python3 generators/gen_diagrams.py

png: svg
	zsh generators/export.sh

.PHONY: all svg png

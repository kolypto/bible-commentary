all: newlines

.PHONY: newlines
newlines: *.md
	@python newlines.py

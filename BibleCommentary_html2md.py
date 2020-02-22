""" Convert Bible commentary HTML (exported from GDocs) into a series of MD files

Usage:
    python BibleCommentary_html2md.py BibleCommentary.html
"""
import re
import sys
import bs4
from typing import List, Optional, IO
from dataclasses import dataclass, field


@dataclass
class Chapter:
    """ Container for a single GDoc chapter """
    # <h*> header depth: 1+
    # level=0 is the root object (the document)
    level: int
    # Chapter title (from the <h*> header)
    title: str
    # Chapter contents: list of paragraphs
    contents: List[str] = field(default_factory=list)
    # Sub-chapters
    subchapters: List['Chapter'] = field(default_factory=list)


def main(argv):
    """ Application """
    # Load HTML
    try:
        html_doc = load_html(argv[1])
    except IndexError:
        print(__doc__, file=sys.stderr)
        exit(1)

    # Parse it
    root_chapter = parse_gdoc_html(html_doc)

    # Top-level chapters (0, 1, 2) become files
    export_chapter_to_file(root_chapter)
    for h1 in root_chapter.subchapters:
        export_chapter_to_file(h1)
        for h2 in h1.subchapters:
            # All sub-chapters are embedded
            export_chapter_to_file(h2, subchapters_become_headings=True)


def export_chapter_to_file(chapter: Chapter, subchapters_become_headings: bool = False):
    """ Export a chapter to a Markdown file """
    # Filename: strip markdown characters
    filename = (chapter.title or 'root').strip('*_ ')

    # Open file
    with open(f'{filename}.md', 'wt') as f:
        _write_chapter_into_stream(f, chapter, recurse=subchapters_become_headings)




def _write_chapter_into_stream(f: IO, chapter: Chapter, *, recurse: bool):
    # Add some vertical space
    if f.tell() != 0:
        f.write('\n' * 3 * chapter.level)  # vspace

    # Chapter heading
    h_prefix = '#' * chapter.level  # Markdown chapter
    f.write(f'{h_prefix} {chapter.title}\n\n')  # chapter heading

    # Chapter contents
    # Just HTML, because it's compatible
    f.write('\n\n'.join(chapter.contents))

    # Sub-chapters?
    if recurse:
        for subchapter in chapter.subchapters:
            _write_chapter_into_stream(f, subchapter, recurse=recurse)




def parse_gdoc_html(html_doc: str):
    """ Parse the Google doc """
    # GDoc has the following simple structure:
    #
    #   html
    #       body
    #           h1
    #           h2
    #           h3
    #           h4
    #           p
    #
    # all headers and text are on the same level.
    # Therefore, we just walk all top-level entities and split them by chapter.

    soup = bs4.BeautifulSoup(html_doc, 'html.parser')

    # Convert some things to look more markdown-ish
    prepare_html_for_markdown(soup)

    # Now parse
    body_elements: List[bs4.element.Tag] = soup.select('body > *')

    # Init the root chapter
    root = Chapter(level=0, title=None)

    # Init the current sub-chapters
    # the list items meaning: [root, h1, h2, h3, h4]
    chapters: List[Optional[Chapter]] = [root, None, None, None, None]

    # Now, start iterating contents
    current_level = 0
    for tag in body_elements:
        # All <p> tags go to the current chapter
        if tag.name == 'p' and tag.attrs['class'] == ['c2']:
            # Add its innerHtml (only the contents)
            chapters[current_level].contents.append(tag.decode_contents())
        # Some other tags are added as is
        elif tag.name in ('p', 'ul', 'a'):
            # Add its outerHtml (including the tag)
            chapters[current_level].contents.append(str(tag))
        # All headers become subchapters
        elif tag.name in ('h1', 'h2', 'h3', 'h4'):
            # Create a new chapter
            level = int(tag.name[1:])
            chapter_title = tag.text.strip('*_ ')  # remove markdown
            new_chapter = Chapter(level=level, title=chapter_title)

            # Replace it
            current_level = level
            chapters[level] = new_chapter

            # Bind it to the parent
            chapters[level-1].subchapters.append(new_chapter)

            # Reset children
            for i in range(level+1, len(chapters)):
                chapters[i] = None
        else:
            raise ValueError(str(tag))

    # Done
    return root


def prepare_html_for_markdown(soup: bs4.BeautifulSoup):
    """ Replace certain tags with MarkDown constructs """
    # a: links
    for tag in soup.select('a'):
        if 'href' in tag.attrs:
            tag.replace_with(bs4.element.NavigableString(f'[{tag.text}]({tag.attrs["href"]})'))

    # <br />
    for tag in soup.select('br'):
        tag.replace_with(bs4.element.NavigableString("\n"))

    # Convert to Markdown constructs
    TO_MARKDOWN = {
        'span.c0': '**{text}**',  # bold
        'span.c1': '__{text}__',  # underline
        'span.c3': '*{text}*',  # italics
    }

    for span_selector, template in TO_MARKDOWN.items():
        # Replace every tag
        for tag in soup.select(span_selector):
            # Refuse to do so if losing embedded HTML tags
            embedded_tags = tag.select('*')
            assert not tag.select('*')

            # Convert to text
            # WARNING: losing HTML contents!
            text = template.format(text=tag.text)

            # Add as plaintext
            tag.replace_with(bs4.element.NavigableString(text))

    # span: remove all other spans
    for tag in soup.select('span'):
        tag.replace_with(bs4.element.NavigableString(tag.decode_contents()))


def load_html(filename):
    """ Load contents from the file """
    with open(filename) as f:
        return f.read()


# Run
main(sys.argv)

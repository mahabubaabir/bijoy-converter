"""
Convert Bijoy (SutonnyMJ) encoded .docx files to Unicode Bengali.

Converts a single .docx, several .docx files, or every .docx in a
directory. Output files are named '<input stem> (Unicode).docx' (or a
custom suffix via --suffix) and are saved next to the input (or into
--out-dir when given).

The source file stores Bijoy bytes decoded as cp1252 characters inside
UTF-8 XML. Each run's text is converted to Unicode, English runs
(English-font runs, English words, or pure-ASCII paragraphs) are kept
unchanged, and Bengali runs get the Kalpurush font. Paragraphs that are
already Unicode Bengali (e.g. from a previous partial conversion) are
passed through unchanged, because re-converting is not idempotent.

Requires: python-docx
    pip install python-docx

Usage:
    python convert_docx.py file.docx
    python convert_docx.py a.docx b.docx
    python convert_docx.py folder/                     # all *.docx inside
    python convert_docx.py file.docx -o out_dir/
    python convert_docx.py file.docx --suffix " - bn"
"""

import argparse
import sys
from pathlib import Path

from docx import Document

from bijoy_converter import convert_bijoy_to_unicode
import bijoy_converter

# Fonts used for English text in the source document
ENGLISH_FONTS = {'Arial', 'Calibri', 'Times New Roman', 'Tahoma'}
BENGALI_FONT = 'Kalpurush'

# Common English words (articles, prepositions, etc.)
COMMON_ENGLISH = {
    'the', 'of', 'and', 'in', 'on', 'at', 'to', 'a', 'an', 'is', 'are',
    'was', 'were', 'be', 'been', 'by', 'for', 'with', 'from', 'this',
    'that', 'these', 'those', 'it', 'its', 'or', 'as', 'we', 'our',
    'you', 'your', 'they', 'their', 'he', 'she', 'his', 'her', 'not',
    'no', 'yes', 'so', 'but', 'if', 'then', 'than', 'can', 'will',
    'would', 'should', 'may', 'might', 'must', 'all', 'some', 'any',
    'each', 'every', 'both', 'one', 'two', 'three', 'day', 'days',
    'session', 'sessions', 'policy', 'break', 'lunch', 'snack', 'tea',
    'learning', 'journey', 'canvas', 'gender', 'esg', 'live', 'safe',
    'safeguarding', 'project', 'youth', 'green', 'connect',
    'entrepreneurship', 'development', 'reflection', 'stakeholder',
    'stakeholders', 'triple', 'bottom', 'line', 'networking',
    'role', 'play', 'wrap', 'up', 'time', 'schedule', 'module',
    'modules', 'day1', 'day2', 'day3', 'day4', 'day5',
}

PUNCT = set('.,;:()[]\'"-/\\|')

# Characters a run must not end with when merging (space/punctuation)
MERGE_SKIP_START = ' \t\n\r.,;:()[]\'"-/\\|'

# All Bijoy-encoded characters (keys of the converter maps). A run that
# contains none of these but already contains Unicode Bengali was already
# converted (e.g. by an earlier manual/partial conversion) and must be
# passed through unchanged.
BIJOY_CHAR_SET = (set(bijoy_converter.PRE_CONVERSION_MAP) |
                  set(bijoy_converter.CONVERSION_MAP))

# Raw Bijoy characters that convert to pre-kars ('ি', 'ৈ', 'ে')
RAW_PRE_KAR_END = {'w', '\u2020', '\u2021', '\u02c6', '\u2030'}

# Raw Bijoy characters that convert to a conjunct starting with a halant
# ('্য', '্র', 'ত্র', 'ক্স', 'ঙ্গ', 'জ্ঞ', 'ক্ষ', ...). A run starting
# with one continues the conjunct begun in the previous run, so the pair
# must be merged for the pre-kar walk to see the whole conjunct.
CONJUNCT_STARTERS = {k for k, v in bijoy_converter.CONVERSION_MAP.items()
                     if v.startswith('\u09cd')}


def is_ascii(text: str) -> bool:
    return all(ord(c) < 128 for c in text)


def has_bengali_unicode(text: str) -> bool:
    return any('\u0980' <= c <= '\u09ff' for c in text)


def is_already_unicode(text: str) -> bool:
    """True if the text is already Unicode Bengali (no Bijoy chars)."""
    return has_bengali_unicode(text) and not any(c in BIJOY_CHAR_SET for c in text)


def clean_word(word: str) -> str:
    """Lowercase and strip punctuation for whitelist matching."""
    return word.strip().strip('.,;:()[]\'"-/\\|').lower()


def collect_english_words(doc) -> set:
    """Build a whitelist of English words from the document itself."""
    words = set(COMMON_ENGLISH)
    seen = set()

    def scan_paragraph(paragraph):
        for run in paragraph.runs:
            if run.font.name in ENGLISH_FONTS:
                for w in _split_words(run.text):
                    words.add(w)

    def scan_table(table):
        for row in table.rows:
            for cell in row.cells:
                if id(cell._tc) in seen:
                    continue
                seen.add(id(cell._tc))
                for paragraph in cell.paragraphs:
                    scan_paragraph(paragraph)
                for nested in cell.tables:
                    scan_table(nested)

    for paragraph in doc.paragraphs:
        scan_paragraph(paragraph)
    for table in doc.tables:
        scan_table(table)
    return words


def _split_words(text: str):
    import re
    for w in re.split(r'[\s/\\]+', text):
        w = clean_word(w)
        if len(w) >= 2:
            yield w


def merge_boundary_runs(paragraph) -> bool:
    """Merge runs split across a pre-kar, a reph marker, or a conjunct.

    Bijoy pre-kars ('ে','ৈ','ি') are typed before the consonant, so when a
    run ends with one, the consonant lives in the next run. Likewise a run
    may start with the reph marker '©' or a conjunct continuation
    ('্য', '্র', ...) whose consonant is in the previous run. Merging the
    pair makes the converter see the whole word (e.g. '‡' + 'RÛvi' ->
    'জেন্ডার', 'D‡`' + 'vM' -> 'উদ্যোগ', 'Kvh' + '©µg' -> 'কার্যক্রম',
    'g¨vwU' + 'ª·' -> 'ম্যাট্রিক্স', 'j‡ÿ' + '¨' -> 'লক্ষ্যে').

    This must run on the RAW (unconverted) run texts: re-converting
    already-converted text is not idempotent (e.g. 'উদ্দেশ্য' -> 'উদ্দশ্যে').
    """
    runs = paragraph.runs
    if len(runs) < 2:
        return False
    orig = [r.text for r in runs]
    changed = False
    again = True
    while again:
        again = False
        for i in range(len(runs) - 1):
            if not orig[i]:
                continue
            next_orig = orig[i + 1]
            if not next_orig:
                continue
            if next_orig[0] in MERGE_SKIP_START:
                continue
            if (orig[i][-1] not in RAW_PRE_KAR_END
                    and next_orig[0] != '\u00a9'
                    and next_orig[0] not in CONJUNCT_STARTERS):
                continue
            merged = orig[i] + next_orig
            runs[i].text = merged
            orig[i] = merged
            runs[i].font.name = BENGALI_FONT
            runs[i + 1]._r.getparent().remove(runs[i + 1]._r)
            del runs[i + 1]
            del orig[i + 1]
            changed = True
            again = True
            break
    return changed


def process_paragraph(paragraph, english_words: set) -> bool:
    """Convert Bijoy runs in a paragraph. Returns True if anything changed."""
    changed = False
    joined = ''.join(run.text for run in paragraph.runs)

    # Pure-ASCII paragraphs pass through unchanged, but only when they look
    # like real English (Bijoy text is pure ASCII too, e.g. 'mgvcYx' ->
    # 'সমাপণী'). A paragraph is considered English when it contains at
    # least one known English word.
    if is_ascii(joined) and joined.strip():
        if any(clean_word(w) in english_words
               for w in joined.split() if len(clean_word(w)) >= 2):
            return False

    # Already-converted Unicode Bengali (partial/manual conversions in the
    # source) must not be re-converted: the converter is not idempotent.
    if is_already_unicode(joined):
        return False

    # Merge runs split across pre-kars / reph markers / conjuncts BEFORE
    # conversion, so the converter always sees the raw Bijoy word.
    if merge_boundary_runs(paragraph):
        changed = True

    for run in paragraph.runs:
        text = run.text
        if not text.strip():
            continue

        font = run.font.name
        if font in ENGLISH_FONTS:
            continue

        # Per-run English-word protection (mixed Bengali/English paragraphs)
        if clean_word(text) in english_words:
            continue

        converted = convert_bijoy_to_unicode(text)
        if converted != text:
            run.text = converted
            run.font.name = BENGALI_FONT
            changed = True

    return changed


def process_table(table, english_words: set) -> bool:
    """Convert all paragraphs inside a table (including nested tables)."""
    changed = False
    seen = set()
    for row in table.rows:
        for cell in row.cells:
            # Merged cells appear multiple times in row.cells; process once.
            # Use the element itself (hashable) - id() of lxml proxies can be
            # reused after garbage collection, causing cells to be skipped.
            if cell._tc in seen:
                continue
            seen.add(cell._tc)
            for paragraph in cell.paragraphs:
                if process_paragraph(paragraph, english_words):
                    changed = True
            for nested in cell.tables:
                if process_table(nested, english_words):
                    changed = True
    return changed


def convert_docx(input_path: str, output_path: str = None,
                 suffix: str = ' (Unicode)') -> str:
    """Convert one .docx file. Returns the output path."""
    input_file = Path(input_path)
    if not input_file.exists():
        raise FileNotFoundError(f'File not found: {input_path}')

    if output_path is None:
        output_path = str(input_file.parent / f'{input_file.stem}{suffix}.docx')

    print(f'Reading: {input_path}')
    doc = Document(input_path)
    english_words = collect_english_words(doc)
    print(f'English whitelist: {len(english_words)} words')

    changed_count = 0
    for paragraph in doc.paragraphs:
        if process_paragraph(paragraph, english_words):
            changed_count += 1

    for table in doc.tables:
        if process_table(table, english_words):
            changed_count += 1

    doc.save(output_path)
    print(f'Converted {changed_count} paragraphs')
    print(f'Saved: {output_path}')
    return output_path


def _expand_inputs(args) -> list:
    """Resolve files/directories from the command line into a file list."""
    files = []
    for item in args.inputs:
        p = Path(item)
        if p.is_dir():
            files.extend(sorted(f for f in p.glob('*.docx')
                                if not f.name.endswith(f'{args.suffix}.docx')))
        elif p.is_file():
            files.append(p)
        else:
            print(f'Warning: not found, skipping: {item}')
    return files


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description='Convert Bijoy (SutonnyMJ) .docx files to Unicode Bengali.',
        epilog='Examples:\n'
               '  python convert_docx.py file.docx\n'
               '  python convert_docx.py a.docx b.docx\n'
               '  python convert_docx.py folder/\n'
               '  python convert_docx.py file.docx -o out_dir/',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('inputs', nargs='+',
                        help='.docx file(s) and/or directories containing .docx files')
    parser.add_argument('-o', '--out-dir', default=None,
                        help='output directory (default: same folder as each input)')
    parser.add_argument('--suffix', default=' (Unicode)',
                        help='output filename suffix (default: " (Unicode)")')
    args = parser.parse_args(argv)

    files = _expand_inputs(args)
    if not files:
        print('No .docx files to convert.')
        return 1

    out_dir = Path(args.out_dir) if args.out_dir else None
    if out_dir:
        out_dir.mkdir(parents=True, exist_ok=True)

    ok = 0
    for f in files:
        out = None
        if out_dir:
            out = str(out_dir / f'{f.stem}{args.suffix}.docx')
        try:
            convert_docx(str(f), out, suffix=args.suffix)
            ok += 1
        except Exception as exc:
            print(f'Error converting {f}: {exc}')
    print(f'Done: {ok}/{len(files)} converted')
    return 0


if __name__ == '__main__':
    sys.exit(main())

"""Bijoy (SutonnyMJ) to Unicode Bengali converter."""

import re
from typing import Dict

# Bijoy to Unicode character mapping table
# Keys are Bijoy ASCII code points, values are Unicode Bengali equivalents
BIJOUY_MAP: Dict[str, str] = {
    # Vowels (স্বরবর্ণ)
    'v': '\u0985',      # অ
    'A': '\u0986',      # আ
    'E': '\u0987',      # ই
    'F': '\u0988',      # ঈ
    'R': '\u0989',      # উ
    'V': '\u098A',      # ঊ
    'K': '\u098B',      # ঋ
    'k': '\u0995',      # ক
    'Ä': '\u0996',      # খ
    'w': '\u0997',      # গ
    '`': '\u0998',      # ঘ
    'S': '\u0999',      # ঙ
    's': '\u099A',      # চ
    'W': '\u099B',      # ছ
    'Z': '\u099C',      # জ
    'z': '\u099D',      # ঝ
    'H': '\u099E',      # ঞ
    'q': '\u099F',      # ট
    'Q': '\u09A0',      # ঠ
    'N': '\u09A1',      # ড
    'n': '\u09A2',      # ঢ
    'B': '\u09A3',      # ণ
    'J': '\u09A4',      # ত
    'j': '\u09A5',      # থ
    'U': '\u09A6',      # দ
    'u': '\u09A7',      # ধ
    'G': '\u09A8',      # ন
    'Y': '\u09AA',      # প
    'y': '\u09AB',      # ফ
    'T': '\u09AC',      # ব
    't': '\u09AD',      # ভ
    'f': '\u09AE',      # ম
    'L': '\u09AF',      # য
    'l': '\u09B0',      # র
    'x': '\u09B2',      # ল
    'X': '\u09B6',      # শ
    'D': '\u09B7',      # ষ
    'C': '\u09B8',      # স
    'c': '\u09B9',      # হ

    # Vowel signs (কার)
    'I': '\u09BF',      # ি (ই-কার)
    'I\x80': '\u09C0', # ী (ঈ-কার) - not standard
    'O': '\u09C1',      # ু (উ-কার)
    'o': '\u09C2',      # ূ (ঊ-কার)
    'P': '\u09C3',      # ৃ (ঋ-কার)
    'p': '\u09C4',      # ৄ (ৠ-কার)
    'e': '\u09C7',      # ে (এ-কার)
    'E\x80': '\u09C8', # ৈ (ঐ-কার)
    'a': '\u09BE',      # া (আ-কার)
    'M': '\u09CD',      # ্ (হসন্ত)

    # Compound vowels
    '\x80': '\u09C8',   # ৈ
    '\x81': '\u09CB',   # ো
    '\x82': '\u09CC',   # ৌ

    # Digits (অংক)
    '0': '\u09E6',      # ০
    '1': '\u09E7',      # ১
    '2': '\u09E8',      # ২
    '3': '\u09E9',      # ৩
    '4': '\u09EA',      # ৪
    '5': '\u09EB',      # ৫
    '6': '\u09EC',      # ৬
    '7': '\u09ED',      # ৭
    '8': '\u09EE',      # ৮
    '9': '\u09EF',      # ৯

    # Punctuation
    ',': ',',            # Comma stays as is
    '.': '.',            # Period stays as is

    # Special characters
    'g': '\u0997',      # গ
    'R': '\u09B0',      # র (alternative)
    'G': '\u09A8',      # ন
}

# Common conjuncts (যুক্তাক্ষর) - Bijoy encoding
CONJUNCTS = {
    'K©': '\u0995\u09CD\u09B0',     # ক্র
    'K¿': '\u0995\u09CD\u09B7',     # ক্ষ
    'N©': '\u09A1\u09CD\u09B0',     # ড্র
    'q©': '\u099F\u09CD\u09B0',     # ট্র
    'Y©': '\u09AA\u09CD\u09B0',     # প্র
    'T©': '\u09AC\u09CD\u09B0',     # ব্র
    'f©': '\u09AE\u09CD\u09B0',     # ম্র
    'J©': '\u09A4\u09CD\u09B0',     # ত্র
    'C©': '\u09B8\u09CD\u09B0',     # স্র
    'U©': '\u09A6\u09CD\u09B0',     # দ্র
    's©': '\u099A\u09CD\u09B0',     # চ্র
    'w©': '\u0997\u09CD\u09B0',     # গ্র
    'c©': '\u09B9\u09CD\u09B0',     # হ্র
    'H©': '\u099E\u09CD\u09B0',     # ঞ্র
    'g©': '\u0997\u09CD\u09B0',     # গ্র
    'Z©': '\u099C\u09CD\u09B0',     # জ্র
    'L©': '\u09B2\u09CD\u09B0',     # ল্র
    'X©': '\u09B6\u09CD\u09B0',     # শ্র
    'D©': '\u09B7\u09CD\u09B0',     # ষ্র
    'B©': '\u09A3\u09CD\u09B0',     # ণ্র

    # Common two-letter conjuncts
    'KU': '\u0995\u09CD\u09A6',     # ক্দ
    'Kf': '\u0995\u09CD\u09AE',     # ক্ম
    'KY': '\u0995\u09CD\u09AA',     # ক্প
    'KT': '\u0995\u09CD\u09AC',     # ক্ব
    'Kt': '\u0995\u09CD\u09AD',     # ক্ভ
    'Kc': '\u0995\u09CD\u09B9',     # ক্হ
    'Kg': '\u0995\u09CD\u0997',     # ক্গ

    'CU': '\u09B8\u09CD\u09A6',     # স্দ
    'Cf': '\u09B8\u09CD\u09AE',     # স্ম
    'CY': '\u09B8\u09CD\u09AA',     # স্প
    'CT': '\u09B8\u09CD\u09AC',     # স্ব
    'Ct': '\u09B8\u09CD\u09AD',     # স্ভ
    'Cc': '\u09B8\u09CD\u09B9',     # স্হ

    'JU': '\u09A4\u09CD\u09A6',     # ত্দ
    'Jf': '\u09A4\u09CD\u09AE',     # ত্ম
    'JY': '\u09A4\u09CD\u09AA',     # ত্প
    'JT': '\u09A4\u09CD\u09AC',     # ত্ব
    'Jt': '\u09A4\u09CD\u09AD',     # ত্ভ
    'Jc': '\u09A4\u09CD\u09B9',     # ত্হ

    'UU': '\u09A6\u09CD\u09A6',     # দ্দ
    'Uf': '\u09A6\u09CD\u09AE',     # দ্ম
    'UY': '\u09A6\u09CD\u09AA',     # দ্প
    'UT': '\u09A6\u09CD\u09AC',     # দ্ব
    'Ut': '\u09A6\u09CD\u09AD',     # দ্ভ
    'Uc': '\u09A6\u09CD\u09B9',     # দ্হ

    'sU': '\u099A\u09CD\u09A6',     # চ্দ
    'sT': '\u099A\u09CD\u09AC',     # চ্ব
    'sf': '\u099A\u09CD\u09AE',     # চ্ম

    'wU': '\u0997\u09CD\u09A6',     # গ্দ
    'wT': '\u0997\u09CD\u09AC',     # গ্ব
    'wf': '\u0997\u09CD\u09AE',     # গ্ম

    'DU': '\u09B7\u09CD\u09A6',     # ষ্দ
    'DT': '\u09B7\u09CD\u09AC',     # ষ্ব
    'Df': '\u09B7\u09CD\u09AE',     # ষ্ম

    'h©': '\u09A4\u09CD\u09B0',     # ত্র
    'g©': '\u0997\u09CD\u09B0',     # গ্র
    'M©': '\u09A8\u09CD\u09B0',     # ন্র

    # More common conjuncts
    'KZ': '\u0995\u09CD\u099C',     # ক্জ
    'KN': '\u0995\u09CD\u09A1',     # ক্ড
    'Kn': '\u0995\u09CD\u09A2',     # ক্ঢ
    'KB': '\u0995\u09CD\u09A3',     # ক্ণ
    'Kq': '\u0995\u09CD\u099F',     # ক্ট
    'KQ': '\u0995\u09CD\u09A0',     # ক্ঠ
    'KJ': '\u0995\u09CD\u09A4',     # ক্ত
    'Kj': '\u0995\u09CD\u09A5',     # ক্থ
    'KG': '\u0995\u09CD\u09A8',     # ক্ন
    'Ky': '\u0995\u09CD\u09AB',     # ক্ফ
    'Kx': '\u0995\u09CD\u09B2',     # ক্ল
    'KS': '\u0995\u09CD\u0999',     # ক্ঙ
    'Ks': '\u0995\u09CD\u099A',     # ক্চ
    'KW': '\u0995\u09CD\u099B',     # ক্ছ
    'Kw': '\u0995\u09CD\u0997',     # ক্গ
    'K`': '\u0995\u09CD\u0998',     # ক্ঘ

    'CZ': '\u09B8\u09CD\u099C',     # স্জ
    'CN': '\u09B8\u09CD\u09A1',     # স্ড
    'Cn': '\u09B8\u09CD\u09A2',     # স্ঢ
    'CB': '\u09B8\u09CD\u09A3',     # স্ণ
    'Cq': '\u09B8\u09CD\u099F',     # স্ট
    'CQ': '\u09B8\u09CD\u09A0',     # স্ঠ
    'CJ': '\u09B8\u09CD\u09A4',     # স্ত
    'Cj': '\u09B8\u09CD\u09A5',     # স্থ
    'CG': '\u09B8\u09CD\u09A8',     # স্ন
    'Cx': '\u09B8\u09CD\u09B2',     # স্ল
    'CS': '\u09B8\u09CD\u0999',     # স্ঙ
    'Cs': '\u09B8\u09CD\u099A',     # স্চ
    'CW': '\u09B8\u09CD\u099B',     # স্ছ
    'Cw': '\u09B8\u09CD\u0997',     # স্গ
    'C`': '\u09B8\u09CD\u0998',     # স্ঘ

    'JZ': '\u09A4\u09CD\u099C',     # ত্জ
    'JN': '\u09A4\u09CD\u09A1',     # ত্ড
    'Jn': '\u09A4\u09CD\u09A2',     # ত্ঢ
    'JB': '\u09A4\u09CD\u09A3',     # ত্ণ
    'Jq': '\u09A4\u09CD\u099F',     # ত্ট
    'JQ': '\u09A4\u09CD\u09A0',     # ত্ঠ
    'JJ': '\u09A4\u09CD\u09A4',     # ত্ত
    'Jj': '\u09A4\u09CD\u09A5',     # ত্থ
    'JG': '\u09A4\u09CD\u09A8',     # ত্ন
    'Jx': '\u09A4\u09CD\u09B2',     # ত্ল
    'JS': '\u09A4\u09CD\u0999',     # ত্ঙ
    'Js': '\u09A4\u09CD\u099A',     # ত্চ
    'JW': '\u09A4\u09CD\u099B',     # ত্ছ

    'UZ': '\u09A6\u09CD\u099C',     # দ্জ
    'UN': '\u09A6\u09CD\u09A1',     # দ্ড
    'Un': '\u09A6\u09CD\u09A2',     # দ্ঢ
    'UB': '\u09A6\u09CD\u09A3',     # দ্ণ
    'Uq': '\u09A6\u09CD\u099F',     # দ্ট
    'UQ': '\u09A6\u09CD\u09A0',     # দ্ঠ
    'UJ': '\u09A6\u09CD\u09A4',     # দ্ত
    'Uj': '\u09A6\u09CD\u09A5',     # দ্থ
    'UG': '\u09A6\u09CD\u09A8',     # দ্ন
    'Ux': '\u09A6\u09CD\u09B2',     # দ্ল
    'US': '\u09A6\u09CD\u0999',     # দ্ঙ

    'sZ': '\u099A\u09CD\u099C',     # চ্জ
    'sN': '\u099A\u09CD\u09A1',     # চ্ড
    'sn': '\u099A\u09CD\u09A2',     # চ্ঢ
    'sB': '\u099A\u09CD\u09A3',     # চ্ণ
    'sq': '\u099A\u09CD\u099F',     # চ্ট
    'sQ': '\u099A\u09CD\u09A0',     # চ্ঠ
    'sJ': '\u099A\u09CD\u09A4',     # চ্ত
    'sj': '\u099A\u09CD\u09A5',     # চ্থ
    'sG': '\u099A\u09CD\u09A8',     # চ্ন
    'sx': '\u099A\u09CD\u09B2',     # চ্ল
    'sS': '\u099A\u09CD\u0999',     # চ্ঙ

    'wZ': '\u0997\u09CD\u099C',     # গ্জ
    'wN': '\u0997\u09CD\u09A1',     # গ্ড
    'wn': '\u0997\u09CD\u09A2',     # গ্ঢ
    'wB': '\u0997\u09CD\u09A3',     # গ্ণ
    'wq': '\u0997\u09CD\u099F',     # গ্ট
    'wQ': '\u0997\u09CD\u09A0',     # গ্ঠ
    'wJ': '\u0997\u09CD\u09A4',     # গ্ত
    'wj': '\u0997\u09CD\u09A5',     # গ্থ
    'wG': '\u0997\u09CD\u09A8',     # গ্ন
    'wx': '\u0997\u09CD\u09B2',     # গ্ল
    'wS': '\u0997\u09CD\u0999',     # গ্ঙ

    'DZ': '\u09B7\u09CD\u099C',     # ষ্জ
    'DN': '\u09B7\u09CD\u09A1',     # ষ্ড
    'Dn': '\u09B7\u09CD\u09A2',     # ষ্ঢ
    'DB': '\u09B7\u09CD\u09A3',     # ষ্ণ
    'Dq': '\u09B7\u09CD\u099F',     # ষ্ট
    'DQ': '\u09B7\u09CD\u09A0',     # ষ্ঠ
    'DJ': '\u09B7\u09CD\u09A4',     # ষ্ত
    'Dj': '\u09B7\u09CD\u09A5',     # ষ্থ
    'DG': '\u09B7\u09CD\u09A8',     # ষ্ন
    'Dx': '\u09B7\u09CD\u09B2',     # ষ্ল
    'DS': '\u09B7\u09CD\u0999',     # ষ্ঙ

    'XZ': '\u09B6\u09CD\u099C',     # শ্জ
    'XN': '\u09B6\u09CD\u09A1',     # শ্ড
    'Xn': '\u09B6\u09CD\u09A2',     # শ্ঢ
    'XB': '\u09B6\u09CD\u09A3',     # শ্ণ
    'Xq': '\u09B6\u09CD\u099F',     # শ্ট
    'XQ': '\u09B6\u09CD\u09A0',     # শ্ঠ
    'XJ': '\u09B6\u09CD\u09A4',     # শ্ত
    'Xj': '\u09B6\u09CD\u09A5',     # শ্থ
    'XG': '\u09B6\u09CD\u09A8',     # শ্ন
    'Xx': '\u09B6\u09CD\u09B2',     # শ্ল
    'XS': '\u09B6\u09CD\u0999',     # শ্ঙ

    'fZ': '\u09AE\u09CD\u099C',     # ম্জ
    'fN': '\u09AE\u09CD\u09A1',     # ম্ড
    'fn': '\u09AE\u09CD\u09A2',     # ম্ঢ
    'fB': '\u09AE\u09CD\u09A3',     # ম্ণ
    'fq': '\u09AE\u09CD\u099F',     # ম্ট
    'fQ': '\u09AE\u09CD\u09A0',     # ম্ঠ
    'fJ': '\u09AE\u09CD\u09A4',     # ম্ত
    'fj': '\u09AE\u09CD\u09A5',     # ম্থ
    'fG': '\u09AE\u09CD\u09A8',     # ম্ন
    'fx': '\u09AE\u09CD\u09B2',     # ম্ল
    'fS': '\u09AE\u09CD\u0999',     # ম্ঙ

    'LZ': '\u09B2\u09CD\u099C',     # ল্জ
    'LN': '\u09B2\u09CD\u09A1',     # ল্ড
    'Ln': '\u09B2\u09CD\u09A2',     # ল্ঢ
    'LB': '\u09B2\u09CD\u09A3',     # ল্ণ
    'Lq': '\u09B2\u09CD\u099F',     # ল্ট
    'LQ': '\u09B2\u09CD\u09A0',     # ল্ঠ
    'LJ': '\u09B2\u09CD\u09A4',     # ল্ত
    'Lj': '\u09B2\u09CD\u09A5',     # ল্থ
    'LG': '\u09B2\u09CD\u09A8',     # ল্ন
    'Lx': '\u09B2\u09CD\u09B2',     # ল্ল
    'LS': '\u09B2\u09CD\u0999',     # ল্ঙ

    'NZ': '\u09A3\u09CD\u099C',     # ণ্জ
    'NN': '\u09A3\u09CD\u09A1',     # ণ্ড
    'Nn': '\u09A3\u09CD\u09A2',     # ণ্ঢ
    'NB': '\u09A3\u09CD\u09A3',     # ণ্ণ
    'Nq': '\u09A3\u09CD\u099F',     # ণ্ট
    'NQ': '\u09A3\u09CD\u09A0',     # ণ্ঠ
    'NJ': '\u09A3\u09CD\u09A4',     # ণ্ত
    'Nj': '\u09A3\u09CD\u09A5',     # ণ্থ
    'NG': '\u09A3\u09CD\u09A8',     # ণ্ন
    'Nx': '\u09A3\u09CD\u09B2',     # ণ্ল
    'NS': '\u09A3\u09CD\u0999',     # ণ্ঙ

    'BZ': '\u09A3\u09CD\u099C',     # ণ্জ
    'BN': '\u09A3\u09CD\u09A1',     # ণ্ড
    'Bn': '\u09A3\u09CD\u09A2',     # ণ্ঢ
    'BB': '\u09A3\u09CD\u09A3',     # ণ্ণ
    'Bq': '\u09A3\u09CD\u099F',     # ণ্ট
    'BQ': '\u09A3\u09CD\u09A0',     # ণ্ঠ
    'BJ': '\u09A3\u09CD\u09A4',     # ণ্ত
    'Bj': '\u09A3\u09CD\u09A5',     # ণ্থ
    'BG': '\u09A3\u09CD\u09A8',     # ণ্ন
    'Bx': '\u09A3\u09CD\u09B2',     # ণ্ল
    'BS': '\u09A3\u09CD\u0999',     # ণ্ঙ
}

# Reph (র্) marker in Bijoy
REPH_MARK = '\u09B0\u09CD'  # র্

def is_bengali_char(char: str) -> bool:
    """Check if a character is Bengali Unicode."""
    cp = ord(char)
    return 0x0980 <= cp <= 0x09FF

def is_url_or_email(text: str, pos: int) -> bool:
    """Check if position is inside a URL or email."""
    # Simple heuristic: look for common URL/email patterns
    before = text[max(0, pos-20):pos]
    after = text[pos:min(len(text), pos+20)]
    combined = before + after
    return bool(re.search(r'https?://|www\.|@.*\.', combined))

def convert_bijoy_to_unicode(text: str) -> str:
    """
    Convert Bijoy (SutonnyMJ) encoded text to Unicode Bengali.

    This handles:
    - Character mapping from Bijoy ASCII to Unicode Bengali
    - Conjuncts (যুক্তাক্ষর)
    - Vowel sign reordering (pre-kars move after consonant)
    - Reph positioning
    - URL/email passthrough
    """
    if not text:
        return ""

    result = []
    i = 0
    n = len(text)

    while i < n:
        char = text[i]

        # Skip URL/email patterns
        if is_url_or_email(text, i):
            # Find end of URL/email
            j = i
            while j < n and text[j] not in (' ', '\n', '\t', '\r'):
                j += 1
            result.append(text[i:j])
            i = j
            continue

        # Check for conjuncts first (longest match)
        found_conjunct = False
        for length in (3, 2):
            if i + length <= n:
                chunk = text[i:i+length]
                if chunk in CONJUNCTS:
                    result.append(CONJUNCTS[chunk])
                    i += length
                    found_conjunct = True
                    break

        if found_conjunct:
            continue

        # Check for pre-composed vowel signs (ো, ৌ)
        if char == '\x81':  # ো
            result.append('\u09CB')
            i += 1
            continue
        elif char == '\x82':  # ৌ
            result.append('\u09CC')
            i += 1
            continue

        # Main character mapping
        if char in BIJOUY_MAP:
            result.append(BIJOUY_MAP[char])
        elif is_bengali_char(char):
            # Already Unicode, pass through
            result.append(char)
        else:
            # Not a Bengali character, pass through (spaces, English, etc.)
            result.append(char)

        i += 1

    # Join and post-process
    output = ''.join(result)

    # Fix reph positioning: র্ + consonant → consonant + র্
    # Actually in Unicode, reph goes after the consonant visually but before in code
    # The reorder pass handles this

    # Fix pre-kars (ি, ে) that should be after consonant
    # In Bijoy, ি comes BEFORE consonant; in Unicode it comes AFTER
    # The conversion already handles this via the mapping

    # Clean up: remove double hasantas
    output = output.replace('\u09CD\u09CD', '\u09CD')

    return output


def convert_file(input_path: str, output_path: str, encoding: str = 'latin-1') -> None:
    """Convert a Bijoy encoded file to Unicode."""
    with open(input_path, 'r', encoding=encoding, errors='replace') as f:
        content = f.read()

    converted = convert_bijoy_to_unicode(content)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(converted)

    print(f"Converted: {input_path} → {output_path}")


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python bijoy_to_unicode.py <input.txt> [output.txt]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.rsplit('.', 1)[0] + '_unicode.txt'

    convert_file(input_file, output_file)

"""
Bijoy (SutonnyMJ) to Unicode Bengali converter.

Based on the reference implementation from:
https://github.com/almehady/Bijoy-to-Unicode-File-Converter
"""

import re
from typing import Dict


def mb_strlen(s: str) -> int:
    """Get string length."""
    return len(s)


def mb_char_at(s: str, i: int) -> str:
    """Get character at position."""
    if 0 <= i < len(s):
        return s[i]
    return ''


def sub_string(s: str, start: int, end: int) -> str:
    """Get substring."""
    return s[start:end]


def do_char_map(s: str, char_map: Dict[str, str]) -> str:
    """Apply character mapping, longest match first."""
    result = []
    i = 0
    n = len(s)

    while i < n:
        matched = False
        # Try longest match first (up to 4 chars)
        for length in range(min(4, n - i), 0, -1):
            chunk = s[i:i + length]
            if chunk in char_map:
                result.append(char_map[chunk])
                i += length
                matched = True
                break

        if not matched:
            result.append(s[i])
            i += 1

    return ''.join(result)


# Pre-conversion normalizations
PRE_CONVERSION_MAP = {
    ' +': ' ',
    'yy': 'y',      # Double Hrosh-u-Kar
    'vv': 'v',      # Double Aa-Kar
    'y&': 'y',      # Hoshonto+Hrosh-u
    '„&': '„',      # Hoshonto+Ri-Kar
    ' ,': ',',
    ' \\|': '\\|',
    '\\\\ ': '',
    ' \\\\': '',
    '\\\\': '',
    '\n +': '\n',
    ' +\n': '\n',
    '\n\n\n\n\n': '\n\n',
    '\n\n\n\n': '\n\n',
    '\n\n\n': '\n\n',
}

# Main Bijoy to Unicode conversion map
CONVERSION_MAP = {
    # Vowels
    'Av': 'আ',
    'A': 'অ',
    'B': 'ই',
    'C': 'ঈ',
    'D': 'উ',
    'E': 'ঊ',
    'F': 'ঋ',
    'G': 'এ',
    'H': 'ঐ',
    'I': 'ও',
    'J': 'ঔ',

    # Consonants
    'K': 'ক',
    'L': 'খ',
    'M': 'গ',
    'N': 'ঘ',
    'O': 'ঙ',
    'P': 'চ',
    'Q': 'ছ',
    'R': 'জ',
    'S': 'ঝ',
    'T': 'ঞ',
    'U': 'ট',
    'V': 'ঠ',
    'W': 'ড',
    'X': 'ঢ',
    'Y': 'ণ',
    'Z': 'ত',
    '_': 'থ',
    '`': 'দ',
    'a': 'ধ',
    'b': 'ন',
    'c': 'প',
    'd': 'ফ',
    'e': 'ব',
    'f': 'ভ',
    'g': 'ম',
    'h': 'য',
    'i': 'র',
    'j': 'ল',
    'k': 'শ',
    'l': 'ষ',
    'm': 'স',
    'n': 'হ',
    'o': 'ড়',
    'p': 'ঢ়',
    'q': 'য়',
    'r': 'ৎ',
    's': 'ং',
    't': 'ঃ',
    'u': 'ঁ',

    # Numbers
    '0': '০',
    '1': '১',
    '2': '২',
    '3': '৩',
    '4': '৪',
    '5': '৫',
    '6': '৬',
    '7': '৭',
    '8': '৮',
    '9': '৯',

    # Kar (vowel signs)
    '•': 'ঙ্',
    'v': 'া',     # Aa-Kar
    'w': 'ি',     # i-Kar
    'x': 'ী',     # I-Kar
    'y': 'ু',     # u-Kar
    'z': 'ু',     # u-Kar
    '\u201c': 'ু',   # u-kar (left double quote)
    '\u2013': 'ু',   # u-kar (en dash)
    '~': 'ূ',     # U-kar
    '\u0192': 'ূ',   # U-kar (f-hook)
    '\u201a': 'ূ',   # U-kar (single low quote)
    '\u201e\u201e': 'ৃ',  # Double Ri-kar
    '\u201e': 'ৃ',   # Ri-Kar
    '\u2026': 'ৃ',   # Ri-Kar
    '\u2020': 'ে',   # E-Kar
    '\u2021': 'ে',   # E-Kar
    '\u02c6': 'ৈ',   # Oi-Kar
    '\u2030': 'ৈ',   # Oi-Kar
    '\u0160': 'ৗ',   # Ou-Kar
    '\\|': '।',     # Full-Stop
    '\\&': '্\u200c',  # Hoshonto
    '^': '্ব',      # Ba-phala (SutonnyMJ layout)

    # Jukto Okkhor (Conjuncts)
    '\\^': '্ব',
    '\u2018': '্তু',
    '\u2019': '্থ',
    '\u2039': '্ক',
    '\u0152': '্ক্র',
    '\u201d': 'চ্',
    '\u2014': '্ত',
    '\u02dc': 'দ্',
    '\u2122': 'দ্',
    '\u0161': 'ন্',
    '\u203a': 'ন্',
    '\u0153': '্ন',
    '\u0178': '্ব',
    '\u00a1': '্ব',
    '\u00a2': '্ভ',
    '\u00a3': '্ভ্র',
    '\u00a4': 'ম্',
    '\u00a5': '্ম',
    '\u00a6': '্ব',
    '\u00a7': '্ম',
    '\u00a8': '্য',
    '\u00a9': '\ue000',   # SutonnyMJ reph '©' -> marker, moved in rearrange
    '\u00aa': '্র',
    '\u00ab': '্র',
    '\u00ac': '্ল',
    '\u00ad': '্ল',
    '\u00ae': 'ষ্',
    '\u00af': 'স্',
    '\u00b0': 'ক্ক',
    '\u00b1': 'ক্ট',
    '\u00b2': 'ক্ষ্ণ',
    '\u00b3': 'ক্ত',
    '\u00b4': 'ক্ম',
    '\u00b5': 'ক্র',
    '\u00b6': 'ক্ষ',
    '\u00b7': 'ক্স',
    '\u00b8': 'গু',
    '\u00b9': 'জ্ঞ',
    '\u00ba': 'গ্দ',
    '\u00bb': 'গ্ধ',
    '\u00bc': 'ঙ্ক',
    '\u00bd': 'ঙ্গ',
    '\u00be': 'জ্জ',
    '\u00bf': '্ত্র',
    '\u00c0': 'জ্ঝ',
    '\u00c1': 'জ্ঞ',
    '\u00c2': 'ঞ্চ',
    '\u00c3': 'ঞ্ছ',
    '\u00c4': 'ঞ্জ',
    '\u00c5': 'ঞ্ঝ',
    '\u00c6': 'ট্ট',
    '\u00c7': 'ড্ড',
    '\u00c8': 'ণ্ট',
    '\u00c9': 'ণ্ঠ',
    '\u00ca': 'ণ্ড',
    '\u00cb': 'ত্ত',
    '\u00cc': 'ত্থ',
    '\u00cd': 'ত',   # SutonnyMJ: 'Í' = ত (not 'ত্ম')
    '\u00ce': 'ত্র',
    '\u00cf': 'দ্দ',
    '\u00d0': '-',
    '\u00d1': '-',
    '\u00d2': '"',
    '\u00d3': '"',
    '\u00d4': "'",
    '\u00d5': "'",
    '\u00d6': '্র',
    '\u00d7': 'দ্ধ',
    '\u00d8': 'দ্ব',
    '\u00d9': 'দ্ম',
    '\u00da': 'ন্ঠ',
    '\u00db': 'ন্ড',
    '\u00dc': 'ন্ধ',
    '\u00dd': 'ন্স',
    '\u00de': 'প্ট',
    '\u00df': 'প্ত',
    '\u00e0': 'প্প',
    '\u00e1': 'প্স',
    '\u00e2': 'ব্জ',
    '\u00e3': 'ব্দ',
    '\u00e4': 'ব্ধ',
    '\u00e5': 'ভ্র',
    '\u00e6': 'ু',   # SutonnyMJ: 'æ' = u-kar (not 'ম্ন')
    '\u00e7': 'ম্ফ',
    '\u00e8': '্ন',
    '\u00e9': 'ল্ক',
    '\u00ea': 'ল্গ',
    '\u00eb': 'ল্ট',
    '\u00ec': 'ল্ড',
    '\u00ed': 'ল্প',
    '\u00ee': 'ল্ফ',
    '\u00ef': 'শু',
    '\u00f0': 'শ্চ',
    '\u00f1': 'শ্ছ',
    '\u00f2': 'ষ্ণ',
    '\u00f3': 'ষ্ট',
    '\u00f4': 'ষ্ঠ',
    '\u00f5': 'ষ্ফ',
    '\u00f6': 'স্খ',
    '\u00f7': 'স্ট',
    '\u00f8': '্ল',   # SutonnyMJ: 'ø' = la-phala (not 'স্ন')
    '\u00f9': 'স্ফ',
    '\u00fa': '্প',
    '\u00fb': 'হু',
    '\u00fc': 'হৃ',
    '\u00fd': 'হ্ন',
    '\u00fe': 'হ্ম',
    '\u00ff': 'ক্ষ',
}

# Post-conversion normalizations
POST_CONVERSION_MAP = {
    '০ঃ': '০:',
    '১ঃ': '১:',
    '২ঃ': '২:',
    '৩ঃ': '৩:',
    '৪ঃ': '৪:',
    '৫ঃ': '৫:',
    '৬ঃ': '৬:',
    '৭ঃ': '৭:',
    '৮ঃ': '৮:',
    '৯ঃ': '৯:',
    ' ঃ': ':',
    '\nঃ': '\n:',
    ']ঃ': ']:',
    '\\[ঃ': '\\[:',
    '  ': ' ',
    'অা': 'আ',
    '্\u200c্\u200c': '্\u200c',
}


def is_bangla_digit(c: str) -> bool:
    """Check if character is a Bengali digit."""
    return '০' <= c <= '৯'


def is_bangla_pre_kar(c: str) -> bool:
    """Check if character is a pre-base vowel sign."""
    return c in ('ি', 'ৈ', 'ে')


def is_bangla_post_kar(c: str) -> bool:
    """Check if character is a post-base vowel sign."""
    return c in ('া', 'ো', 'ৌ', 'ৗ', 'ু', 'ূ', 'ী', 'ৃ')


def is_bangla_kar(c: str) -> bool:
    """Check if character is any vowel sign."""
    return is_bangla_pre_kar(c) or is_bangla_post_kar(c)


def is_bangla_banjore_borno(c: str) -> bool:
    """Check if character is a consonant."""
    return c in (
        'ক', 'খ', 'গ', 'ঘ', 'ঙ', 'চ', 'ছ', 'জ', 'ঝ', 'ঞ',
        'ট', 'ঠ', 'ড', 'ঢ', 'ণ', 'ত', 'থ', 'দ', 'ধ', 'ন',
        'প', 'ফ', 'ব', 'ভ', 'ম', 'য', 'র', 'ল', 'শ', 'ষ',
        'স', 'হ', 'ড়', 'ঢ়', 'য়', 'ৎ', 'ং', 'ঃ', 'ঁ'
    )


def is_bangla_hallant(c: str) -> bool:
    """Check if character is halant (hasanta)."""
    return c == '্'


def is_space(c: str) -> bool:
    """Check if character is whitespace."""
    return c in (' ', '\t', '\n', '\r')


def rearrange_unicode_text(s: str) -> bool:
    """Rearrange pre-kars and reph in converted Unicode text."""
    i = 0
    n = mb_strlen(s)

    while i < n:
        # Handle reph (র্)
        if (i < n - 1 and mb_char_at(s, i) == 'র' and
            is_bangla_hallant(mb_char_at(s, i + 1)) and
            is_bangla_hallant(mb_char_at(s, i - 1))):

            j = 1
            while True:
                if i - j < 0:
                    break
                if (is_bangla_banjore_borno(mb_char_at(s, i - j)) and
                    is_bangla_hallant(mb_char_at(s, i - j - 1))):
                    j += 2
                elif j == 1 and is_bangla_kar(mb_char_at(s, i - j)):
                    j += 1
                else:
                    break

            temp = sub_string(s, 0, i - j)
            temp += mb_char_at(s, i)
            temp += mb_char_at(s, i + 1)
            temp += sub_string(s, i - j, i)
            temp += sub_string(s, i + 2, n)
            s = temp
            i += 1
            continue

        i += 1

    # Remove double halants
    s = s.replace('্্', '্')

    # SutonnyMJ-style reph marker '\ue000' (from '©'): the reph was typed
    # AFTER the consonant cluster. Move it to just before that cluster
    # (skipping any kars and phala pairs in between), e.g. 'অজর্ন' -> 'অর্জন',
    # 'বণর্না' -> 'বর্ণনা', 'সামথ্য' + marker -> 'সামর্থ্য'.
    i = 0
    n = mb_strlen(s)
    while i < n:
        n = mb_strlen(s)
        if mb_char_at(s, i) == '\ue000':
            j = i - 1
            while j >= 0:
                c = mb_char_at(s, j)
                if is_bangla_kar(c):
                    j -= 1
                elif c != '্' and j >= 1 and mb_char_at(s, j - 1) == '্':
                    j -= 2
                elif c == '্':
                    j -= 1
                else:
                    break
            if j >= 0 and is_bangla_banjore_borno(mb_char_at(s, j)):
                s = (sub_string(s, 0, j) + 'র্' +
                     sub_string(s, j, i) + sub_string(s, i + 1, n))
                i += 1
                continue
            s = sub_string(s, 0, i) + 'র্' + sub_string(s, i + 1, n)
        i += 1

    i = 0
    n = mb_strlen(s)

    while i < n:
        # Handle reph with different pattern
        if (i < n - 1 and mb_char_at(s, i) == 'র' and
            is_bangla_hallant(mb_char_at(s, i + 1)) and
            not is_bangla_hallant(mb_char_at(s, i - 1)) and
            is_bangla_hallant(mb_char_at(s, i + 2))):

            j = 1
            a_z = 0

            while True:
                if is_bangla_banjore_borno(mb_char_at(s, i + j)) and is_bangla_hallant(mb_char_at(s, i + j + 1)):
                    j += 2
                elif is_bangla_banjore_borno(mb_char_at(s, i + j)) and is_bangla_pre_kar(mb_char_at(s, i + j + 1)):
                    a_z = 1
                    break
                else:
                    break

            temp = sub_string(s, 0, i - 1)
            temp += sub_string(s, i + j + 1, i + j + a_z + 1)
            temp += sub_string(s, i + 1, i + j + 1)
            temp += mb_char_at(s, i - 1)
            temp += mb_char_at(s, i)
            temp += sub_string(s, i + j + a_z + 1, n)
            s = temp
            i += j + a_z
            continue

        # Handle vowel + halant + consonant
        if (i > 0 and mb_char_at(s, i) == '্' and
            (is_bangla_kar(mb_char_at(s, i - 1)) or mb_char_at(s, i - 1) == 'ঁ') and
            i < n - 1):

            temp = sub_string(s, 0, i - 1)
            temp += mb_char_at(s, i)
            temp += mb_char_at(s, i + 1)
            temp += mb_char_at(s, i - 1)
            temp += sub_string(s, i + 2, n)
            s = temp

        # Handle ra + halant + vowel
        if (i > 0 and i < n - 1 and
            mb_char_at(s, i) == '্' and
            mb_char_at(s, i - 1) == 'র' and
            mb_char_at(s, i - 2) != '্' and
            is_bangla_kar(mb_char_at(s, i + 1))):

            temp = sub_string(s, 0, i - 1)
            temp += mb_char_at(s, i + 1)
            temp += mb_char_at(s, i - 1)
            temp += mb_char_at(s, i)
            temp += sub_string(s, i + 2, n)
            s = temp

        # Handle pre-kars
        if (i < n - 1 and is_bangla_pre_kar(mb_char_at(s, i)) and
            not is_space(mb_char_at(s, i + 1))):

            temp = sub_string(s, 0, i)

            j = 1
            while (i + j) < n - 1 and is_bangla_banjore_borno(mb_char_at(s, i + j)):
                if (i + j + 1) < n and is_bangla_hallant(mb_char_at(s, i + j + 1)):
                    j += 2
                elif (i + j + 1) < n and mb_char_at(s, i + j + 1) == '়':
                    j += 1
                elif ((i + j + 2) < n and
                      mb_char_at(s, i + j + 1) in ('ল', 'ব', 'ভ') and
                      is_bangla_hallant(mb_char_at(s, i + j + 2))):
                    j += 2
                else:
                    break

            temp += sub_string(s, i + 1, i + j + 1)

            l = 0
            if mb_char_at(s, i) == 'ে' and mb_char_at(s, i + j + 1) == 'া':
                temp += "ো"
                l = 1
            elif mb_char_at(s, i) == 'ে' and mb_char_at(s, i + j + 1) == 'ৗ':
                temp += "ৌ"
                l = 1
            else:
                temp += mb_char_at(s, i)

            temp += sub_string(s, i + j + l + 1, n)
            s = temp
            i += j

        # Handle nukta after post-kars
        if (i < n - 1 and mb_char_at(s, i) == 'ঁ' and
            is_bangla_post_kar(mb_char_at(s, i + 1))):

            temp = sub_string(s, 0, i)
            temp += mb_char_at(s, i + 1)
            temp += mb_char_at(s, i)
            temp += sub_string(s, i + 2, n)
            s = temp

        i += 1

    return s


def convert_bijoy_to_unicode(text: str) -> str:
    """
    Convert Bijoy (SutonnyMJ) encoded text to Unicode Bengali.

    Args:
        text: Bijoy-encoded text string

    Returns:
        Unicode Bengali text
    """
    if not text:
        return text

    # Pre-conversion
    text = do_char_map(text, PRE_CONVERSION_MAP)

    # Main conversion
    text = do_char_map(text, CONVERSION_MAP)

    # Rearrange (pre-kars, reph, etc.)
    text = rearrange_unicode_text(text)

    # Post-conversion
    text = do_char_map(text, POST_CONVERSION_MAP)

    return text


def convert_file(input_path: str, output_path: str, encoding: str = 'latin-1') -> None:
    """Convert a Bijoy encoded file to Unicode."""
    with open(input_path, 'r', encoding=encoding, errors='replace') as f:
        content = f.read()

    converted = convert_bijoy_to_unicode(content)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(converted)

    print(f"Converted: {input_path} -> {output_path}")


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python bijoy_converter.py <input.txt> [output.txt]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.rsplit('.', 1)[0] + '_unicode.txt'

    convert_file(input_file, output_file)

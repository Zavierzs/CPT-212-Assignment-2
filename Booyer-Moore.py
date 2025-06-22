NO_OF_CHARS = 256  # Number of possible characters (ASCII)

def bad_char_heuristic(pattern):
    """
    Creates the bad character heuristic table.
    For each character in the pattern, store its last occurrence index.
    If a character is not present in the pattern, its value remains -1.
    """
    badchar = [-1] * NO_OF_CHARS  # Initialize all occurrences as -1
    for i in range(len(pattern)):
        badchar[ord(pattern[i])] = i  # Update the index of the character in the pattern
    return badchar


def preprocess_strong_suffix(shift, bpos, pattern):
    """
    Preprocesses the pattern for the strong good suffix rule (case 1).
    Fills the shift and bpos arrays to determine how far to shift the pattern
    when a mismatch occurs after a partial match at the end of the pattern.
    """
    m = len(pattern)
    i, j = m, m + 1
    bpos[i] = j  # Set border position for the end of the pattern

    # Loop to fill shift[] and bpos[] for all borders of the pattern
    while i > 0:
        # Find the next border where the suffix matches a prefix
        while j <= m and pattern[i - 1] != pattern[j - 1 if j - 1 < m else m - 1]:
            if shift[j] == 0:
                shift[j] = j - i  # Set shift value for this border
            j = bpos[j]  # Jump to the next widest border
        i -= 1
        j -= 1
        bpos[i] = j  # Set border position for current i


def preprocess_case2(shift, bpos):
    """
    Preprocesses the pattern for the fallback good suffix rule (case 2).
    Ensures that every position in the shift array has a valid shift value,
    even if it was not set in the strong suffix preprocessing.
    """
    m = len(bpos) - 1  # Length of the pattern
    j = bpos[0]
    for i in range(m + 1):
        if shift[i] == 0:
            shift[i] = j  # Set shift to the next widest border
        if i == j:
            j = bpos[j]  # Move to the next border


def boyer_moore_search(text, pattern):
    """
    Searches for 'pattern' in 'text' using Boyer-Moore algorithm.
    Combines bad character and good suffix rules to skip unnecessary checks.
    """
    m = len(pattern)
    n = len(text)
    # If pattern or text is empty, or pattern is longer than text, return empty result
    if m == 0 or n == 0 or m > n:
        return []

    badchar = bad_char_heuristic(pattern)  # Preprocess bad character table
    bpos = [0] * (m + 1)                  # Border positions for good suffix rule
    shift = [0] * (m + 1)                 # Shift values for good suffix rule

    preprocess_strong_suffix(shift, bpos, pattern)  # Fill strong good suffix shifts
    preprocess_case2(shift, bpos)                  # Fill fallback good suffix shifts

    matches = []
    s = 0  # s is the shift of the pattern with respect to text

    while s <= n - m:
        j = m - 1  # Start comparing from the end of the pattern
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1  # Move left if characters match
        if j < 0:
            matches.append(s)  # Pattern found at position s
            s += shift[0]  # Shift pattern according to good suffix rule
        else:
            # Calculate shifts for bad character and good suffix rules
            bad_char_shift = j - badchar[ord(text[s + j])]
            # Calculate shift based on the good suffix rule
            good_suffix_shift = shift[j + 1]
            s += max(bad_char_shift, good_suffix_shift)  # Shift by the maximum

    return matches
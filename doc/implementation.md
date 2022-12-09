Python 3.8 is required for the walrus operator.

Line splitting
==============

Line separators:
  * We need to keep the separators so we can output the original separators
  * We still have to remove the line endings for layout calculation, or the
    line separator after a short line would make the column longer
  * We could only split on \n and keep the line endings. That way, we would
    automatically handle \r\n.
  * Or we could split on regex \r?\n, if this gives us the line ending
    directly.

Trailing empty lines: 
  * The output should match the input
  * Unterminated lines might not be complete, wait until flushed
  Splitting: we'll probably do it manually by appending to a buffer and
  finding line separators
  * string.splitlines recognizes too many line endings
  * Maybe we could use StringIO.readline 


Block splitting
===============

Questions:
  * Lines without a separator - treat as single cell or pass through?
    * Only relevant if there's trailing whitespace added, i. e. when we're
      padding the last cell or the row and when we're not trimming output lines
  * Consecutive non-table lines - collect or pass through individually?

We may want to split on:
  * Blank lines
  * Vertical tabs
    * First character in a line: split before that line
    * Last character in a line: split after that line
    * Single character in a line:
      * Split before/after the line?
      * Keep the empty line? Continuity!
    * Somewhere in a line: ???
  * Lines without a separator (including blank lines)


Space alignment
===============

Continuity:

    "ab " -> "ab", length 2 (left-aligned)
    "a "  -> "a", length 1
    " "   -> "", length 0

    " ab" -> "ab", length 2 (right-aligned)
    " a"  -> "a", length 1
    " "   -> "", length 0

    " ab " -> "ab", length 2 (centered)
    " a "  -> "a", length 1
    "  "   -> "", length 0


Trailing whitespace
===================

All cells except the last one in a row:
  * Must be fully padded to align the next one

Last cell in a row:
  * We must be able to stretch the column using whitespace, even we don't output
    it (at the end of a row)

End-of-line options:
  1. Remove all whitespace
  1. Keep original whitespace
  1. Pad to last cell width (noop for right-aligned cells)
  1. Pad to full table width (or: add empty cells and pad the last one)

Leading/trailing whitespace vs. cell width:
  * For now, just treat it like any other character so we can leave gaps in the
    table
  * If we ever remove whitespace before calculating cell width, we can't use the
    "keep original whitespace" option for the last cell in a row (other rows
    might have more cells)
  * This is also relevant for right-aligned cells

Conclusion - options:
  * --pad (none|cell|row)  - default is none
  * --trim
  * --trim overrides --pad cell and --pad row
  * For now, no option to ignore whitespace when calculating cell width

Conclusion - algorithm:
  * If pad==row, add empty cells to row
  * If pad==row or pad==cell, add whitespace to the last row
  * If trim, remove whitespace from the last row

To test:
  * All relevant whitespace options
  * With alignment left/right/center

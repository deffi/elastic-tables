Cell alignment:
  * Default alignment:
    * Text cells: left
    * Numeric columns: right with --align-numeric, else left
      Numeric columsn are columns that contain onyl numeric cells
      Numeric cells are cells with contains only digits and an optional sign:
      \s*[+-]?\d*\s*
  * Leading/trailing whitespace: --whitespace
    * keep: treated like other characters
    * remove: not included in cell contents
    * align:
      * Regular whitespace: not included in cell contents and used to determine
        alignment
      * NBSP (\xa0): used for alignment and removed; regular
        whitespace is kept
  * --quote: only whitespace outside the quotes is used for alignment
    and/or removed; one set of double-quotes are also removed (if present)
  * --keep-blank: completely blank cells are kept (only makes sense with
    --whitespace remove and --whitespace align)
  * Limitations:
    * With --whitespace align, we can't default-align a cell with
      leading/trailing whitespace, not even using nbsp. 
  * Defaults for CLI:
    * elastic-tables:  --whitespace align --align-numeric --keep-blank
    * elastic-tabstops: --whitespace keep

Specify encoding?
open without encoding uses locale.getpreferredencoding(False)
https://docs.python.org/3/library/functions.html#open

Support ANSI escape codes (currently, they probably mess up the formatting)

Allow coloring columns or cells

Advanced block splitting (configurable):
* Blank line (only whitespace)
* Empty line (contains nothing)
* Line without a column separator
  * More precisely, split before a line if its "has column separator" is
    different from the previous line

  * Advanced cell formatting:
* Explicitly specify formatter for column by index
* Auto-detect numeric colums (/-?\d+)
* Align on character (e. g. decimals)
* Keep leading/trailing whitespace in cell
* Treat whitespace like text for alignment

* Advanced table formatting:
* Column separator
* Preserve trailing whitespace
* Extend all rows to same number of cells

Global install:
  * Allow uninstall - if something replaced stdout in the meantime, we can't
    really do that, but we should be able to replace it with a passthrough. If
    it's re-installed later, we can re-replace it instead of adding another
    wrapper
  * Provide context manager

Escape sequences:
  * Which escape characters are easily accessible?
  * Which unicode escape characters exist?

I/O:
  * Open output file
  * Unconditionally provide elastic_tables.io.stdio/stderr
    But with what settings? Probably only makes sense with some kind of default
    configuration

Formatting by escape codes:
  * Probably best use backslash rather than ESC as escape character
  * Alignment: \< left, \> right, \| center?

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

Note that space alignment interfers with indentation. May need an extra tab
at the beginning or the line or after the indent.


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

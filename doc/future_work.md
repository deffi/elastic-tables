

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

Text
====

Encoding
--------

Right now, we don't explicitly specify the encoding, so it's probably locale
aware (locale.getpreferredencoding(False), see
https://docs.python.org/3/library/functions.html#open)

We may want to allow specifying the encoding explicitly. We might even want to
allow specifying an input encoding and an output encoding, though we're not in
the converting business.


Escape codes
------------

Right now, ANSI escape codes (color codes) will probably mess up the formatting
because the escape codes will contribute to the cell width. We should support
them by (optionally) filtering them out before calculating the cell width.

Open questions:
  * When the cell content is padded and an escape code specifies a background
    color, should that extend to the padding?
  * We may be able to specify this per cell by only considering the first/last
    color change in a cell: a switch to default followed by a switch to a
    background color will not affect the left padding.



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

Misc
----

Leading/trailing whitespace: --whitespace
* keep: treated like other characters
* remove: not included in cell contents
* align:
  * Regular whitespace: not included in cell contents and used to determine
    alignment
  * NBSP (\xa0): used for alignment and removed; regular
    whitespace is kept
--quote: only whitespace outside the quotes is used for alignment
and/or removed; one set of double-quotes are also removed (if present)
--keep-blank: completely blank cells are kept (only makes sense with
--whitespace remove and --whitespace align)
Limitations:
* With --whitespace align, we can't default-align a cell with
  leading/trailing whitespace, not even using nbsp. 
Defaults for CLI:
* elastic-tables:  --whitespace align --align-numeric --keep-blank
* elastic-tabstops: --whitespace keep


Cell alignment
==============

Cells alignment refers to how the text is placed in the cell if the cell is
wider than the text. The following alignment options are valid:
  * Left
  * Right
  * Centered-left (round to the left if the difference between cell width and
    text width is not an even number)
  * Centered-right (likewise, round to the right)

The following alignment settings are available from most to least specific:
  * For a cell
  * For a column
  * For a table
  * Default

When a cell is rendered, its content is padded on the left, on the right, or on
both sides, depending on the alignment and the difference between cell width and
content width (if the difference is 1, then even a centered cell will only be
padded on one side).

Open questions:
  * How to handle whitespace near the alignment edge?


Numeric alignment
-----------------

A numeric cell is a cell which contains only digits and an optional sign:
    \s*[+-]?\d*\s*

A numeric column is a column which contains only numeric cells.

Optionally, numeric columns are right-aligned by default. This might still be
overridden for the whole column or for individual cells.

We may also want to handle hexadecimal numbers, potentially only with a 0x
prefix. We may also want to handle 0o, 0b, and 0d.

We may also want to handle fractional numbers, but then we'll have to align them
on the decimal point. This goes beyond alignment because it affects the cell
width.
  * For now, the user must provide a column break before the decimal point, or
    after the last digit if there is no decimal point
  * The easiest way would probably be to determine which columns qualify and
    then to split these columns before or after the decimal point

Open questions:
  * Does it matter whether we split before or after the decimal point?
  * How do we handle leading whitespace?
  * How do we handle trailing whitespace?


Space alignment
---------------

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

Special whitespace?
  * NBSP
  * C1 padding character

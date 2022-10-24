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
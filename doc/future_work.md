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
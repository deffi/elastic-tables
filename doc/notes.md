Next:
  * Stdin: without universal newlines
    https://stackoverflow.com/questions/50476200/changing-the-way-stdin-stdout-is-opened-in-python-3
    https://discuss.python.org/t/forcing-sys-stdin-stdout-stderr-encoding-newline-behavior-programmatically/15437
  * TODOs in tests
  * Different line separators (\n, \r\n)
  * Align cells (based on leading/trailing whitespace)?
    * We my want to allow cells to start/end with whitespace

Project:
  * Move script to scripts/, it name-collides with the package
  * Rename? With cell alignment, it goes beyond elastic tabs
    * tab-les / tab_les
    * elastic-tables
  * Create package
  * Publish package
  * Auto-publish via GitHub actions

Alignment:
  * Control:
    * Keep trailing spaces from original?
    * Consider spaces when doing alignment?

Escape sequences:
  * Which escape characters are easily accessible?
  * Which unicode escape characters exist?

Future work:
  * Specify encoding?
    open ohne encoding benutzt locale.getpreferredencoding(False)
    https://docs.python.org/3/library/functions.html#open
  * Support ANSI escape codes (currently, they probably mess up the formatting)
  * Allow coloring columns or cells
  * Advanced block splitting (configurable):
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

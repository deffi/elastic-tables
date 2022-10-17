Next:
  * Block splitter, line splitter, filter: consistent interface
  * Create package
  * Publish package
  * Auto-publish via GitHub actions?

Tests:
  * Different line separators (\n, \r\n)

Render options:
  * Keep trailing whitespace (always pad last column, might be right-padded)
  * Extend rows (same number of cells in each row)
  * Recognize numeric cells?
    * Don't want this for decimals? But leading period -> non-numeric

Block separators (options):
  * Blank line
    * Line with only whitespace counts as blank?
    * Can we have a blank line without causing a block break?
  * Vertical tab or form feed at the end of / somewhere in a line
  * Line without a column separator
    * More precisely, split before a line if its "has column separator" is
      different from the previous line

Alignment:
  * Types:
    * Left
    * Right
    * Center
    * On character
  * Control:
    * Setup functions
    * Escape sequences? At least for left-align?
    * Keep trailing spaces from original?
    * Consider spaces when doing alignment?

Escape sequences:
  * Which escape characters are easily accessible?
  * Which unicode escape characters exist?

Future work:
  * Specify encoding?
    open ohne encoding benutzt locale.getpreferredencoding(False)
    https://docs.python.org/3/library/functions.html#open

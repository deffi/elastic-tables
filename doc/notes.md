Next:
  * Add new Filter
  * Block splitter, line splitter: consistent interface
  * Text sources:
    * Internal (\n)
    * Stdin
    * File
    * Stdin and file must use str (and text file) rather than bytes: a UTF-8
      stream might contain the byte value of the line terminator
  * Line separators:
    * We need to keep the separators so we can output the original separators
    * We still have to remove the line endings for layout calculation, or the
      line separator after a short line would make the column longer
    * We could only split on \n and keep the line endings. That way, we would
      automatically handle \r\n.
    * Or we could split on regex \r?\n, if this gives us the line ending
      directly.
  * Trailing empty lines: 
    * The output should match the input
    * Unterminated lines might not be complete, wait until flushed
  * Splitting: we'll probably do it manually by appending to a buffer and
    finding line separators
    * string.splitlines recognizes too many line endings
    * Maybe we could use StringIO.readline 
  * Global install stdout
  * Create package
  * Publish package
  * Auto-publish via Github actions

Tests:
  * Different line separators (\n, \r\n)

Render options:
  * Keep trailing whitespace (always pad last column, might be right-padded)
  * Extend rows (same number of cells in each row)
  * Recognize numeric cells?
    * Don't want this for decimals? But leading period -> non-numeric

Chunk separators (options):
  * Blank line
    * Line with only whitespace counts as blank?
    * Can we have a blank line without causing a chunk break?
  * Vertical tab or form feed at the end of / somewhere in a line
  * Line without a column separator
    * More precisely, split before a line if its "has column separator" is
      different from the previous line

Parsing:
  * Reproduce original line breaks?
  * Pass through lines without tabs?

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

Interface:
  * Parse/render functions
  * Line filter
  * Context manager that line-filters stdout/other streams
  * Global stdout line-filter
  
Escape sequences:
  * Which escape characters are easily accessible?
  * Which unicode escape characters exist?

Future work:
  * Specify encoding?
    open ohne encoding benutzt locale.getpreferredencoding(False)
    https://docs.python.org/3/library/functions.html#open
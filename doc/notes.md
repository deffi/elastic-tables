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

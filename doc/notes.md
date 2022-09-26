Render options:
  * Keep trailing whitespace (always pad last column, might be right-padded)
  * Extend rows (same number of cells in each row)

Chunk separators (options):
  * Blank line
    * Line with only whitespace counts as blank?
    * Can we have a blank line without causing a chunk break?
  * Vertical tab or form feed at the end of / somewhere in a line

Parsing:
  * Recognize numeric cells?
    * Don't want this for decimals? But leading period -> non-numeric
  * Reproduce original line breaks?

Alignment:
  * Types:
    * Left
    * Right
    * Center
    * On character
  * Control:
    * Setup functions
    * Escape sequences? At least for left-align?

Interface:
  * Parse/render functions
  * Line filter
  * Context manager that line-filters stdout/other streams
  * Global stdout line-filter
  
Escape sequences:
  * Which escape characters are easily accessible?
  * Which unicode escape characters exist?

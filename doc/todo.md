Next:
  * Align cells (based on leading/trailing whitespace)?
    * We my want to allow cells to start/end with whitespace
  * Unconditionally provide tab_les.io.stdio/stderr
  * TODOs in tests

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

Limitations:
  * With --whitespace align, we can't default-align a cell with
    leading/trailing whitespace, not even using nbsp. 

Defaults for CLI:
  * tab-les:  --whitespace align --align-numeric --keep-blank
  * elastic-tabs: --whitespace keep

I/O:
  * Open output file

Project:
  * Publish package
  * Auto-publish via GitHub actions

Alignment:
  * Control:
    * Keep trailing spaces from original?
    * Consider spaces when doing alignment?
Interface:
  * Parse/render functions
  * Line filter
  * Context manager that line-filters stdout/other streams
  * Global stdout line-filter

Text sources:
  * Internal (\n)
  * Stdin
  * File
  * Stdin and file must use str (and text file) rather than bytes: a UTF-8
  stream might contain the byte value of the line terminator


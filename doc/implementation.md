Line separators:
  * We need to keep the separators so we can output the original separators
  * We still have to remove the line endings for layout calculation, or the
    line separator after a short line would make the column longer
  * We could only split on \n and keep the line endings. That way, we would
    automatically handle \r\n.
  * Or we could split on regex \r?\n, if this gives us the line ending
    directly.

Trailing empty lines: 
  * The output should match the input
  * Unterminated lines might not be complete, wait until flushed
  Splitting: we'll probably do it manually by appending to a buffer and
  finding line separators
  * string.splitlines recognizes too many line endings
  * Maybe we could use StringIO.readline 

Python 3.8 is required for the walrus operator.

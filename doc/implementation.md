Python 3.8 is required for the walrus operator.


I/O
===

We calculate the text width, so we need to open the file as text so we get
strings (not bytes) and can be locale aware.


Line splitting
==============

Goals:
  * CR and CRLF are recognized as line terminators
  * Lines are processed as soon as they are complete, even if there is input
    data left (desirable for shell filter operation)
  * The original line terminators are output (even for mixed files)
  * A trailing unterminated line is reproduced (i. e., treated as a line,
    formatted like all other lines, and output without a terminators)
  * Line terminators are not considered for cell width calculation

Line splitting:
  * We need to separate the line terminator ("\r", "\r\n", or "") from the line
    content so we don't consider it when calculating the cell width
  * We need to keep the original line terminators, so we can't use universal
    newlines mode
  * string.splitlines recognizes many fancy line terminators that we're not
    interested in, so we can't use that
  * We could use StringIO (using the readline method or iteration), but we'd
    still have to separate the line terminator for the line content, and that
    would be a risk of inconsistency
  * Therefore, we append incoming data to a buffer and split on regex \r?\n
  * A line is complete (a) whne it is terminated, (b) when the input ends, or
    (c) when the line splitter is flushed manually

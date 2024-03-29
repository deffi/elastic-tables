TODOs in src
TODOs in tests

Issues
======

If we do
    elastic_tables.io.install()
Rich won't output colors by default (Workaround: FORCE_COLOR=1) because
rich.console.Console().is_terminal is False

Tests
=====

Can we get the coverage from the subproces runs?

File tests:
  * Empty line (1 or more) in input
  * Trailing unterminated line
 
Test whether it is locale (encoding) aware


Implementation
==============

use fileinput
Implement StreamFilter as Filter subclass?

Rename cell text to cell content

Split lines into rows before splitting groups of lines into blocks?
  * Pro: configurable column separator doesn't have to be duplicated; also, we
    may want to escape the column separator 
  * We may want to provide an interface where the user provides pre-split rows
  * Con: handling of vertical tab must modify rows 

We have two places where the default options are defined for filter options:
  * Filter class and cli functions
  * Require specifying filter options? But bad for programmatic use
  * FilterOptions class?
  * We also want to be able to change existing filter options, or forward
    StreamFilter options to the underlying Filter



Features
========

Alignment:
  * Remove align-whitespace? It's probably poorly defined in case of space-only
    cells

CLI:
  * multiple files: flush between?

Block splitting:
  * Treat lines without tabs as text lines -> no table formatting
  * Can't treat runs of lines without tabs as a single-column table because
    we would get padding
  * Can probably treat them as individual single-row single-column tables

Column separator:
  * Add output column separator
  * Allow multiple separators
  * Add (optional) escaping for literal separator?
    * Cant just use "\"+separator because that might conflict with other
      escape codes
  * Allow preserving cell separator (potentially by re-adding it)

Make whitespace character configurable? (useful for unit tests)

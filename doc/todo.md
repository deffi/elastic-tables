Allow other separators for easier testing

Default trim=true for CLI and Filter (update unit tests)
Default align-numeric=false

Remove align-whitespace? It's probably poorly defined in case of space-only
cells

We have two places where the default options are defined for filter options:
  * Filter class and cli functions
  * Require specifying filter options? But bad for programmatic use
  * FilterOptions class?
  * We also want to be able to change existing filter options, or forward
    StreamFilter options to the underlying Filter

Block splitting:
  * Treat lines without tabs as text lines -> no table formatting
  * Can't treat runs of lines without tabs as a single-column table because
    we would get padding
  * Can probably treat them as individual single-row single-column tables

Make cell separator configurable (e. g. for unit tests)
  * Add (optional) escaping for literal separator?
    * Cant just use "\"+separator because that might conflict with other
      escape codes

Make whitespace character configurable? (for unit tests)

Allow preserving cell separator (potentially by re-adding it)

TODOs in src
TODOs in tests

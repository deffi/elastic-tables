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

TODOs in src
TODOs in tests

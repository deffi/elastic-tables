How to handle output options?
  * Individual properties in renderer(/others?)
  * OutputOptions class that is passed into renderer -> stateless renderer!
  * Perform whitespace interpretation (for alignment)
    * In parser (when the cell is created) -> cell stores trimmed contents
    * In renderer (when rendering) -> cell stores original contents
    * Inbetween (transform models)

TODOs in tests

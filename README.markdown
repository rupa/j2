A complete rethink of [j](http://github.com/rupa/j/) using python to do the
heavy lifting.

Changes from original j:

    * Uses 2 separate files, so install is a bit more complicated.

    * Default ordering is 'frecent': rank weighted by time since last access.
      Match by 'rank' and 'recent' still available.

    * If all matches have a common prefix, and the prefix is one of the matches,
      and all args are matched in the prefix, go there unconditionally. This
      attempts to follow the principle of least surprise and replaces the
      'short' ordering.

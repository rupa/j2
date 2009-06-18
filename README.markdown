# OVERVIEW

Spend a lot of time cd-ing around a complex directory tree?

`j` keeps track of where you’ve been and how much time you spend there, and provides a convenient way to jump to the directories you actually use.

This is a complete rethink of [j](http://github.com/rupa/j/). See CHANGES for differences.

# INSTALLATION

* put something like this in your .bashrc:

    export JPY=/path/to/j.py # tells j.sh where the python script is
    . /path/to/j.sh          # provides the j() function

* make sure `j.py` is executable
* `cd` around for a while to build up the db
* PROFIT!!

# USE

* `j` by itself (or `j -l`) displays the current list of directories being remembered.

* `j foo` jumps to the highest weighted directory that has the substring `foo` in it, `j foo bar` for the weighted directory that has both `foo` and `bar`, etc...

* `j` supports tab completion.

* if you opten prefer one of the non-default match type, use aliases:
    * `alias jl='j -l'`
    * `alias jt='j -t recent'`
    * `alias jr='j -t rank'`

# MATCHING ALGORITHM

Look for case sensitive match first, then fall back to case insensitive.

If all matches have a common prefix, and the prefix is one of the matches, and all args are matched in the prefix, go there unconditionally. This attempts to follow the principle of least surprise.

Frecency: alter rank by time of last access.
* If access within last hour, multiply rank by 10.
* If access within last day, multiply rank by 2.
* If access within last week, divide rank by 2.
* If access is more than a week, divide rank by 10.

# AGING

Rank is recalculated as .9*rank when sum of ranks > MAX_NUM.
When the rank of a directory falls below 1, it will fall off the list.

# FAQ

Q) How come `j` doesn’t work like`cd`?

A) `j` is not intended as a substitute for the cd command. You should still `cd` everywhere as you normally would. When you want to jump somewhere you have been, then type `j <args>` to jump to a directory in your often used list.

Q) How do i 'source' something? Why?

A) Short answer: instead of running the script as `j.sh` you type `source j.sh or `. j.sh` in a shell, or to make it available all the time, put a command in your `.bashrc` that sources it, or just paste the contents of `j.sh` directly into your `.bashrc`.

Long answer: sourcing is like importing. When you run a script in a shell, it creates a subshell, runs your script, and returns to your current shell. If you cd in that subshell, it won’t matter to your current shell, because when your script is done running, it exits, and comes back to where you (still) are in your current shell. What we want in this case is to have the function and commands in our script defined in our current shell. Sourcing – rather than executing – the file does exactly that.

# CHANGES FROM [ORIGINAL j](http://github.com/rupa/j/)

* Uses python to do the heavy lifting.

* Uses 2 separate files, so install is a bit more complicated.

* Default ordering is 'frecent': rank weighted by time since last access. Match by 'rank' and 'recent' still available.

* If all matches have a common prefix, and the prefix is one of the matches, and all args are matched in the prefix, go there unconditionally. This attempts to follow the principle of least surprise and replaces the 'short' ordering.

# CREDITS

Joel Schaerer aka joelthelion for autojump
Daniel Drucker aka dmd for finding bugs and making me late for lunch

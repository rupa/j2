#!/bin/bash

j() {
    local datafile=$HOME/.j
    if [ "$1" = "--add" ]; then
        shift
        # $HOME isn't worth matching
        [ "$*" = "$HOME" ] && return
        awk -v q="$*" -v t="$(date +%s)" -F"|" '
            BEGIN { l[q] = 1; d[q] = t }
            $2 >= 1 {
                if( $1 == q ) {
                    l[$1] = $2 + 1
                    d[$1] = t
                } else {
                    l[$1] = $2
                    d[$1] = $3
                }
                count += $2
            }
            END {
                if( count > 1000 ) {
                 for( i in l ) print i "|" 0.9*l[i] "|" d[i] # aging
                } else for( i in l ) print i "|" l[i] "|" d[i]
            }
        ' $datafile 2>/dev/null > $datafile.tmp
        mv -f $datafile.tmp $datafile
    elif [ "$1" = "--complete" ]; then
        # tab completion
        awk -v q="$2" -F"|" '
            BEGIN { split(substr(q,3),a," ") }
            {
                if( system("test -d \"" $1 "\"") ) next
                for( i in a ) $1 !~ a[i] && $1 = ""; if( $1 ) print $1
            }
        ' $datafile 2>/dev/null
    else
        # list/go (must set $JPY)
        [ -f "$JPY" ] || return
        cd="$($JPY -f $datafile $*)"
        [ -z "$cd" -o "$cd" = "$PWD" ] && return
        cd "$cd"
    fi
}
# tab completion
complete -C 'j --complete "$COMP_LINE"' j
# populate directory list. avoid clobbering other PROMPT_COMMANDs.
PROMPT_COMMAND='j --add "$(pwd -P)";'"$PROMPT_COMMAND"

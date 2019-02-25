#!/bin/bash

## run_script.sh
## written by ChaoticWeg (Shawn Lutch)
##
## provides an easy way to treat an entire python script as a critical section
## because python blows at concurrency
##
## usage: ./run_script.sh --script=<script> [--lockfile=<lockfile>] [args...]
##      script:   name of python script to run. required.
##      lockfile: name of lockfile to use. optional. default = lockfile
##      args...:  args to pass along to the python script. optional.

# globals

DEFAULT_LOCKNAME=lockfile

# handle command-line arguments

EXTRA_ARGS=()
SCRIPTNAME=
LOCKNAME=

while (( "$#" )); do
    case "${1}" in

        # --script=<script>
        --script=*) SCRIPTNAME=${1/--script=/''}; shift;;
        --script) SCRIPTNAME=${2}; shift; shift;;

        # --lockfile=<lockfile> (default: lockfile)
        --lockfile=*) LOCKNAME=${1/--lockfile=/''}; shift;;
        --lockfile) LOCKNAME=${2}; shift; shift;;

        # not handled? toss it on the pile to pass to python later
        *) EXTRA_ARGS+=("${1}"); shift;;

    esac
done

# check user input

[[ -z ${SCRIPTNAME} ]] && echo "fatal: no script given. use --script=<script>" && exit 1;
[[ -z ${LOCKNAME} ]] && LOCKNAME="${DEFAULT_LOCKNAME}"

# set up directories

thisdir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
pydir="${thisdir}/py"

# request lock

echo -ne "requesting lock: ${LOCKNAME}.lock... "
lockfile-create "${LOCKNAME}"
lockfile-touch "${LOCKNAME}" &
PID_LOCKTOUCH="$!"
echo "OK. ${PID_LOCKTOUCH}"

# run script

SCRIPTPATH="${pydir}/${SCRIPTNAME}"
echo "python ${SCRIPTPATH} ${EXTRA_ARGS[*]}"
python "${SCRIPTPATH}" ${EXTRA_ARGS[*]}

# release lock

echo -ne "killing ${PID_LOCKTOUCH}... "
kill "${PID_LOCKTOUCH}"
echo -ne "OK\nreleasing lock: ${LOCKNAME}.lock... "
lockfile-remove lockfile
echo "OK"

# clean up 

unset EXTRA_ARGS
unset SCRIPTNAME
unset SCRIPTPATH
unset LOCKNAME


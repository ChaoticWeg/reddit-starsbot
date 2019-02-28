#!/bin/bash

## run.sh
## written by ChaoticWeg (Shawn Lutch)
##
## provides an easy way to treat an entire script as a critical section
## to make certain scripts block others easily
##
## depends on lockfile-progs:
##      ubuntu: $ sudo apt-get install -y lockfile-progs
##
## usage: ./run.sh [--lockfile=<lockfile>] command...
##      lockfile     name of lockfile to use. optional. default = lockfile
##      command...   the command to run

# globals

DEFAULT_LOCKNAME=lockfile

# handle command-line arguments

EXTRA_ARGS=()
LOCKNAME=

while (( "$#" )); do
    case "${1}" in

        # --lockfile=<lockfile> (default: lockfile)
        --lockfile=*) LOCKNAME=${1/--lockfile=/''}; shift;;
        --lockfile) LOCKNAME=${2}; shift; shift;;

        # not handled? toss it on the pile to handle later
        *) EXTRA_ARGS+=("${1}"); shift;;

    esac
done

# check user input

[[ -z ${LOCKNAME} ]] && LOCKNAME="${DEFAULT_LOCKNAME}"

# set up directories and pushd into this one

thisdir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
pushd "${thisdir}" >/dev/null 2>&1

# request lock

echo -ne "requesting lock: ${LOCKNAME}.lock... "
lockfile-create "${LOCKNAME}"
lockfile-touch "${LOCKNAME}" &
PID_LOCKTOUCH="$!"
echo "OK. ${PID_LOCKTOUCH}"

###
###  BEGIN CRITICAL SECTION
###

# grab credentials from creds/

credsdir="${thisdir}/creds"
mkdir -p "${credsdir}"      # create if not exist
for creds_file in $credsdir/*.sh; do source "${creds_file}"; done

# run command

COMMAND_TO_RUN="${EXTRA_ARGS[*]}"
echo -ne "${COMMAND_TO_RUN}\n\n"
eval ${COMMAND_TO_RUN}
echo -ne "\n"

###
###  END CRITICAL SECTION
###

# release lock

echo -ne "killing ${PID_LOCKTOUCH}... "
kill "${PID_LOCKTOUCH}"
echo -ne "OK\nreleasing lock: ${LOCKNAME}.lock... "
lockfile-remove "${LOCKNAME}"
echo "OK"

# clean up 

unset EXTRA_ARGS
unset SCRIPTNAME
unset SCRIPTPATH
unset LOCKNAME
popd >/dev/null 2>&1

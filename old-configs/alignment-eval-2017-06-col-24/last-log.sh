#!/bin/bash

PROGRAM=${1-echo}

SJL=/groups/flyem/data/scratchspace/sparkjoblogs
$PROGRAM ${SJL}/$(ls -tr ${SJL} | tail -n1)

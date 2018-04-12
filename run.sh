#!/bin/bash

pids=""
./beagle_run.sh 1>bgl_run.log 2>bgl_run.error.log &
pids="$pids $!"
./minimac_run.sh 1>mnmc_run.log 2>mnmc_run.error.log &
pids="$pids $!"

wait $pids
./bash.acc.eval.sh 1>/dev/null 2>/dev/null &

#!/bin/bash

while true
  do
    if pgrep trron_final >/dev/null 2>&1
      then
        echo "not restarting it"
        sleep 1m
        exit 1
      else
        python3 trron/trron_final.py
        sleep 1m
    fi
done


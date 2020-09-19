#!/usr/bin/env bash

case "$1" in
  "run")
    echo "Starting api server ..."
    exec make run
    ;;
  "tests")
    echo "Running tests ..."
    exec make tests
    ;;
  "")
    echo "No run parameter passed please use one of: [run, tests]"
    exit 1
    ;;
  *)
    echo "Unknown command '$1'. please use one of: [run, tests]"
    exit 1
    ;;
esac

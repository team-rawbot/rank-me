#!/usr/bin/env sh

for f in tests/envdir/*; do
    export $(basename $f)=$(cat $f)
done

./manage.py test $@

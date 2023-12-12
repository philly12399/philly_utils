#!/bin/bash

for i in {25001..25300}
do
  s=$(printf "%06d" "$i")
  # cp ../../../seq/seq1/$s.pcd .
  touch $s.txt
  #  rm $s.pcd
  echo $s
done

#   s=$(printf "%06d" "$i")
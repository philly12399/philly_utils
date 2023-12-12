#!/bin/bash

for i in {25000..25300}
do
  s=$(printf "%06d" "$i")
   ln ../../../pingtung-03-09-1300-2w3wpcd/$s.pcd .
  #  rm $s.pcd
  echo $s
done

#   s=$(printf "%06d" "$i")
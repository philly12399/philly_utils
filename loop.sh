#!/bin/bash

for i in {29000..29299}
do
  s=$(printf "%06d" "$i")
  cp   $s.pcd ../seq3/
  echo $s
done

#   s=$(printf "%06d" "$i")
#!/bin/bash

for i in 1 2 3
do
    sbatch 1node.sh trial_1/1node_$i
done

for i in 1 2 3
do
    sbatch 2node.sh trial_1/2node_$i
done

for i in 1 2 3
do
    sbatch 4node.sh trial_1/4node_$i
done

for i in 1 2 3
do
    sbatch 6node.sh trial_1/6node_$i
done

for i in 1 2 3
do
    sbatch 8node.sh trial_1/8node_$i
done

for i in 1 2 3
do
    sbatch 12node.sh trial_1/12node_$i
done

for i in 1 2 3
do
    sbatch 16node.sh trial_1/16node_$i
done

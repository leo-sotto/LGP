#!/bin/bash

swig -python -c++ calc_fit.i
c++ -flto -Ofast -mtune=native -march=native -fPIC -c calc_fit.cpp calc_fit_wrap.cxx -I/home/leo/anaconda3/include/python3.7m
c++ -shared calc_fit.o calc_fit_wrap.o -o _calc_fit.so


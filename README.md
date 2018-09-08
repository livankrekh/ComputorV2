# ComputorV2

Project is a simple calculator with abilities of add, multiplying, resolving real, comlplex numbers, matrices, vectors, functions

![Plotting](https://drive.google.com/uc?authuser=0&id=1JUrHWNUP7bEZULxcer9DNDsCEy72w2EO&export=download)

## Pre-installation

You need have being installed `python3` with `pip3` and `virtualenv`

## Install and run

```
> ./install.sh
> ./computor.py
```
OR

Create and enter in your own virtualenv
```
(venv) > pip3 install -r requirements.txt
(venv) > python3 computor.py
```

## Usage

At first, you can create variables of next types:

* `Real number` : every real numbers -> integer, float, results of operations (adding, sub, multiplying, division, power) 

`>> real = -23.32432`, `>> result = 234*34234 ^ 7 + 23`
* `Complex number` : complex number has next form -> `(real) + (real) * i`; `i` - imaginary number (solution)

`>> number = -4i`, `>> complex = 4.4 + -8i`
* `Matrix` : matrix has form -> `[[1,2,3,...];[1,2,3,...];...]`; symbol `**` - multiplying matrices operator

`>> A = [[1,0];[0,1]]`, `>> B = [[2,3];[2,3]]`, `>> A ** B`, `>> vector = [[1,2,3,4,5,6,7,8,9]]`
* `Function` : 

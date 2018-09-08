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
```
>> real = -23.32432
>> result = 234*34234 ^ 7 + 23
```
* `Complex number` : complex number has next form -> `(real) + (real) * i`; `i` - imaginary number (solution)
```
>> number = -4i
>> complex = 4.4 + -8i
```
* `Matrix` : matrix has form -> `[[1,2,3,...];[1,2,3,...];...]`; symbol `**` - multiplying matrices operator
```
>> A = [[1,0];[0,1]]
>> B = [[2,3];[2,3]]
>> A ** B
[2.0, 3.0]
[2.0, 3.0]
>> vector = [[1,2,3,4,5,6,7,8,9]]
```
* `Function` : function has form -> `func(x) = a * x^9 + ... + b`; `func` - function name, `x` - argument name
```
>> lol(cool) = cool^2 + 21cool + 23
>> m = [[21,3];[42,21]]
>> foo(bar) = bar^3 + 20 * m
bar^3 + 20 * [[21,3];[42,21]]
```
## Functionality

You can:
* Get variable as argument in function or include in other equition
```
>> bro = 2i
>> f(y) = y * 23 + 1.12
>> f(bro) = ?
1.12 + 46.0i
>> other(falcon) = falcon^3 + bro
falcon^3 + 2 * i
```
* Get result of equition
```
>> 2 + 34.41 - 0.1264^3 * 945 + 723 % 34 * (10 + 4.2*(0.95+31))
1332.2115840819201
>> a = 902*(30 + 65.3)
>> b = 65 - 85^2
>> a + b
78800.59999999999
>> a * b = ?
-615477895.9999999
```
* Resolve of function with degree less than 2
```
>> f(x) = -20x^2 + 3
>> f(x) = ?
-20 * x ^ 2 + 3 = 0
Polynomial degree is: 2
The solution is: x1 =  0.3872983346207417 , x2 =  -0.3872983346207417
>> f(x) = 20 ?
-20 * x ^ 2 + 3 = 20.0
Polynomial degree is: 2
The solution is: x = ( 0 +/- √-1360.0 ) / -40.0
```
* Display function graph
```
>> func(x) = -20x^19 + 30x^6 + 12.06x^3 + 18
>> plot func ?
```
![graph](https://drive.google.com/uc?authuser=0&id=1BdbL9mQ8i15sbaA-xibrKOPE6ihVagdq&export=download)

* Display matrix or vector graph
```
>> vector = [[213,341214,12,-12323,23,964,-234,-6765,-4,57,0,657567,-23487,723,8154,-872387,1000000]]
>> diagram vector ?
```
![diagram](https://drive.google.com/uc?authuser=0&id=1selzViWGO5CxRJ3jYh3VWn6dmBFNcKLk&export=download)

## Exit

`Ctrl` + `C`
OR
```
>> exit()
```

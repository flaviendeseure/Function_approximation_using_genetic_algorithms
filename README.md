[![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1W646LJHqZnAjvlj81odE8WgjC2r2xp52?usp=sharing)
[![made-with-latex](https://img.shields.io/badge/Made%20with-LaTeX-1f425f.svg)](https://www.latex-project.org/)
<p align="center">
    <h1 align="center">Function approximation using genetic algorithms</h3>
</p>

## Overview
### I. Introduction
This project aims to determine the temperature at the surface of a new unknown star at any time, from a few observations.
It is known that the temperature follows a function called Weierstrass, defined as follows:  
  
<img align="middle" src="https://render.githubusercontent.com/render/math?math=t(i)=\sum_{n=0}^c a^n\times \cos(b^n\pi i)"/>  
    
Where <img src="https://render.githubusercontent.com/render/math?math=t(i)"> is the star temperature at a given time i, with the following set of parameters:  
<img src="https://github.com/flaviendeseure/Function_approximation_using_genetic_algorithms/blob/main/Images/parameters.PNG?raw=true"/>  

To reach this objective, we need to find the appropriate (a,b,c) coefficients.  
We have at our disposal a set of temperature points measured at several instants i.


### II. Search space
The search space has the size ]0, 1\[x20x20.  
However, in Python the maximum precision is 10^15 - 1. So there are **(10^15 - 1) × 20 × 20 = 4 × 10^16 - 1 possibilities**


### III. Fitness function
I have chosen the following function for fitness:  
<img src="https://github.com/flaviendeseure/Function_approximation_using_genetic_algorithms/blob/main/Images/fitness.png?raw=true"/>  
where t is the Weierstrass function with the parameters a,b,c and n the number of observations.  
  
This function corresponds to the norm 2 of the vector of the difference between the observations and the values found.  
The choice of the norm 2 (compared to the norm 1) has the advantage to penalize the differences and thus to obtain a more optimized fitness.  


### IV. Crossovers and mutations
In order to find the best parameters of the function, I decided to use different operators for the integers b and c and the real number a.
I will therefore present the operators in a separate way
#### 1. Integers
The integers are converted into binary number and then put side by side to obtain a chromosome.
##### a. Crossover
**Method used:** Two point crossover.  
This method consists in choosing two points randomly in the chromosomes of each parent and inverting the gene sequences between these two points.
<img src="https://github.com/flaviendeseure/Function_approximation_using_genetic_algorithms/blob/main/Images/Two_point_crossover.png?raw=true" width="400"/>
##### b. Mutation
**Method used:** Multiple flip bit mutation.  
This method consists in choosing several genes randomly in the chromosome and inverting their values (0 if 1 or 1 if 0).
<img src="https://github.com/flaviendeseure/Function_approximation_using_genetic_algorithms/blob/main/Images/flip-bit-mutation.jpg?raw=true" width="400"/>

#### 2. Real numbers
##### a. Crossover
**Method used:** Simulated binary crossover.
This method imitates the properties of the Single point crossover. One of its properties is that the average of the values of the parents is equal to the average of the values of the children.    
The two children are created from the two parents using the following formula:  

<img src="https://github.com/flaviendeseure/Function_approximation_using_genetic_algorithms/blob/main/Images/offsprings.PNG?raw=true" width="200"/>

Where β, the spreading factor, is defined as follows:  

<img src="https://github.com/flaviendeseure/Function_approximation_using_genetic_algorithms/blob/main/Images/beta.PNG?raw=true" width="200"/>

With the following parameters:  
- η: between 2 and 5: (2: more variation between parents, 5: less
variations)
- u : uniformly distributed on the interval [0, 1]
<img src="https://github.com/flaviendeseure/Function_approximation_using_genetic_algorithms/blob/main/Images/Simulated_binary_crossover.jpg?raw=true" width="400"/>


##### b. Mutation
The method consists in multiplying the parent by a factor between 0.95 and 1.05.


### V. Selection
For the selection, I have chosen the best and worst individuals.  
The proportion is as follows:  
- Best individuals: 5/15
- Worst individuals: 2/15
- New individuals : 8/15
  
I have used this simple method, because it has the advantage of keeping the best individuals at each generation and to be less computationally intensive while bringing, for my case, results equivalent to other algorithms (roulette wheel, stochastic universal sampling, tournament, ranked-based,...).
  
### VI Solution
**I found the following values:**
- a = 0.3415035442650213
- b = 15
- c = 3   
  
**Parameters used and basic statistics:**
1. **Population size:** 100 individuals
2. **Average number of iterations to converge:** 57 iterations
3. **Running time over 30 iterations:**
    - Threshold for fitness: 0.19
        - Average: 6.5 seconds
        - Standard deviation: 4.5 seconds
    - Threshold for fitness: 0.1813
        - Mean: 21 seconds
        - Standard deviation: 27 seconds  
   
Note: The execution time is quite important because of the high accuracy required. 
By decreasing the requirements (for example having a precision of 10^-2), the execution time is much lower.


## Requirements
The requirements.txt file list all Python libraries that the project depends on.  
To install, use the following command:

```
pip install -r requirements.txt
```

## Getting started
There are two ways to use this project:
#### Google colab 
Simply use the link located at the top of this page  
#### Locally, on your computer  
1. Clone this repository  
2. Install the associate libraries (see requirements)
3. Two options:
    1. Open the notebook
    2. Launch the python program on your command prompt
    ```
    python path/to/cloned/repository/Genetic_algorithm.py
    ```

## Discussion
I have tested different configurations for this problem, each one having its advantages and drawbacks.

### 1. Binary Version
**Description:**
I have tested a method consisting in converting a,b and c in binary and put them side by side to form a chromosome.  
*Note:* For a, we choose a precision (10^-2 for example).  
  
**Advantages:**
- Very fast
- Very precise if you know the precision in advance  
  
**Drawbacks:**
- Not very stable
- Low accuracy if you don't choose the right precision

### 2. Modification of parameters and hyperparameters
#### a. Population size
Increasing the size of the population (while proportionally decreasing the number of iterations) does not result in better performance.
#### b. Proportion for the selection
Different proportions have been tested, for example, elitism (we keep only the best individuals). This proves to be not very efficient (divergence).
#### c. Crossing operator
I have tested the single point crossover. However, this method was less efficient than the two point crossover.
#### d. Mutation operator
I have tested the Michalewicz non-uniform mutation. However, the ratio of solution accuracy and performance was too low to justify its use.


## Authors
Flavien DESEURE--CHARRON - flavien.deseure@gmail.com - [![Linkedin](https://i.stack.imgur.com/gVE0j.png) LinkedIn](https://www.linkedin.com/in/flavien-deseure--charron/)


## References
[1] E. Wirsansky, "Hands-On Genetic Algorithms with Python:applying genetic algorithms to solve real-world deep learning and artificial intelligence problems", *Packt*, 2020  
[2] P Siarry, "Métaheuristiques", *Eyrolls*, 2014

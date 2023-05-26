### Results
#### Task 3.1
- The nim_sum_strategy had a good performance against the pure_random winning all the matches.
- The basic_strategy was almost random but it was able to beat the pure_random in some cases depending on the parameters.
#### Task 3.2
- Using the basic_strategy in a genetic algorithm the results look promissing, having some of the individuals winning all the matches of the fitness computation.
Example of individual:
- Genome: Genome(p_longest=0.79, p_take_one=0.17, p_leave_one=0.64, p_take_all=0.24)
- Fitness: 0.9

The solution was based on the code developed in class by professor Squillero.

#### Task 3.3
- The minmax strategy has the best performance not taking the nim sum algorithm.
- There is a complexity constraint regarding the depth of the tree which was upper bounded by 10. Since the minmax tree should fully grow in order to get some result for the nim game, the take_one algorithm was used when depth got bigger then 10. When the number of objects in the game start to decrease the minmax will properly function.  

The minmax solution was based on https://realpython.com/python-minimax-nim/
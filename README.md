# projecteuler923
Problem 923 of Project Euler

It seems that Project 923 is nearly impossible. Nobody I've talked to even knows where to begin. That's exactly why we're going to try to solve it. I don't care how long it takes; we WILL get there.

Before you look at any of the code,

Time complexity for 922.py in its current state is literally worse than the ackermann function, dont expect much

I have discovered that using a disjunctive sum model for the boards does not work. 

Counter example: (1,1,2),(1,1,2)
Normally computing each board would result in a sum of 2 (1 for each board), but adding the second board counterintuitively makes it a win for Down

Instead, we need to represent the game in full canonical form due to its "hot" nature - which may help us "cool" the game to a more workable state
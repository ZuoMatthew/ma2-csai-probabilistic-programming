% Much of the code of the previous example was for controlling the sequence of rolls. We’ll now change the rules to generate infinite sequences, and query for finite prefixes of these sequences (of length 5 in our case, thanks to the list pattern with five anonymous variables used in the query). Here’s a first model. We roll the first die for sure, as specified by the fact roll([1]), and if we already have seen a list of rolls, we take the first element F of the list, roll its die, and add the outcome H to the front of the extended sequence.

1/3::dice(1,D); 1/3::dice(2,D); 1/3::dice(3,D) :- die(D).
die(X) :- between(1,3,X).

roll([1]).
roll([H,F|L]) :- roll([F|L]), dice(H,F).

seen(L) :- reverse(L,[],R), roll(R).

reverse([],L,L).
reverse([H|T],A,L) :-
  reverse(T,[H|A],L).

query(seen([_,_,_,_,_])).
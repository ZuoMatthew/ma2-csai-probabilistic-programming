e(drink,alcoholic).
e(drink,nonalcoholic).
e(alcoholic,beer).
e(alcoholic,wine).
e(alcoholic,spirit).
e(nonalcoholic,soda).
e(nonalcoholic,coffee).
e(beer,ale).
e(beer,stout).
e(beer,lager).
e(wine,redwine).
e(wine,whitewine).
e(spirit,gin).
e(spirit,whiskey).

member(X,[X|_]).
member(X,[_|T]) :- member(X,T).

d(B,B,[B]).
d(B,E,[B|L]) :- e(B,M), d(M,E,L),\+member(B,L).
d(B,E,[M|L]) :- e(M,B), d(M,E,L),\+member(B,L).

P::similar(B,E) :- d(B,E,L), length(L,LL), (LL=1, P is 1; LL>1, P is 1/(LL-1)).

query(similar(ale,stout)).
query(similar(ale,gin)).
query(similar(ale,soda)).
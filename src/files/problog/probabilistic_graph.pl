% ProbLog can also be used to model probabilistic graphs, i.e., graphs in which the existence of some edges is uncertain. We can use ProbLog2 to calculate, for instance, the probability of there being a path between two given nodes.

0.6::edge(1,2).
0.1::edge(1,3).
0.4::edge(2,5).
0.3::edge(2,6).
0.3::edge(3,4).
0.8::edge(4,5).
0.2::edge(5,6).

path(X,Y) :- edge(X,Y).
path(X,Y) :- edge(X,Z),
             Y \== Z,
         path(Z,Y).

query(path(1,5)).
query(path(1,6)).
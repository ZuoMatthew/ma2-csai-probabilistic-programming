0.5::similar(ale,stout).
0.25::similar(ale,gin).
0.2::similar(ale,soda).
query(similar(ale,stout)).
query(similar(ale,gin)).
query(similar(ale,soda)).

%PROBLOG OUTPUT
%PROGRAM:
%0.5::similar(ale,stout).
%0.25::similar(ale,gin).
%0.2::similar(ale,soda).
%query(similar(ale,stout)).
%query(similar(ale,gin)).
%query(similar(ale,soda)).
%============================
%DIMACS:
%p wcnf 3 6 48929
%c 1  similar(ale,stout)
%c 2  similar(ale,gin)
%c 3  similar(ale,soda)
%c 1  similar(ale,stout)
%c 2  similar(ale,gin)
%c 3  similar(ale,soda)
%6931 -1 0
%6931 1 0
%13862 -2 0
%2876 2 0
%16094 -3 0
%2231 3 0
%============================
%EVALUATION:
%{similar(ale,stout): 0.5000000000000001, similar(ale,gin): 0.25, similar(ale,soda): 0.2}
%============================

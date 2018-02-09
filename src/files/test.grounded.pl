query(simple_parser)    .
%    comment      one two three
win_keep :- prize(1).
win_keep(2) :- prize(1), prize(2).
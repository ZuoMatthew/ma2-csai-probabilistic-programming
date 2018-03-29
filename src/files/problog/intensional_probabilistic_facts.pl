% Concretely, we allow what we call intensional probabilistic facts, which are statements of the form p::f:− body, with body a conjunction of calls to non-probabilistic facts. Also intensional annotated disjunctions can be expressed like this: p1::f1;…;pn::fn:− body.

0.7::red(X); 0.3::green(X) :- ball(X).

ball(a). ball(b). ball(c).

query(red(_)).
query(green(_)).

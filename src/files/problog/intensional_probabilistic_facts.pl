% Concretely, we allow what we call intensional probabilistic facts, which are statements of the form p::f:− body, with body a conjunction of calls to non-probabilistic facts. Also intensional annotated disjunctions can be expressed like this: p1::f1;…;pn::fn:− body.

0.7::red(X); 0.3::green(X) :- ball(X).

ball(a). ball(b). ball(c).

query(red(_)).
query(green(_)).A ProbLog program consists of two parts: a set of ground probabilistic facts, and a logic program, i.e. a set of rules and (‘non-probabilistic’) facts. A ground probabilistic fact, written p::f, is a ground fact f annotated with a probability p. We allow syntactic sugar for compactly specifying an entire set of probabilistic facts with a single statement. Concretely, we allow what we call intensional probabilistic facts, which are statements of the form p::f:− body, with body a conjunction of calls to non-probabilistic facts. Also intensional annotated disjunctions can be expressed like this: p1::f1;…;pn::fn:− body.


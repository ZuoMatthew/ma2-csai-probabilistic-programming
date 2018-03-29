% The first example (See example 6.1 in Woudenberg et al) is a predictive model to model the effects of two medications for patients with primary type-1 osteoporosis. The risks of bone fracture associated with osteoporosis, can be reduced to some small extent by treatment. Two common treatments for osteoporosis are calcium supplementation and medication with bisphosphonates. But the concurrent intake of both medications will fully cancel out the effect of the bisphosphonates and the effect of the calcium supplementation is cancelled out partially.

increaseOsteoblasts :- calcium.
0.5::\+increaseOsteoblasts :- calcium, bispho.

reduceOsteoclasts :- bispho.
1.0::\+reduceOsteoclasts :- calcium , bispho.

osteoprosis :- initialOsteoprosis.
0.85::\+osteoprosis :- reduceOsteoclasts.   % Bisphosphonates
0.15::\+osteoprosis :- increaseOsteoblasts. % Calcium

% Prior probabilities
0.5::calcium. 0.5::bispho. 0.5::initialOsteoprosis.

% Query probability of effect
evidence(initialOsteoprosis, true).
evidence(calcium, true).
evidence(bispho, false).
query(osteoprosis).
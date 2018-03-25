0.1::a. % prob = 0.1
0.2::a. % prob = 1 - (1 - prob) * (1 - 0.2) = 0.28
0.3::a. % prob = 1 - (1 - prob) * (1 - 0.3) = 0.496
0.4::a. % prob = 1 - (1 - prob) * (1 - 0.4) = 0.6976

0.5::b. % prob = 0.5
b.      % prob = 1 - (1 - prob) * (1 - 1) = 1

c.      % prob = 1
0.6::c. % prob = 1 - (1 - prob) * (1 - 0.6) = 1

query(a).
query(b).
query(c).
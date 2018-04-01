% converted from the bayesian network

0.3::smoker.
0.9::pollution("low"); 0.1::pollution("high").
0.03::cancer :- pollution("low"), smoker.
0.001::cancer :- pollution("low"), \+smoker.
0.05::cancer :- pollution("high"), smoker.
0.02::cancer :- pollution("high"), \+smoker.


0.9::xray("positive"); 0.1::xray("negative") :- cancer.
0.2::xray("positive"); 0.8::xray("negative") :- \+cancer.



0.65::dyspnoea :- cancer.
0.3::dyspnoea :- \+cancer.

query(smoker).
query(pollution("low")).
query(pollution("high")).
query(cancer).
query(xray("positive")).
query(xray("negative")).
query(dyspnoea).
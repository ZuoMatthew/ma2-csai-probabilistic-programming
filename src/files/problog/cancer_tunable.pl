t(_)::smoker.
t(_)::pollution("low"); t(_)::pollution("high").
t(_)::cancer :- pollution("low"), smoker.
t(_)::cancer :- pollution("low"), \+smoker.
t(_)::cancer :- pollution("high"), smoker.
t(_)::cancer :- pollution("high"), \+smoker.
t(_)::xray("positive"); t(_)::xray("negative") :- cancer.
t(_)::xray("positive"); t(_)::xray("negative") :- \+cancer.
t(_)::dyspnoea :- cancer.
t(_)::dyspnoea :- \+cancer.

query(smoker).
query(pollution("low")).
query(pollution("high")).
query(cancer).
query(xray("positive")).
query(xray("negative")).
query(dyspnoea).
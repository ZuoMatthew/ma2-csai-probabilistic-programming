t(0.9)::smoker.

t(_)::alpha_pollution("low").
pollution("low"):- alpha_pollution("low"), \+ pollution("high").
t(_)::alpha_pollution("high").
pollution("high") :- alpha_pollution("high"), \+ pollution("low").

t(_)::alpha_cancer_1.
cancer:- pollution("low"), smoker, alpha_cancer_1.
t(_)::alpha_cancer_2.
cancer:- pollution("low"), \+smoker, alpha_cancer_2.
t(_)::alpha_cancer_3.
cancer:- pollution("high"), smoker, alpha_cancer_3.
t(_)::alpha_cancer_4.
cancer:- pollution("high"), \+smoker, alpha_cancer_4.

% t(_)::xray("positive"); t(_)::xray("negative") :- cancer.
% t(_)::xray("positive"); t(_)::xray("negative") :- \+cancer.

t(_)::alpha_xray("positive")_1.
xray("positive")_1 :- alpha_xray("positive")_1, \+xray("negative")_1, cancer.

t(_)::alpha_xray("negative")_1.
xray("negative")_1:- alpha_xray("negative")_1, \+xray("positive")_1, cancer.

t(_)::alpha_xray("positive")_2.
xray("positive")_2 :- alpha_xray("positive")_2, \+ xray("negative")_2, \+cancer.

t(_)::alpha_xray("negative")_2.
xray("negative")_2 :- alpha_xray("negative")_2, \+ xray("positive")_2, \+cancer.

xray("positive") :- xray("positive")_1, xray("positive")_2.
xray("negative") :- xray("negative")_1, xray("negative")_2.

t(_)::dyspnoea_1.
dyspnoea:- cancer, dyspnoea_1.
t(_)::dyspnoea_2.
dyspnoea:- \+cancer, dyspnoea_2.

query(smoker).
query(pollution("low")).
query(pollution("high")).
query(cancer).
query(xray("positive")).
query(xray("negative")).
query(dyspnoea).
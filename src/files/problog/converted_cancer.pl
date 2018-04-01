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

t(_)::alpha_xray_1("positive").
xray_1("positive"):- alpha_xray_1("positive"), \+xray_1("negative"), cancer.

t(_)::alpha_xray_1("negative").
xray_1("negative"):- alpha_xray_1("negative"), \+xray_1("positive"), cancer.

t(_)::alpha_xray_2("positive").
xray_2("positive") :- alpha_xray_2("positive"), \+ xray_2("negative"), \+cancer.

t(_)::alpha_xray_2("negative").
xray_2("negative") :- alpha_xray_2("negative"), \+ xray_2("positive"), \+cancer.

xray("positive") :- xray_1("positive"), xray_2("positive").
xray("negative") :- xray_1("negative"), xray_2("negative").

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
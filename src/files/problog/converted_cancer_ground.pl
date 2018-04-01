0.9::smoker.
0.9::alpha_pollution("low").
pollution("low"):- alpha_pollution("low"), \+ pollution("high").
0.1::alpha_pollution("high").
pollution("high") :- alpha_pollution("high"), \+ pollution("low").
0.03::alpha_cancer_1.

cancer:- pollution("low"), smoker, alpha_cancer_1.
0.001::alpha_cancer_2.
cancer:- pollution("low"), \+smoker, alpha_cancer_2.
0.05::alpha_cancer_3.
cancer:- pollution("high"), smoker, alpha_cancer_3.
0.02::alpha_cancer_4.
cancer:- pollution("high"), \+smoker, alpha_cancer_4.

0.9::alpha_xray_1("positive").
xray_1("positive"):- alpha_xray_1("positive"), \+xray_1("negative"), cancer.
0.1::alpha_xray_1("negative").
xray_1("negative"):- alpha_xray_1("negative"), \+xray_1("positive"), cancer.
0.2::alpha_xray_2("positive").
xray_2("positive") :- alpha_xray_2("positive"), \+ xray_2("negative"), \+cancer.
0.8::alpha_xray_2("negative").

xray_2("negative") :- alpha_xray_2("negative"), \+ xray_2("positive"), \+cancer.
xray("positive") :- xray_1("positive"), xray_2("positive").
xray("negative") :- xray_1("negative"), xray_2("negative").
0.65::dyspnoea_1.
dyspnoea:- cancer, dyspnoea_1.
0.3::dyspnoea_2.
dyspnoea:- \+cancer, dyspnoea_2.

query(smoker).
query(pollution("low")).
query(pollution("high")).
query(cancer).
query(xray("positive")).
query(xray("negative")).
query(dyspnoea).
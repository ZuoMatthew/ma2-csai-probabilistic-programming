# Inference for Statistical Relational Learning
The goal of the Probabilistic Programming assignment is to build your own state-of-the-art inference and learning engine for probabilistic graphical models such as Bayesian networks and statistical relational models.

## Usage
The program can evaluate ProbLog programs and Bayesian networks.

### Problog programs
To evaluate ProbLog programs:
```sh
python3 scripts/inference.py --problog files/problog/ball_colors_and_types.pl
```
The underlying model counter that is used for evaluation can be set with the `--model_counter` parameter. It can be `minic2d` or `sdd`.

The program will print the following steps of the inference pipeline:
* The ground version of the input program
* The ground program converted to a First Order Logic theory
* The ground program in a CNF encoding
* The CNF encoding in dimacs format
* The results using our pipeline
* The results using the problog library

### Bayesian networks
For Bayesian networks, the process is a bit different.
The following command will convert the Bayesian network to a ground ProbLog program and run the pipeline on it.
```sh
python3 scripts/inference.py -bn files/networks/earthquake.net
```
The output will contain the same elements mentioned above. However, as there are no queries in the ground ProbLog program, there will be nothing to evaluate. In order to add queries, simply copy the ground ProbLog output of the program to a new file and add the queries you want. Then run the command for evaluating a ProbLog file.

Bayesian networks in the following file formats are supported: uai, net, xdsl, xml. The networks are converted to ProbLog code using [conversion scripts](/src/problog_conversions) taken (and slightly adapted) from the [ProbLog repository](https://github.com/jordn/ProbLog).

### Parameter learning
There is support for parameter learning. To do this, the program expects a file containing tunable probabilities and another file containing values for all probabilities (the ground truth). The ground truth is necessary for generation of interpretations (training evidence). The amount of interpretations to be generated can be set as well.

```sh
python3 scripts/inference.py --problog_learn file --problog_learn_truth file_ground_truth --learning_interpretations 100
```
The interpretations that were generated for the execution will be written to src/files/interpretations.txt.

#### Note
The file with tunable probabilities needs to be in ground ProbLog form and cannot contain any comments. This is because we uses the problog library to ground files, and the library cannot ground files with tunable probabilities.

Also, in order to generate interpretations, the file with the ground truth must have `query(...).` statements for all predicates for which evidence should be generated.

### Tests
Tests have been created to make sure our pipeline delivers the same results as the problog library. They can be ran as follows:
```sh
python3 tests/pipeline.py
```
The ProbLog code used for testing is mainly taken from the online [ProbLog tutorial](https://dtai.cs.kuleuven.be/problog/tutorial.html).

## Dependencies
* Python >= 3.6
* graphviz

### MiniC2D
The program relies on the MiniC2D package in model_counters/ to be installed. To install it, simply unpack them and run make. MiniC2D might return compilation errors with g++ versions greater than 4.8. To fix this issue, install an older compiler and explicitly add your version in MiniC2D's makefile.

The code of the MiniC2D package in model_counters/ has been edited to make it return results with higher precision.

## Python dependencies
To install most of the Python dependencies.
```sh
pip3 install --upgrade setuptools
pip3 install -r requirements.txt
```
The program relies on PySDD for model counting using SDDs. To install PySDD, see the [compilation instructions](https://github.com/wannesm/PySDD).

## Papers
- [Mark Chavira and Adnan Darwiche. “On probabilistic inference by weighted model counting”. In: Artificial Intelligence 172.6 (2008), pp. 772–799.](http://www.sciencedirect.com/science/article/pii/S0004370207001889)
- [Arthur Choi, Doga Kisa, and Adnan Darwiche. “Compiling Probabilistic Graphical Models using Sentential Decision Diagrams”. In: Proceedings of the 12th European Conference on Symbolic and Quantitative Approaches to Reasoning with Uncertainty (ECSQARU). 2013.](https://link.springer.com/content/pdf/10.1007%2F978-3-642-39091-3.pdf)
- [Daan Fierens, Guy Van den Broeck, Ingo Thon, Bernd Gutmann, and Luc De Raedt. “Inference in probabilistic logic programs using weighted CNFs”. In: Theory and Practice of Logic Programming 15 (2015).](https://www.noexperiencenecessarybook.com/OvZm2/inference-in-probabilistic-logic-programs-using-weighted-cnf-39-s.html)
- [Bernd Gutmann, Ingo Thon, and Luc De Raedt. “Learning the Parameters of Probabilistic Logic Programs
from Interpretations”. In: European Conference on Machine Learning and Knowledge Discovery in Databases
(ECML/PKDD) (2011), pp. 581–596.](https://link.springer.com/content/pdf/10.1007%2F978-3-642-23780-5.pdf)
- [Umut Oztok and Adnan Darwiche. “A top-down compiler for sentential decision diagrams”. In: Proceed-
ings of the 24th International Conference on Artificial Intelligence (IJCAI). 2015.](http://www.ijcai.org/Proceedings/15/Papers/443.pdf)
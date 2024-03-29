<p align="center">
<img src="https://github.com/softsys4ai/FlexiBO/blob/master/reports/figures/implementation.png" width="100%" height="100%" title="FlexiBO logo">
<p>


A multi-objective optimization algorithm to optimize multiple objectives of 
different costs. Currently, we support multi-objective optimization of two 
different objectives using gaussian process (GP) and random forest (RF) surrogate 
models. We implement this method to optimize accuracy and energy consumption of 
different deep neural networks.

## Instructions 
Our approach is developed to perform multi-objective optimization on resource constrained
devices specially NVIDIA Jetson Tegra X2 (TX2) and NVIDIA Jetson Xavier. To run 
FlexiBO please resolve the following dependencies:
* GPy
* apscheduler
* scikit-learn
* PyTorch
* Keras (Tensorflow)

## Reviews and Rebuttals (ICPE'20 (Rejected) -> IJCAI'20 (Rejected) -> JAIR'23 (Accepted))
We thank the reviewers of IJCAI'20, ICPE'20 and JAIR for their valuable feedbacks. Their
reviews and the rebuttals can be found here.
* [JAIR'23 reviews](https://github.com/softsys4ai/FlexiBO/blob/master/reports/JAIR.md)
* [IJCAI'20 reviews and rebuttals](https://github.com/softsys4ai/FlexiBO/blob/master/reports/IJCAI.md)
* [ICPE'20 reviews](https://github.com/softsys4ai/FlexiBO/blob/master/reports/ICPE.md)


## Run
To run FlexiBO in online mode use the following command:
```python
command: python RunFlexiBO.py -m online -d data -s surrogate
```
For example, to run optimization with GP in online with measurements.csv as initial data use: 
```python
command: python RunFlexiBO.py -m online -d measurements.csv -s GP

To run FlexiBO in offline mode use the following command:
```python
command: python RunFlexiBO.py -m offline -d data -s surrogate
```
For example, to run optimization with RF in online with measurements.csv as initial data use: 
```python
command: python RunFlexiBO.py -m offline -d measurements.csv -s RF
```


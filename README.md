# FlexiBO
A multi-objective optimization algorithm to optimize multiple objectives of 
different costs. Currently, we support multi-objective optimization of two 
different objectives using gaussian process (GP) and random forest (RF) surrogate 
models. We implement this method to optimize accuracy and energy consumption of 
different deep neural networks.

## Instructions 
FlexiBO is developed to perform multi-objective optimization on resource constrained
devices specially NVIDIA Jetson Tegra X2 (TX2) and NVIDIA Jetson Xavier. To run 
FlexiBO please resolve the following dependencies:
* GPy
* apscheduler
* scikit-learn
* PyTorch
* Keras (Tensorflow)


## Run
To run FlexiBO use the following command:
```python
command: python RunFlexiBO.py [surrogate model]
```
For example, to run optimization with GP use: 
```python
command: python RunFlexiBO.py GP
```

## Citing this work

If you use Athena for academic or industrial research, please feel free to cite the following [paper](https://arxiv.org/pdf/2001.00308.pdf):

```
@article{athena2020,
  title={FlexiBO: Cost-Aware Multi-Objective Optimization of Deep Neural Networks},
  author={Iqbal, Shahriar and Su, Jianhai and Kotthoff, Lars and Jamshidi, Pooyan},
  year={2020}
}
```

## Contacts

* Md Shahriar Iqbal (miqbal@email.sc.edu)
* [Pooyan Jamshidi](https://pooyanjamshidi.github.io/)


## Acknowledgments

This project has been partially supported by: 
* AFRL and DARPA (FA8750-16-2-0042)
* ASPIRE grant from the Office ofthe Vice President for Research at the University of South Carolina
* Google via GCP cloud research credits

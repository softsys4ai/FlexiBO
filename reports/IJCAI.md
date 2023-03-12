# IJCAI 2020 Reviews

## Reviews
### Review 1
    1. Comments to authors
        In this paper, the authors proposes a cost-aware Bayesian optimization algorithm that takes into consideration the cost of each objective during the search.

        I generally find the premise quite interesting. The idea of evaluating an objective only when it is most beneficial, is indeed intriguing. However, I have the following comments:

        Comments:
        1. It is unclear why a dominated point would become non-dominated in subsequent iterations. This inclusion, while stated, is not properly justified.
        2. By choosing a point and an objective to evaluate based on the change in volume of the pareto region, which is defined based on the pessimistic and optimistic pareto fronts, will the search algorithm excessively favor exploration rather than exploitation? It seems that the portion of the pareto region that might be largest would be associated with the highest model uncertainty.
        3. I found the plots to be rather small and difficult to properly make out, particularly Figure 2.
        4. The definitions of GP and RF are missing. Further, the configurations of these surrogate models are not also defined.
        5. I find Table 2 somewhat confusing. As the proposed FlexiBO does not evaluate every objective at every iteration, is the comparisons of Table 2, at 200 iterations, a fair one? After all, by not evaluating every objective at every iteration, there is a savings in cost but, presumably, at the expense of rate of progress.
        6. Figure 6 shows the min hypervolume vs. iterations. The definition of "steps" as described in the next in relation to this figure is unclear. Further, as the other optimization algorithms evaluate every objective at every iteration while FlexiBO does not, is the comparison here fair? Would something along the lines of hypervolume vs. some measure of cost incurred be more suitable?

        Typo:
        1. eq (1). Bold f?
        2. Anonymized Appendix is empty.
        3. In eq. 6, is the x for the multiplication operation necessary?

### Review 2

    1. Comments to authors
        Summary
        The paper considers the problem of optimizing the hyperparameters of a deep neural network system where each objective has a different cost for evaluation. A Bayesian optimization based solution namely FlexiBO is proposed to solve the problem. The key idea is to find the input point and the objective that leads to the largest reduction in the volume of a Pareto region per unit cost of the objective. Experiments are performed on 7 different tasks.


        Detailed Comments and Questions

        1. The novelty of the proposed approach is limited. The proposed approach is a simple combination of two key ideas from PAL (constructing pessimistic and optimistic regions) and PESMO [1] (decoupled evaluation of objectives). The proposed modifications are not justified properly as well. For example, "but instead, we consider all the points x \in E to determine dominance" is not provided with justification. Ideally, a theoretical analysis should be provided in terms of bounds on maximum hypervolume error (similar to PAL) or convergence bounds in terms of a suitable regret metric defined over multi-objective functions.

        2. The paper deserves credit for evaluation on multiple datasets. However, the results of the proposed approach are not satisfactory. Although the proposed method performs well in terms of diversity and R2 indicator, PAL finds equally good quality pareto fronts as the proposed method (Figure 2).

        3. Some descriptions in the paper doesn't seem correct. For example: "the set of solutions inside the Pareto region are classified as the Pareto-optimal solutions", is it the correct definition for Pareto-optimal solutions? Is this description defined with respect to the true (black-box) objective functions?

        4. PAL results are missing in Figure 6. Are they overlapping with other methods? Why is the variance of the results not shown in Figure 2 and Figure 6?

        5. If we are using decoupled evaluations, the surrogate model corresponding to the objective with less evaluations will be less accurate. It will be nice to quantify how does it affect the accuracy and convergence of the algorithm?

        6. How is the volume of the Pareto Region computed in Equation (5)? If it is computed via the hypervolume metric, then the method might not be scalable beyond few objectives since the complexity of hypervolume is exponential in the number of objective functions [2].

        7. Lobato et. al.[1] first used the idea of decoupled evaluations for designing neural network hardware accelerators. To better see the effectiveness of the approach, please consider comparing the proposed method with that implementation.


        References

        [1] Jose Miguel Hernandez-Lobato, Michael A Gelbart, Brandon Reagen, Robert Adolf, Daniel Hernandez-Lobato, Paul N Whatmough, David Brooks, Gu-Yeon Wei, and Ryan P Adams. Designing neural network hardware accelerators with decoupled objective evaluations. In NIPS workshop on Bayesian Optimization, page 10, 2016.

        [2] C. M. Fonseca, L. Paquete, and M. López-Ibáñez, “An improved dimension-sweep algorithm for the hypervolume indicator,” in CEC 2006, IEEE Congress on Evolutionary Computation, (Vancouver, Canada), pp. 1157--1163, July 2006.

### Review 3

    1. Comments to authors
        The authors describe a novel algorithm called FlexiBO for Bayesian multi-objective optimization. The algorithm is then used to optimize the hyper-parameters of deep neural networks and hardware parameters while optimizing the performance and electricity consumption of the resulting DNN.

        The algorithm itself is quite interesting and novel, however, the presentation is relatively poor and should be significantly improved. The paper contains some abbreviations and notions that are never explained (GP, RF, Contribution rate indicator). In fact, even the optimization objectives are never explicitly defined. More specifically, i suggest the following improvements:

        1. Section 3.2 should be better explained - maybe even add a figure showing the process.
        2. Figure 1 on the other hand is quite useless as it is never explained.
        3. Some steps of the algorithm should be better explained - how is the volume of the Pareto region computed? How are the pessimistic and optimistic fronts obtained (also related to first comment)?
        4. In the experiments - define explicitly what are the objectives and how they are measured and also what is the configuration/design space. I do not see how you can measure one without measuring the other (it seems that in order to get the consumption, we have to train the model and measure it, but at that point, we also get the performance of the model for free, and vice versa).
        5. It is not clear, why the accuracy measurements are not subject to noise - the initialization of the network is random, therefore we can get different performance in different runs with the same settings. Or does this point rather mention the performance of an already trained network?

        Overall, the paper needs a lot of work on presentation so that it is easier to understand and more self-contained, the authors provided link to anonymized appendix that however it does not work and additionally it is not allowed by the conference (it is also not anonymous, Dropbox showed me who shared the link the first time I clicked it).

### Review 4

    1. Comments to authors
        Summary
        The paper proposes a solution named FlexiBO for hyperparameters tuning of a deep neural network. The method targets the issue of optimizing multiple objectives where each of the objectives can have different costs for the same evaluation. Additionally, the input can affect the cost of the objectives. The goal is to reach the inputs (Pareto set) that provides the best tradeoff between the functions while accounting for the cost of each function


        Detailed Comments and Questions
        Pros :

        1. The paper is addressing an existing issue from a different angle
        2. Several datasets were evaluated.
        Cons:
        1. The paper contribution is very weak. The proposed work is a mix between two existing approaches: PAL and PESMO (decoupled version)
        2. The decoupled approach in multi-objective settings does not make a strong case and even in PESMO, the decoupled approach was proposed as an addition to a very principled approach and was not the main contribution. The main idea behind solving multi-objective optimization is to evaluate all objectives at the same time. Not evaluating all of them, brings several questions namely: A Pareto front point is defined by all the functions so how can we know the success of the method if we are not looking at the actual values of all the functions. Also, the surrogate model will not be equally contributing to the optimization process if they are not fitted to the same points for all functions.
        3. If the paper is inheriting the decoupled approach from PESMO, it should compare to the decoupled version of PESMO in the experiments.
        4. Several state-of-the-art methods are missing in the experiments: SUR, EHI, and MESMO.
        5. The results do not seem promising. In most of the experiments, FlexiBO is either not outperforming the state-of-the-art methods or outperforming them at the few last iterations. Knowing that BO methods are designed for expensive experiments, convergence speed is very important.
        6. PAL (and other BO methods ) had a theoretical convergence proof. Since FlexiBO does not always outperform state-of-the-art methods in practice, a meaningful contribution could have been an enhancement over the theoretical guarantee provided by PAL.


## Rebuttals
### Review 1
We appreciate the feedback and suggestions made by the reviewer. In response to the reviewer's concern about the justification of dominated points becoming non-dominated in later iterations, our intuition is that in earlier iterations the predictions are not very accurate and have larger differences from the actual value. Therefore, a dominant point can become non-dominated in future iterations as more samples are used. To account for the exploration and exploitation tradeoff we use a scaling parameter, Beta, for the tradeoff that determines how large the uncertainty region is with respect to the uncertainty of that prediction. This ensures we explore more in the earlier iterations and exploit more in the later iterations for better trade-offs as the value of Beta is dependent on the iteration number. We agree with the other comments of the reviewer and will improve the size of Figure 2, include definitions for the terms like GP and RF pointed out by the reviewer and correct the typos, links in the final version.  

### Review 2
We appreciate the feedback and suggestions made by the reviewer. We completely agree with the reviewer's comment about including proofs or theoretical analysis as our future work. According to our definition of the Pareto region, all the points inside the region are non-dominated and will be Pareto-optimal(#2). Difference between the area dominated by Optimistic and Pessimistic Pareto front(#6). We also plan to include the Lobato et. al. and Fonseca et. al. approaches for comparison in the future.

### Review 3
We appreciate the feedback and suggestions made by the reviewer. We have put the symbols, notations, hyperparameters of the surrogate models and intuition behind choosing them in the supplementary materials (link in the paper). We used accuracy and energy consumption as two objectives for our work. We agree with the concern raised by the reviewer about the noise for accuracy measurements in non-pre-trained models, however, we use a fixed random seed for initialization before training a model that should be possible to reproduce with very little noise. In future work, we can also consider the noise for accuracy but due to the high cost for training, we did not account for this in FlexiBO. We firmly believe this would not impact the results obtained by much.

### Review 4
We appreciate the feedback and suggestions made by the reviewer. We agree with the reviewer's comment#2, however, the surrogate models do not need to contribute equally and that was the key point of our approach. So the surrogate model is much more accurate on the cheaper function and the hypothesis is that it helps to skip rather unnecessary function evaluations on the expensive function. In other words, by skipping such function evaluations on the expensive function, the optimizer is able to traverse the multi-objective response surface with cheaper cost by employing a rather less accurate surrogate model for the expensive function compared with the cheaper ones. We respectfully disagree with the promise of the results made by the reviewer as we have shown that FlexiBO can achieve almost similar Pareto fronts in comparison with others with significantly less time/cost (80.23%). Given the same cost, FlexiBO builds Pareto fronts of better quality.
 


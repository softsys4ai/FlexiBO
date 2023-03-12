# JAIR Reviews
## Reviewer A:

This paper proposed a cost-aware decoupled evaluation strategy for multi-objective Bayesian optimization (FLEXIBO). This approach selects a design and an objective for evaluation at each interaction. When deciding which design and objective to evaluate, it trades off the additional information gained through this evaluation with the cost of running the evaluation. 

This paper then conducted extensive experiments on multiple architectures and datasets to show that the proposed method (FLEXIBO) outperforms various other algorithms in searching Pareto optimal designs. In the experiments, this paper also compared the performance of FLEXIBO under different objective evaluation functions and surrogate models. 

It's a very important research direction to design search algorithms to more efficiently find designs that provide optimal trade-offs among multiple objectives. This paper makes progress in this direction by designing a cost-aware decoupled MOBO approach. This paper is well-written. The algorithm is well explained. This paper also provided an extensive review of the literature and carefully compared different algorithms. Extensive experiments were provided to demonstrate the effectiveness of the proposed algorithm and also to study different design choices in the algorithm. Code was also provided for better reproducibility of the experimental results. I think this work advances the design of algorithms that find Pareto-optimal designs. I recommend acceptance of this work. 

 

 

Recommendation: Accept


## Reviewer B:

Summary:

This paper proposes a multi-objective Bayesian optimization approach FlexiBO. Unlike previous methods, FlexiBO is both cost-aware and decoupled. The authors clearly explain the motivation and perform extensive experiments and ablations to show the effectiveness of FlexiBO.

Questions:

- The cost-aware part is easy to understand, while the decoupled part is harder to follow and requires more explanations and experiments. The description of PESMO-DEC that introduces the decoupled appraoch is not clear either. Do you mean that the evaluation cost and the amount of information obtained are decoupled?

- For compared baselines, which surrogate model are they using, Gaussian process or Random Forest? From Figure 19, the proposed FlexiBO performs no better than baseline methods if using Random Forest as the surrogate model. As there are many design choices in the MOBO approaches, did you also make sure that the baselines are well-tuned? This is make sure that combining cost-aware and decoupling, which is the main contribution of the paper, is indeed helpful.

Recommendation: Accept with minor revisions

### Reviewer C:

Summary:

In this paper, the authors developed a novel decoupled cost-aware approach, Flexible Multi-Objective Bayesian Optimization (FlexiBO), which weights the improvement of the hypervolume of the Pareto region by the measurement cost of each objective. This helps balance the expense of collecting new information with the knowledge gained through objective evaluations, prevent from performing expensive measurements for little to no gain. The authors evaluated FlexiBO on seven state-of-the-art DNNs for image recognition, NLP, and speech-to-text translation tasks.

 

Comments: 

What’s the major difference between the proposed FlexiBO and traditional MOBO strategies? The authors may want to highlight this difference more clearly. It seems that the FlexiBO just introduced the step evaluation cost to reweight the acquisition function in the existing MOBO framework.  
There lacks comparison with more recent NAS strategies such as DARTS and many follow-up work after DARTS
Liu, Hanxiao, Karen Simonyan, and Yiming Yang. "Darts: Differentiable architecture search." arXiv preprint arXiv:1806.09055 (2018).

The compared baselines are usually quite outdated.

1. How does energy consumption defined in the actual experiments? I am not very clear what this is actually referring to?

2. How does the Hypervolume Error calculated in the real-world experiments such as resnet training? A bit more details would be helpful.

Recommendation: Accept with minor revisions


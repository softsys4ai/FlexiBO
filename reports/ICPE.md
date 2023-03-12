#ICPE Reviews:


SUBMISSION: 58
TITLE: FlexiBO: A Cost-Aware Multi-Objective Optimization Algorithm to Optimize Deep Neural Network Systems

## Review 1
 SUBMISSION: 58


### ----------- Overall Evaluation -----------
 SCORE: 2 (accept)
### ----------- Article summary -----------
 the manuscript addresses the problem of optimizing design of a Deep Neural Network (DNN) with respect to multiple objectives, whose evaluation subtends strongly different computational efforts and possible limitations given by resource-constrained running environments (e.g.: evaluation of the time spent in training takes much longer time than evaluation of the inference performance; tasks performed at the edge ar subject to stronger limitations; ... ).
 The manuscript proposes a Bayesian multi-objective optimization algorithm (FlexiBO) that conditions optimization search on the different cost of multiple objectives so as to balance the gain in information with its cost, and to efficiently select the points (i.e. DNN configurations) that are more likely to enlarge the Pareto-front of optimization. To this end, selection of sampled points is driven by surrogate regression models (a Gaussian Process or a Random Forest) that provide a measure of uncertainty associated with each objective.
 Experimental results obtained on a suite of DNNs from the literature (8 different architectures, designed for domains of object detection, Natural Language Processing and speech recognition) indicate that for a fixed search cost, the approach permits a significant gain in the identification of the Pareto front with respect to the state of the art benchmark. As a part of contribution, the work is accompanied by a significant dataset reporting on experiments taken.
### ----------- Main strengths -----------
 The paper is very well written, with concepts always introduced in a way that couples intuition and sharpness, smoothing the difficulty and the dependency on concepts that may be not common in the audience of this Conference. Technical treatment is clean and definitely sound (I'm not able to tell about DNNs, but this seems not to be the core point but rather just a kind of killer application for the proposed technique), built on an educated ground and accompanied by a relevant experimentation. Overall the work contributes to the wider and timely subject of engineering the performance of applications that rely on machine learning approaches.
### ----------- Main weaknesses -----------
 The work has relevant roots in the areas of (multi-objective) optimization and Deep Neural Networks, which might be not completely accessible to the average audience of this Conference.
### ----------- Details and suggestions for improvement -----------
 just a comment because this is required: I guess that the same approach might be applied to optimization of design of a large class of software intensive systems, not restrained to the case of Deep Neural Networks.
### ----------- Suggested references -----------
 I have not additional references to suggest
### ----------- Explanation of the overall score -----------
 I like this paper, for the subject it addresses, the way how it develops on the ground of optimization methods, the quality of presentation, the concreteness of experimentation.
 I have a really basic understanding about Deep Neural Networks.
### ----------- Artifact link -----------
 SELECTION: no

## Review 2
### ----------- Overall Evaluation -----------
 SCORE: -2 (reject)
### ----------- Article summary -----------
The paper develops a method for multi-objective bayesian optimization that takes into account the fact that evaluating different objective functions can have different costs. This is the case for training of (deep) neural networks, where evaluating the accuracy of the network (e.g., after changing its topology) requires performing a full new training, unlike evaluating its power consumption when used in inference (e.g., after changing the CPU frequency), which can be done at a fraction of the cost.

The proposed solution builds on PAL, a previously proposed multi-objective optimization framework, and revises it by proposing an acquisition function that incorporates the cost incurred for evaluation cost.

The solution is evaluated on a range of different deep neural networks.
### ----------- Main strengths -----------
 + Very timely and relevant topic
 + The proposed acquisition function is interesting and makes a lot of sense
 + Solid experimental study
### ----------- Main weaknesses -----------
 + The writing, especially of the technical parts, is often unclear and imprecise
 + The real novel technical contribution is the definition of the new acquisition, whereas the base optimization framework is the one of PAL. This is unclear until reaching the last page of the paper.
 + The idea of factoring in the cost of testing a configuration is far from being new (see, e.g., Expected improvement per second [1])
### ----------- Details and suggestions for improvement -----------
 + As I detail below there are several imprecisions in the presentation of the technical contributions of the paper that hinder severely the readability of the paper. In its current form, the paper is very hard to parse and below you find several suggestions on how to clarify the parts that I found unclear.

 + My understanding is that the real novel technical contribution of the paper lies in the definition of a new acquisition function, whereas the "base" multi-objective optimization method (in particular the definition of the optimistic and pessimistic Pareto fronts) was originally presented in PAL. The authors mention that their approach is "reasonably similar" to PAL only in the last page of the paper. I find this quite deceptive for the reader and unfair to the authors of PAL. My recommendation is that the paper introduces a preliminary section on PAL, clarifying what are the advantages and limitations of this approach in the considered context, before presenting their contributions.

 + The idea of keeping into account the cost of testing a configuration is not new and there are relatively easy ways for incorporating this factor in standard acquisition functions. Snoek et al. [1] (see the references suggested below), for instance, propose the use of expected improvement per second, i.e., the ratio of the expected improvement of an untested configuration and the time needed to test that configuration. This seems very similar in spirit to what is proposed in the paper, although the paper considers a multi-objective optimization problem, unlike Shoek et al. [1]. Relations with this type of approaches should be discussed in the related work and I would recommend also including a comparison wiith such an acquisition function in the experimental evaluation.

 Detailed comments:
 - when introducing the RF in 2.1.2, mention how diversity is introduced among the various decision trees. I guess you are using different features, but the current description is too vague. Also, at some point in the paper (e.g., in 2.1.1) you should say which kernel you use for GPs and how you trained them.
 - 2.3 Pareo-volume => Pareto-volume
 - 2.3 "Let Pareto-fronts P1, P2, P3..., Pk , are obtained" => Let P1, P2, P3..., Pk  be Pareto-fronts obtained
 - 2.3 The sentence that starts with "To compute CR we combine all the Pareto-fronts" has a type-setting problem at its end.
 - 2.3 What is a "standardized" pareto front? You use it without defining.
 - 2.3. what does r mean in I_{H}(P,r)? it does not seem to be used at all in the definition.
 - 2.3  When you introduce the Diversity Measure you mention a reference set, but you don't define it. Also, clarify if this is a metric you are proposing or was already proposed elsewhere in the literature.
 - Equations 11 and 12 are not precise: they lack to clarify that the predicate must be true for all objectives. The same imprecision is done in the pseudo-code of algorithm 1.
 - Algorithm 2 is not explained clearly in the text. Since this appears to coincide with the PAL approach, I suggest that you omit the pseudo-code (which is quite dense) and present the general idea of how the pessimistic and optimistic pareto fronts are built into a background section where you describe the PAL approach.
 - Equation 13 returns the next sample x_{t+1} and not the objective O_i, as stated right before Equation 13. Since this is the main novel contribution of the paper this part should be crystal clear, whereas it is, unfortunately, quite confusing.
 - In Section 5 I had a hard time to map Steps 2 and 3 to the algorithm presented earlier (which, as I already mentioned, is not presented very clearly). After reading the algorithm description in Section 4 I understood that by maximizing the acquisition function (i.e., Eq. 13), you had already deterrmined which configuration to test AND which objective to evaluate.
 - In Section 6.1, it would be useful to provide information on the size of the search space, on the time required to sample a configuration (on average, min/max), to evaluate the two considered objective functions, as well as to determine what configuration to sample next.
 - In Section 6.2.2, you write that in FCM "the optimization methods are allowed to run until the stopping criterion is satisfied or maximum number of iterations is reached". I may have missed it but I could not find anywhere what is the stopping criterion you used.
### ----------- Suggested references -----------
 [1] Jasper Snoek, Hugo Larochelle, Ryan P. Adams: Practical Bayesian Optimization of Machine Learning Algorithms. NIPS 2012: 2960-2968
### ----------- Explanation of the overall score -----------
 I think that the paper makes a potentially interesting contribution by proposing the use of a novel cost-aware acquisition function that can be used in the context of multi-objective bayesian optimization. However, in its current form, I do not believe that the paper is ready for publication. The two main points that I recommend to address are: i) presenting the proposed contribution in the right perspective with respect to PAL and other cost-aware acquisition functions for BO; ii) fixing the several technical imprecisions that currently hinder the understanding of the proposed technique.
### ----------- Artifacts -----------
 The code and the datasets.
### ----------- Artifact link -----------
 SELECTION: yes



## Review 3
 
### ----------- Overall Evaluation -----------
 SCORE: 2 (accept)
### ----------- Article summary -----------
The authors propose an algorithm for detecting the Pareto-front of multiple objectives for designing deep neural networks (DNN). The novelty of the work lies in the consideration of the varying evaluation costs of each objective. This is done by an effective selection of DNN configurations to be tested through a predictive model of their evaluation cost and potential information gain. The paper is well written and easy to follow despite heavy technical content. It is particularly valuable that authors share the measurements and scripts for the reproducibility of their results. I believe this would be a strong contribution provided that the following minor issues are clarified.
### ----------- Main strengths -----------
 1. well written
 2. strong technical content
 3. timely
### ----------- Main weaknesses -----------
 1. The choice of Bayesian optimization is not motivated or justified. What are the possible alternatives and why Bayesian optimization is better? The same goes for the selection of the particular surrogate models.

 2. A formal definition of the problem (e.g. as a linear program) in Section 3 would avoid potential ambiguities.

 3. In certain cases, updating the model may be possible instead of complete retraining as suggested in step 4 of the FlexiBO. This would significantly reduce the evaluation cost. A discussion on this would be useful.
### ----------- Details and suggestions for improvement -----------
 please see previous section
### ----------- Suggested references -----------
 
### ----------- Explanation of the overall score -----------
 Timely and well written article, of particular interest for ICPE community.
### ----------- Artifacts -----------
 authors share measurements and scripts.
### ----------- Artifact link -----------
 SELECTION: yes

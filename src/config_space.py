import itertools
import pandas as pd
import numpy as np

class ConfigSpaceReal:
    """This class is used to create configuration space for real cases for DNN systems
    """
    def __init__(self, layer1, layer2, 
                layer3):
        print ("[STATUS]: initializing configreal class")
        self.LAYER1=layer1 
        self.LAYER2=layer2 
        self.LAYER3=layer3
        self.set_design_space()

    def set_design_space(self):
        """This function is used to set design space for real cases"""
      
        import yaml
        with open("config.yaml","r") as fp:
            config=yaml.load(fp)
        config=config["config"]["design_space"]
        # build design space
        bounds=list()
        for key, _ in config.items():
            if (key==self.LAYER1 or key==self.LAYER2 or key==self.LAYER3):
                cur=config[key]
                for _, val in cur.items():
                    bounds.append(val)

        permutation = list(itertools.product(*bounds))
        return (
                [list(x) for x in permutation],
                [{"o1":False, "o2":False} for _ in permutation],
                [{"o1":False, "o2":False} for _ in permutation])

class ConfigSpaceSynthetic:
    """This class is used to create configuration space for synthetic cases
    """
    def __init__(self):
        print ("[STATUS]: initializing configsynthetic class")
        self.n_var = 3

    def set_design_space(self):
        """This function is used to set design space for synthetic functions"""

        self.X = np.random.random((100,self.n_var))
        return (
                [list(i) for i in self.X],
                [{"o1":False, "o2":False} for _ in self.X],
                [{"o1":False, "o2":False} for _ in self.X])

    def set_evaluation(self):
        """This function is used to evaluate synthetic objective functions"""
        from objective_synthetic import ObjectiveSynthetic
        OS=ObjectiveSynthetic()
        (Y1,
        Y2) = OS.Kursawe(self.X, self.n_var)
        Y1=[[i] for i in Y1]
        Y2=[[i] for i in Y2]

        (init_X,
        init_Y1,
        init_Y2,
        init_index)=OS.initialize(self.X,
                     Y1,
                     Y2)
        return (
                Y1,
                Y2,
                init_X,
                init_Y1,
                init_Y2,
                init_index)


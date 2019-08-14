import Config
from Utils import Utils


class FlexiBO(object):
    """This class is used to implement an active learning approach to optimize
    multiple objectives of different cost
    design space: E
    """
    def __init__(self):
        print ("Initializing FlexiBO class")
        self.utils=Utils()
        self.E=self.utils.create_design_space(Config.bounds)
 

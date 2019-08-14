import itertools

class Utils(object):
    def __init__(self):
        print ("Initializing Utils Class")
    
    def create_design_space(self,
                           bounds):
        """This function is used to create discrete design space usign bounds
        @input: bounds
        @output: design space- X
        """
        return list(itertools.product(*bounds))

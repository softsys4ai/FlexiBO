"""-----------------------------------------------------------------------------
@Name: Flexible Bayesian Optimization (FlexiBO): An active learning for optimiz-
ing  multiple objectives of different cost
@Version: 0.1
@Author: Shahriar Iqbal
--------------------------------------------------------------------------------
"""
import itertools
import numpy as np
from operator import itemgetter

class Utils(object):
    def __init__(self):
        print ("Initializing Utils Class")
        self.O1_IND=1
        self.O2_IND=0
        

    def create_design_space(self,
                           bounds):
        """@CREATE_DESIGN_SPACE
        ------------------------------------------------------------------------
        This function is used to create discrete design space usign bounds
        @input: bounds
        @output: design space- X
        ------------------------------------------------------------------------
        """
        permutation=list(itertools.product(*bounds))
        return [list(x) for x in permutation], [{"o1":False, "o2":False} for _ in permutation], [{"o1":False, "o2":False} for _ in permutation]
    

    def compute_pareto_volume(self,
                              front):
        """@COMPUTE_PARETO_VOLUME
        ------------------------------------------------------------------------
        This function is used to compute pareto volume between pessimistic and
        optimistic pareto front
        ------------------------------------------------------------------------
        """
        prev_x=0
        prev_y=0
        area=0
        for point in front:
            a=point[self.O1_IND]-prev_x
            b=point[self.O2_IND]-prev_y
            area+=a*b
            prev_x=point[self.O1_IND]
        
        return area
    
    def construct_pessimistic_pareto_front(self,
                               pareto_points_ind,
                               pareto_points,
                               mode):
        """@CONSTRUCT_PESSIMISTIC_PARETO_FRONT
        ------------------------------------------------------------------------
        This function is used to construct pessimistic pareto front using the
        undominated points
        ------------------------------------------------------------------------
        """
        if mode=="CONSTRUCT":
            pess_pareto=list()
            indices_map={}       
            for point in xrange(len(pareto_points)):
                indices_map[point]=pareto_points_ind[point]
                pess_pareto.append(pareto_points[point]["pes"])
        if mode=="UPDATE":
            pess_pareto=pareto_points[:]          
        # sort along object1 in descending order
        sorted_pess_ind=sorted(range(len(pess_pareto)), key=lambda k: pess_pareto[k][self.O1_IND])[::-1]
               
        #-----------------------------------------------------------------------
        # Pessimistic Pareto Front Computation
        #-----------------------------------------------------------------------
        
        pess_o2=[pess_pareto[i][self.O2_IND] for i in sorted_pess_ind]
        i=0
        max_val=[]
        orig=[]
        sampled_pess_pareto_ind=[]
        while i<len(pess_o2): 
            cur=pess_o2[i]
            sampled_pess_pareto_ind.append(i)
            orig.append(i)
    
            for j in xrange(i+1,len(pess_o2)):
                if cur>=pess_o2[j]:
                    sampled_pess_pareto_ind.append(i)
                    max_val.append(j)
                    orig.append(j)
            if len(max_val)!=0:
               i=np.max(max_val)+1
               max_val=[]
            else:
               i=i+1
        sampled_pess_pareto=[[pess_o2[sampled_pess_pareto_ind[i]],pess_pareto[i][self.O1_IND]]for i in xrange(len(orig))]
        if mode=="CONSTRUCT":
            return (sampled_pess_pareto, 
                    indices_map)
        if mode=="UPDATE":
            return sampled_pess_pareto
    
    def construct_optimistic_pareto_front(self,
                                          pareto_points_ind,
                                          pareto_points,
                                          mode):
        """@CONSTRUCT_OPTIMISTIC_PARETO_FRONT
        ------------------------------------------------------------------------
        This function is used to construct optimistic pareto front using the 
        undominated points
        ------------------------------------------------------------------------
        """
        if mode=="CONSTRUCT":                                   
            opt_pareto=list()
            indices_map={}       
            for point in xrange(len(pareto_points)):
                indices_map[point]=pareto_points_ind[point]
                opt_pareto.append(pareto_points[point]["opt"])
        if mode=="UPDATE":
            opt_pareto=pareto_points[:]
        # sort along object1 in descending order
        sorted_opt_ind=sorted(range(len(opt_pareto)), key=lambda k: opt_pareto[k][self.O1_IND])[::-1]
        #-----------------------------------------------------------------------
        # Optimistic Pareto Front Computation
        #-----------------------------------------------------------------------
        # sample optimistic pareto points
        cur=opt_pareto[sorted_opt_ind[0]]
        # initialize 
        sampled_opt_pareto_ind=[sorted_opt_ind[0]]
        sampled_opt_pareto=[cur]
        for ind in xrange(1,len(sorted_opt_ind)):
            next=opt_pareto[sorted_opt_ind[ind]]
            if next[self.O2_IND]>=cur[self.O2_IND]:
                sampled_opt_pareto_ind.append(sorted_opt_ind[ind])
                sampled_opt_pareto.append(next)
            cur= opt_pareto[sorted_opt_ind[ind]]
        
        if mode=="CONSTRUCT":
            return (sampled_opt_pareto,
                    indices_map)
        if mode=="UPDATE":
            return sampled_opt_pareto
                             
    def identify_undominated_points(self,
                             region):
        """@IDENTIFY_UNDOMINATED_POINTS
        ------------------------------------------------------------------------
        This function is used to determine the dominated points that will be
        included in the pessimistic and optimistic pareto front.
        ------------------------------------------------------------------------
        """
        
        dominated_points_ind=list()
        pes_pareto,opt_pareto=list(),list()
        undominated_points_ind=[i for i in xrange(len(region))]
        
        for undom_i in undominated_points_ind:
            # if the current config is not dominated 
            if undom_i!= -1:
                cur= region[undom_i]
                for undom_j in undominated_points_ind :
                    # check only undominated configs other than current
                    if (undom_j!= undom_i or undom_j!=-1):
                        
                       # check if current config is dominated   
                       if (region[undom_j]["pes"][self.O1_IND] >= cur["opt"][self.O1_IND] and
                          region[undom_j]["pes"][self.O2_IND] >= cur["opt"][self.O2_IND]):
                          # append the current config to dominated
                          dominated_points_ind.append(undom_i)
                          undominated_points_ind[undom_i]=-1
          
                       # check if current config dominates
                       if (region[undom_j]["opt"][self.O1_IND] < cur["pes"][self.O1_IND] and
                          region[undom_j]["opt"][self.O2_IND] < cur["pes"][self.O2_IND]):
                          # append the config that is dominated by current to dominated 
                          dominated_points_ind.append(undom_j)
                          undominated_points_ind[undom_j]=-1
        
        # TODO: Dominated points indices multiple occurence issue                 
        undominated_points_ind=[i for i in undominated_points_ind if i not in (-1,-1)]
        undominated_points=[region[i] for i in undominated_points_ind]
        
        return (undominated_points_ind, 
                undominated_points)
           
    def compute_improvement_per_cost(self):
        """@COMPUTE_IMPROVEMENT_PER_COST
        ------------------------------------------------------------------------
        This function is used to compute improvement per cost
        ------------------------------------------------------------------------
        """
        print "Improvement/Cost"
        
        
        
        
        
        
        
        
        
        
        


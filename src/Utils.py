import itertools
import numpy as np
from pareto import sample as region
from operator import itemgetter


class Utils(object):
    def __init__(self):
        print ("Initializing Utils Class")
        self.O1_IND=0
        self.O2_IND=1
    
    def create_design_space(self,
                           bounds):
        """This function is used to create discrete design space usign bounds
        @input: bounds
        @output: design space- X
        """
        permutation=list(itertools.product(*bounds))
        return [list(x) for x in permutation], [{"o1":False, "o2":False} for _ in permutation], [{"o1":False, "o2":False} for _ in permutation]
    

    def compute_pareto_volume():
        """This function is used to compute pareto volume between pessimistic and
        optimistic pareto front
        """
        print "PARETO_VOLUME"
         
    def construct_pareto_front(pareto_points_ind,
                           pareto_points):
        """This function is used to construct the pareto front using pessimistic 
        and optimistic pareto points
        """
        
        pess_pareto=list()
        opt_pareto=list()
        indices_map={}
        # sample pessimistic pareto points that will be used to construct 
        # pessimistic pareto front        
        for point in xrange(len(pareto_points)):
            indices_map[point]=pareto_points_ind[point]
            pess_pareto.append(pareto_points[point]["pes"])
            opt_pareto.append(pareto_points[point]["opt"])
        
        # sort along object1 in descending order
        sorted_pess_ind=sorted(range(len(pess_pareto)), key=lambda k: pess_pareto[k][O1_IND])[::-1]
        sorted_opt_ind=sorted(range(len(opt_pareto)), key=lambda k: opt_pareto[k][O1_IND])[::-1]
        
        #-----------------------------------------------------------------------
        # Pessimistic Pareto Front Computation
        #-----------------------------------------------------------------------
        
        pess_o2=[pess_pareto[i][O2_IND] for i in sorted_pess_ind]
        temp_pess_o2 = [(v,i) for i,v in enumerate(pess_o2)]
        temp_pess_o2.sort()
        sorted_pess_o2, sorted_pess_o2_indices = zip(*temp_pess_o2)
        sorted_pess_o2_indices=list(sorted_pess_o2_indices)

        rank_map_pess_o2=[{} for _ in sorted_pess_o2_indices]   
        for i in xrange(len(sorted_pess_o2_indices)):
            rank_map_pess_o2[sorted_pess_o2_indices[i]]=i

        pess_pareto_ind=[]
        cur_rank=0
        active_rank=-1
        shifted_pess_o2=[]
        for i in xrange(len(rank_map_pess_o2)):
            if rank_map_pess_o2[i]==i:
                pess_pareto.append(i)
                cur_rank=i
            elif rank_map_pess_o2[i]>=cur_rank:
                if active_rank==-1:
                    active_rank=cur_rank
                    if len(shifted_pess_o2)==0:
                        shifted_pess_o2=list(np.arange(cur_rank,rank_map_pess_o2[i]))
                        cur_rank=rank_map_pess_o2[i]
           
            else:
                if len(shifted_pess_o2)!=0: 
                    if rank_map_pess_o2[i] in shifted_pess_o2:
                        shifted_pess_o2.remove(rank_map_pess_o2[i])
                        pess_pareto_ind.append(active_rank)
                if len(shifted_pess_o2)==0:
                  active_rank=-1
       
       
        pess_pareto=[pess_o2[i] for i in pess_pareto_ind]
        
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
            if next[O2_IND]>=cur[O2_IND]:
                sampled_opt_pareto_ind.append(sorted_opt_ind[ind])
                sampled_opt_pareto.append(next)
            cur= opt_pareto[sorted_opt_ind[ind]]
        
        final_opt_ind=[indices_map[i] for i in sampled_opt_pareto_ind]
                    
                      
    def compute_pareto_front(region):
        """This function is used to determine the dominated points that will be
        included in the pessimistic and optimistic pareto front.
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
                       if (region[undom_j]["pes"][O1_IND] >= cur["opt"][O1_IND] and
                          region[undom_j]["pes"][O2_IND] >= cur["opt"][O2_IND]):
                          # append the current config to dominated
                          dominated_points_ind.append(undom_i)
                          undominated_points_ind[undom_i]=-1
          
                       # check if current config dominates
                       if (region[undom_j]["opt"][O1_IND] < cur["pes"][O1_IND] and
                          region[undom_j]["opt"][O2_IND] < cur["pes"][O2_IND]):
                          # append the config that is dominated by current to dominated 
                          dominated_points_ind.append(undom_j)
                          undominated_points_ind[undom_j]=-1
        
        # TODO: Dominated Points Indices Multiple Occurence Issue                 
        undominated_points_ind=[i for i in undominated_points_ind if i not in (-1,-1)]
        undominated_points=[region[i] for i in undominated_points_ind]
        construct_pareto_front(undominated_points_ind,
                               undominated_points)
        return pes_pareto, opt_pareto
        



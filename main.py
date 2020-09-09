####################################################
# Note: This is 3-objective version of NSGA-II
# Last modified: 2018-02-03
# Developers: Jiao Ruwang    ruwangjiao@gmail.com
####################################################

# -*- coding: utf-8 -*-
import DCNSGA_II_DE_tools
import DCNSGA_II_DE_conf
import dynamic_tools
import copy
import os
import nichec
import sys
#import numpy as np
#import matplotlib.pyplot as plt

WORKING_DIR  = os.getcwd()
PROBLEM_DIR = WORKING_DIR + r"/PROBLEM CEC2010"
RESULT_DIR = WORKING_DIR + r"/RESULT"
LOCAL_PATH = [WORKING_DIR, PROBLEM_DIR, RESULT_DIR]
sys.path.extend(LOCAL_PATH)

def init(popSize,  problem_initialize, evaluator):
    global parent_size, offspring_size,  _genCount, _evaluator, parent_pop, upper, lower, constraints_num, objectives_number, evaluationTime
    parent_size, offspring_size, _genCount, _evaluator, upper, lower = popSize, popSize, problem_initialize[0], evaluator, problem_initialize[1], problem_initialize[2]
    constraints_num, objectives_number = problem_initialize[4], problem_initialize[5]
    parent_pop = dynamic_tools.initialize_parent_population(parent_size, _genCount)
    dynamic_tools.caculate_pheno(parent_pop, upper, lower, _genCount, parent_size)
    evaluationTime = 0
    evaluationTime += dynamic_tools.evaluate_population(parent_pop, _evaluator, dynamic_tools.get_fill_result)  

def loop(generation, outputfreq, condition):
    global parent_pop, evaluationTime
    initialMaxViolation = dynamic_tools.caculate_initial_max_violation(parent_pop)
    e = initialMaxViolation
    dynamic_tools.caculate_violation_objective(initialMaxViolation, parent_pop)
    dynamic_tools.mark_individual_efeasible(e, parent_pop)
    K, g = 0, 0
    MaxK = DCNSGA_II_DE_conf.MaxK
    normalized_upper, normalized_lower = [1.0] * _genCount, [0.0] * _genCount
    R = nichec.get_MaxR(_genCount, parent_size + offspring_size, normalized_upper, normalized_lower)    # modify, Setepeter 6,2016, by Zeng Sanyou , Jiao Ruwang
    while K <= MaxK:
        print "Generation:",g," State:",K
        bool_efeasible = dynamic_tools.judge_population_efeasible(parent_pop)
        if bool_efeasible == 1 :
            K += 1
            if K >= MaxK+1:
                break
            e = dynamic_tools.reduce_boundary(initialMaxViolation, K, MaxK)
            r = nichec.reduce_radius(K, MaxK, _genCount, R, upper, lower)
            dynamic_tools.mark_individual_efeasible(e, parent_pop)   
        offspring_pop = dynamic_tools.generate_offspring_population(g, offspring_size, parent_pop, _genCount)
        dynamic_tools.caculate_pheno(offspring_pop, upper, lower, _genCount, offspring_size)
        evaluationTime += dynamic_tools.evaluate_population(offspring_pop, _evaluator, dynamic_tools.get_fill_result)
        dynamic_tools.caculate_violation_objective(initialMaxViolation, offspring_pop)
        dynamic_tools.mark_individual_efeasible(e, offspring_pop)
        nichec.caculate_nichecount(parent_pop, offspring_pop, _genCount, r, parent_size + offspring_size)
        parent_pop = DCNSGA_II_DE_tools.select_next_parent_population(offspring_pop, parent_pop, parent_size)
        
        if g == generation:
            break
        else:
           g += 1

    #nondominated = DCNSGA_II_DE_tools.fast_non_dominated_sort(parent_pop, len(parent_pop))
    #bestObj = copy.deepcopy(nondominated[0][:])
    parent_pop.sort(cmp = compare)
    bestObj = parent_pop[0]
    return bestObj, evaluationTime, g    #return the best individual, the last environment K, the last generation

def compare(a, b):
    if a["violation_objectives"][0] < b["violation_objectives"][0]:
        return -1
    elif a["violation_objectives"][0] > b["violation_objectives"][0]:
        return 1
    else:
        if a["objectives"] < b["objectives"]:
            return -1
        elif a["objectives"] > b["objectives"]:
            return 1
        else:
            return 0
        
def run(problem_initialize, generation, popsize, evaluator, outputfreq = 1, condition = lambda x : False):
    init(popsize, problem_initialize, evaluator)
    return loop(generation, outputfreq, condition)
    
def get_average(res):
    c = sum(res)
    ave = float(c)/len(res)
    return ave

def get_variance(res,ave):
    sumvar = 0.0
    for i in range(len(res)):
        sumvar = sumvar+pow(float(res[i])-ave,2)
    var = pow(sumvar/len(res),0.5)
    return var
       
if __name__ == '__main__':
    import c01,c02,c03,c04,c05,c06,c07,c08,c09,c10,c11,c12,c13,c14,c15,c16,c17,c18
    problemModule = [c06,c08,c10,c15,c11]
    print "================================================================================"
    print "This is dynamic version of NSGA_II:"
    for m in problemModule:
        print "this is", m.__name__, "problem"
        problem_initialize = m.problem_initialize()
        print "D is ", problem_initialize[0]
        t = 25
        res = []
        res1 = []
        res2 = []
        initFile = open(RESULT_DIR+"/"+str(m.__name__) + ".txt", 'w')
        initFile.write("This is dynamic version of NSGA_II:")
        initFile.write('\n')
        initFile.close()
        while t > 0:
            avr = (run(problem_initialize, 10000, 100, m.evaluate ,0))
            res.append(avr[0])
            res1.append(avr[1])
            res2.append(avr[2])
            initFile = open(RESULT_DIR+"/" + str(m.__name__) + ".txt", 'a')
            initFile.write('run is ' + str(t))
            initFile.write('\n')
            initFile.write(str(avr))         
            initFile.write('\n')
            t -= 1
            initFile.close()
        tmp_avr = []
        for i in range(len(res)):
            tmp_avr.append(res[i]["objectives"][0])
        initFile = open(RESULT_DIR+"/" + str(m.__name__) + ".txt", 'a')
        print tmp_avr
        print "tmp_avr ", tmp_avr
        print 'the Max is :', max(tmp_avr)
        print 'the Min is :', min(tmp_avr)
        maxo = max(tmp_avr)
        mino = min(tmp_avr)
        ave = get_average(tmp_avr)
        print 'the average is :', ave
        var = get_variance(tmp_avr, ave)
        print 'the variance is :', var
        initFile.write("Worst:" + str(maxo))
        initFile.write('\n')
        initFile.write("Best: " + str(mino))
        initFile.write('\n')
        initFile.write("Mean: " + str(ave))
        initFile.write('\n')
        initFile.write("Varia:" + str(var))
        initFile.write('\n')
        initFile.write('generation is ' + str(res2))
        initFile.write('\n')
        ave_g = get_average(res2)
        var_g = get_variance(res2,ave_g)
        initFile.write("average generation is " + str(ave_g))
        initFile.write('\n')
        initFile.write("variance generation is " + str(var_g))
        initFile.write('\n')
        initFile.write('the evaTime is ' + str(res1))
        initFile.write('\n')
        ave_evaTime = get_average(res1)
        var_evaTime = get_variance(res1, ave_evaTime)
        initFile.write("the average evaTime is " + str(ave_evaTime))
        initFile.write('\n')
        initFile.write("variance evaTime " + str(var_evaTime))
        initFile.write('\n')
        print "================================================================================"
        initFile.close()

# DCMOEA
A general framework of dynamic constrained multiobjective evolutionary algorithms for constrained optimization
***************************************************************************************************
*
*  This is the DCMOEA in python 2.7 for Windows.
*  This program is coded by the evolutionary computation group in China University of Geosciences.
*  All the problems are in the directory PROBLEM, and the results will be put in the directory RESULT by the program.
*
*  The algorithm starts by  if __name__ == '__main__' in the file main.py:
*  (1) import the problem  you want to solve (i.e., import g02, g03)
*  (2) put the problem in list of module that you want to run (i.e, module = [g02])
*  (3) You can change the total number of independent runs (i.e., t = 25)
*
*  If you want to modify the parameter setting, please open the conf.py, and change
*  (1) the maximum number of generaions (i.e., K=2400) 
*  (2) population size (i.e., popsize=100)
*
***************************************************************************************************
# Acknowledge
Please kindly cite this paper in your publications if it helps your research:
```
@article{zeng2017general,
  title={A general framework of dynamic constrained multiobjective evolutionary algorithms for constrained optimization},
  author={Zeng, Sanyou and Jiao, Ruwang and Li, Changhe and Li, Xi and Alkasassbeh, Jawdat S},
  journal={IEEE transactions on Cybernetics},
  volume={47},
  number={9},
  pages={2678--2688},
  year={2017},
  publisher={IEEE}
}
```

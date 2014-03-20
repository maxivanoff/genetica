import Individual
var_ranges = {'X':[-1,1],'Y':[-1,1]}
individ1 = Individual.RealCoded(var_ranges)
individ1.objectives['obj1']=0.1
individ1.objectives['obj2']=0.2

individ2 = Individual.RealCoded(var_ranges)
individ2.objectives['obj1']=0.11
individ2.objectives['obj2']=0.19

print individ1.dominate(individ2)

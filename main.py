############################################################################################
#creator:李寅龙
#time:2020.10.21
#E-mail:3078017732@qq.com
#以下是问题解决的主函数，分别使用三种方法：宽度优先算法，深度优先算法，启发式算法，解决了3个传教士，3个野人，负载2人；
#6个传教士，6个野人，负载5人；10个传教士，10个野人，负载5人的情况。野人与传教士人数不相等的情况还有bug，有待后续调试。
#状态的三个参数分别表示此岸的传教士人数，此岸的野人人数，船的状态，1表示船在对岸，0表示船在此岸
############################################################################################


from MyModule import StateSpace,GraphSearch
#######################################################
#3个传教士，3个野人，负载为2的情况
model1 =StateSpace(3,3,2)
states,operations = model1.fit()#得到此问题状态空间的所有合理状态与算符
init_state=[3,3,0]#初始状态此岸3个传教士，3个野人，船在此岸
final_state=[0,0,1]#目的状态此岸0个传教士，0个野人，船在对岸
GraphSearchModel1=GraphSearch(init_state=init_state,final_state=final_state,set_of_operation=operations,
                              set_of_state=states)
print("使用启发式算法:","\n")
GraphSearchModel1.search(method="heuristic")#使用启发式算法
print("使用宽度优先算法:","\n")
GraphSearchModel1.search(method="breadth")#使用宽度优先算法
print("使用深度优先算法:","\n")
GraphSearchModel1.search(method="depth")#使用深度算法
#######################################################
#6个传教士，6个野人，负载为5的情况
model2 =StateSpace(6,6,5)
states,operations = model2.fit()#得到此问题状态空间的所有合理状态与算符
init_state=[6,6,0]#初始状态此岸6个传教士，6个野人，船在此岸
final_state=[0,0,1]#目的状态此岸0个传教士，0个野人，船在对岸
GraphSearchModel2=GraphSearch(init_state=init_state,final_state=final_state,set_of_operation=operations,
                              set_of_state=states)
print("使用启发式算法:","\n")
GraphSearchModel2.search(method="heuristic")#使用启发式算法
print("使用宽度优先算法:","\n")
GraphSearchModel2.set_depth_limit(30)#设置搜索深度30
GraphSearchModel2.search(method="breadth")#使用宽度优先算法
print("使用深度优先算法:","\n")
GraphSearchModel2.search(method="depth")#使用深度算法

############################################################
#10个传教士，10个野人，负载为5的情况
model3 =StateSpace(10,10,5)
states,operations = model3.fit()#得到此问题状态空间的所有合理状态与算符
init_state=[10,10,0]#初始状态此岸10个传教士，10个野人，船在此岸
final_state=[0,0,1]#目的状态此岸0个传教士，0个野人，船在对岸
GraphSearchModel3=GraphSearch(init_state=init_state,final_state=final_state,set_of_operation=operations,
                              set_of_state=states)
print("使用启发式算法:","\n")
GraphSearchModel3.search(method="heuristic")#使用启发式算法
print("使用宽度优先算法:","\n")
GraphSearchModel3.set_depth_limit(30)#设置搜索深度30
GraphSearchModel3.search(method="breadth")#使用宽度优先算法
print("使用深度优先算法:","\n")
GraphSearchModel3.search(method="depth")#使用深度算法

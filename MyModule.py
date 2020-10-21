#############################################################################################
#creator：李寅龙
#time：2020.10.21
#E-mail：3078017732@qq.com
#以下包含了提取状态空间的类StateSpace，和进行图搜索的GraphSearch
############################################################################################


#计算状态转移，用于图中结点的展开
def state_transition(current_state, set_of_operation, set_of_state):
    if current_state not in set_of_state:
        print("Error!Unreasonable state!")
        return None
    next_states = []
    for move in set_of_operation:

        missionaries = current_state[0]
        cannibals = current_state[1]
        this_side = (current_state[-1] == 0)
        if this_side:
            next_state = [missionaries - move[0], cannibals - move[1], 1]
        else:
            next_state = [missionaries + move[0], cannibals + move[1], 0]
        if next_state in set_of_state:
            next_states.append(next_state)
    if next_states == []:
        return None
    return next_states


#将找到的路径打印出来
def print_the_road(relation,final_state,init_state):
    road=[final_state]
    current_state=final_state
    nodes=list(relation.keys())
    while True:
        if current_state==init_state:
            break
        if str(current_state) not in nodes:
            print("rode printing failed!",nodes,current_state)
            return None
        parent_node=relation[str(current_state)]
        road.append(parent_node)
        current_state=parent_node
    road.reverse()
    for node in road:
        print("--->",node,"\n")
    return road

#深度优先算法中用于计算该节点所在深度
def get_depth(init_state,current_state,relation):
    road=[]
    while True:
        if current_state==init_state:
            break
        parent_node=relation[str(current_state)]
        road.append(parent_node)
        current_state=parent_node
    return len(road)

#启发式算法中用于重排open表
def rank_open_table(open_table):
    ranked_table=sorted(open_table,key=lambda x:x[0]+x[1])
    return ranked_table

#状态空间相关的类
class StateSpace:

    def __init__(self, missionaries, cannibals, capacity):
        self.missionaries = missionaries
        self.cannibals = cannibals
        self.capacity = capacity

    #用于找出所有合理的状态
    def set_of_state(self):
        states = []
        for i in range(self.missionaries + 1):
            for j in range(self.cannibals + 1):
                missionaries_other_side, cannibals_other_side = self.missionaries - i, self.cannibals - j
                if i == self.missionaries and j == self.cannibals:
                    state = [i, j, 0]
                    states.append(state)
                    continue
                if i == 0 and j == 0:
                    state = [i, j, 1]
                    states.append(state)
                    continue
                if (i == 0 and missionaries_other_side >= cannibals_other_side) or \
                        (i >= j and missionaries_other_side >= cannibals_other_side) or \
                        (i == self.missionaries and i >= j):
                    state1 = [i, j, 0]
                    state2 = [i, j, 1]
                    states.append(state1)
                    states.append(state2)
        self.states = states

    #用于找出所有合理的算符
    def set_of_operation(self):
        operations = []
        for i in range(self.capacity + 1):
            max_cannibal = self.capacity - i
            if i == 0:
                for cannibal in range(self.capacity):
                    operations.append([0, cannibal + 1])
            else:
                for cannibal in range(i + 1):
                    if cannibal <= max_cannibal:
                        operations.append([i, cannibal])
                        continue
                    else:
                        break
        self.operations = operations

    def fit(self):
        self.set_of_operation()
        self.set_of_state()
        return self.states, self.operations



#与图搜索算法相关的类
class GraphSearch:

    def __init__(self, init_state, final_state, set_of_operation, set_of_state):
        self.init_state = init_state
        self.final_state = final_state
        self.set_of_operation = set_of_operation
        self.set_of_state = set_of_state
        self.limit_depth = 25

    #宽度优先算法
    def breadth_first_search(self):
        open_table = [self.init_state]
        closed_table = []
        relation = {}
        flag = 0
        road = []
        while True:
            if open_table == []:
                print("Error!The open table is empty.Breadth first search failed!")
                return None
            current_state = open_table[0]
            next_state = state_transition(current_state, self.set_of_operation, self.set_of_state)
            open_table.remove(current_state)
            closed_table.append(current_state)
            if next_state == None:
                continue
            for child in next_state:
                if child not in closed_table:
                    relation[str(child)] = current_state
                    open_table.append(child)
                    if child == self.final_state:
                        road = print_the_road(relation, child, self.init_state)
                        flag = 1
                        break
            if flag == 1:
                break
        self.road = road

    #深度优先算法
    def depth_first_search(self):
        open_table = [self.init_state]
        closed_table = []
        relation = {}
        flag = 0
        road = []
        while True:
            if open_table == []:
                print("Error!The open table is empty.Depth first search failed!")
                return None
            current_state = open_table[0]
            next_state = state_transition(current_state, self.set_of_operation, self.set_of_state)
            open_table.remove(current_state)
            closed_table.append(current_state)
            if next_state == None:
                continue
            for child in next_state:
                if child not in closed_table:
                    relation[str(child)] = current_state
                    depth = get_depth(self.init_state, current_state, relation)
                    if depth > self.limit_depth:
                        break
                    open_table.insert(0, child)
                    if child == self.final_state:
                        road = print_the_road(relation, child, self.init_state)
                        flag = 1
                        break
            if flag == 1:
                break
        self.road = road

    #启发式算法，启发函数为还没有过岸的总人数
    def heuristic_search(self):
        open_table = [self.init_state]
        closed_table = []
        relation = {}
        flag = 0
        road = []
        while True:
            if open_table == []:
                print("Error!The open table is empty.Heuristic search failed!")
                return None
            open_table_ranked = rank_open_table(open_table)
            current_state = open_table_ranked[0]
            next_state = state_transition(current_state, self.set_of_operation, self.set_of_state)
            open_table.remove(current_state)
            closed_table.append(current_state)
            if next_state == None:
                continue
            for child in next_state:
                if child not in closed_table:
                    relation[str(child)] = current_state
                    open_table.append(child)
                    if child == self.final_state:
                        road = print_the_road(relation, child, self.init_state)
                        flag = 1
                        break
            if flag == 1:
                break
        self.road = road

    #搜索，任选一种方法搜索
    def search(self, method="breadth"):
        if method == "breadth":
            self.breadth_first_search()
        if method == "depth":
            self.depth_first_search()
        if method == "heuristic":
            self.heuristic_search()
        print("The length of road is:",len(self.road),"\n")

    #设置深度优先算法中的极限深度，默认值为25层
    def set_depth_limit(self,depth_limit):
        self.limit_depth = depth_limit
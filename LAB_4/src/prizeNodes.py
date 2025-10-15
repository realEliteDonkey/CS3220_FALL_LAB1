import random as rand


class P_Node:
    def __init__(self, node_str):
        self.node_id = node_str
        self.prize = None
        
    def __repr__(self):
        return f"ID: {self.node_id}, Prize: {self.prize}"


class P_PrizeNodes:
    nodes_w_prize = []
    prizes = ["Gold", "Diamond", "PizzaFlyer", "ExamPoints"]
    
    @classmethod
    def generate_prizes(cls, node_list):
        cls.nodes_w_prize.clear()
        # use .replace() to reassign key to graph
        # push (["N__"]["prize"])
        for i in range(0,4):
            rand_node = rand.randint(2, 31)
            prize_node = node_list[rand_node]
            prize_node.prize = cls.prizes[i]
            cls.nodes_w_prize.append(prize_node)
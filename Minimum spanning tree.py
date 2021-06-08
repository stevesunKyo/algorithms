# 单向图和双向图的数组表示
# 用Plim和Kuskar算法来解最小生成树问题
# created by Sun Anyang on 2021.06.08
import networkx as nx  # 用来画计算好的最小生成树图形的module
import matplotlib.pyplot as plt
from math import sin, cos


class graph(object):

    def __init__(self, nums, g_type):
        self.point_numbers = nums
        self.points = list(range(0, nums))
        self.graphs = [[10000] * nums for row in range(nums)]
        self.links = [[10000] * nums for row in range(nums)]
        self.work = False  # 是否已经完成最小生成树的查找
        if g_type == "directed":
            self.graph_type = "directed"
        elif g_type == "undirected":
            self.graph_type = "undirected"
        else:
            raise ValueError("Graph Type Error")

    def input_link(self, a, b, value=1):
        """
        联通图的第a个点和第b个点。这里在输入图坐标的时候采用 0-index
        value 为第a个点和第b个点之间路径的权重，默认为1,即所有图的权重完全一样。
        """
        if self.graph_type == "directed":
            # 单向图进行连接的时候只是单项连接。连接方法是将graphs[a][b]设置为Value
            # 即：index为[a]和[b]的两个点之间有一条权重为Value的线相连。
            self.graphs[a][b] = value
        elif self.graph_type == "undirected":
            # 无向图(两个方向进行连接的图)是双向连接，所以设置方法应该是将graphs[a][b]和graphs[b][a]都设置为Value
            self.graphs[a][b] = value
            self.graphs[b][a] = value

    def find_linked_point(self, point):
        # find linked point and weights of a point
        # variant Point is index of a point
        point_index = []
        point_value = []
        for i in range(0, self.point_numbers):
            if point_value != 10000:
                point_value.append(self.graphs[point][i])
                point_index.append([point,i])
        return point_index, point_value

    def calculate_coord_points_circle(self):
        # in order to place those points in a circle, the coordinate of points should be calculated.
        # 用极坐标，x = rcost, y = rsint
        # t = [0, 2pi] r = 3
        t = [x / self.point_numbers * 3.14159 for x in list(range(0, self.point_numbers))]
        res = []
        di = {}
        for i in range(0, self.point_numbers):
            res.append([3 * cos(t[i]), 3*sin(t[i])])
            di[i] = res[i]
        return di

    def prim(self, start_point=0):
        # prim算法求最小生成树
        # 从index为start_point的点开始进行计算。默认为从第一个点开始。
        """
        Prim算法原理：
        1）以某一个点开始，寻找当前该点可以访问的所有的边；
        2）在已经寻找的边中发现最小边，这个边必须有一个点还没有访问过，将还没有访问的点加入我们的集合，记录添加的边；
        3）寻找当前集合可以访问的所有边，重复2的过程，直到没有新的点可以加入；
        4）此时由所有边构成的树即为最小生成树。
        """
        Not_linked = list(range(0, self.point_numbers))
        Not_linked.remove(start_point)
        linked = [start_point]
        # 节点分为两种，一种是已经连接的 一种是没有连接的
        while True:
            linked_value_all = []
            linked_index_all = []
            for i in linked:
                linked_index, linked_value = self.find_linked_point(i)
                linked_index_all += linked_index
                linked_value_all += linked_value
            # 首先建立记录着所有目前能够通过一步连接连起来的数组linked_index_all
            # 还有记录着所有linked_index_all数组里面连接的权重的数组linked_value_all
            zuixiao = 10000
            zuixiao_ind = 0
            for i in range(0, len(linked_value_all)):
                if linked_value_all[i] <= zuixiao and linked_index_all[i][1] in Not_linked:
                    zuixiao = linked_value_all[i]
                    zuixiao_ind = i
            zuixiao_ind = linked_index_all[zuixiao_ind]
            # 找出目前的所有可用链接中权重最小的而且有效(至少有一段连接的是未连接的点)的链接
            # 此时zuixiao_index代表着所有可连接的链接中value最小的那一条, 格式为[起始点, 终止点]
            self.links[zuixiao_ind[0]][zuixiao_ind[1]] = 1
            Not_linked.remove(zuixiao_ind[1])
            linked.append(zuixiao_ind[1])
            if len(Not_linked) != 0:
                pass
            else:
                print("已经找到最小生成树")
                self.work = True
                break

    def print_tree(self):
        # 下一步的工作：固定pos的位置，同时将图加上label
        nodes = list(range(0, self.point_numbers))
        image = nx.Graph()
        coord = self.calculate_coord_points_circle()
        for node in nodes:
            image.add_node(node)
        for i in range(0, self.point_numbers):
            for j in range(i, self.point_numbers):
                if self.graphs[i][j] != 10000:
                    image.add_edge(nodes[i], nodes[j], weight=self.graphs[i][j])
        edge_labels = nx.get_edge_attributes(image, 'weight')
        nx.draw_networkx_edge_labels(image, coord, edge_labels=edge_labels)
        nx.draw(image, pos=coord, with_labels=True, node_color='y')
        plt.show()

    def print_link(self):
        if self.work:
            nodes = list(range(0, self.point_numbers))
            image = nx.Graph()
            coord = self.calculate_coord_points_circle()
            for node in nodes:
                image.add_node(node)
            for i in range(0, self.point_numbers):
                for j in range(0, self.point_numbers):
                    if self.links[i][j] != 10000:
                        image.add_edge(nodes[i], nodes[j], weight=self.graphs[i][j])
            edge_labels = nx.get_edge_attributes(image, 'weight')
            nx.draw_networkx_edge_labels(image, coord, edge_labels=edge_labels)
            nx.draw(image, pos=coord, with_labels=True, node_color='y', )
            plt.show()
        else:
            print("最小生成树查找未完成")


if __name__ == '__main__':
    # 计算例， 一个总共五个点的双向图
    new_graph = graph(5, "undirected")
    new_graph.input_link(0, 1, 3)
    new_graph.input_link(0, 2, 1)
    new_graph.input_link(0, 4, 2)
    new_graph.input_link(1, 4, 2)
    new_graph.input_link(1, 3, 4)
    new_graph.input_link(3, 4, 5)
    new_graph.input_link(2, 3, 6)
    new_graph.prim(0)
    new_graph.print_tree()
    new_graph.print_link()


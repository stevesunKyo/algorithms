# 单向图和双向图的数组表示
# 用Plim和Kuskar算法来解最小生成树问题
# created by Sun Anyang on 2021.06.08
import networkx as nx  # 用来画计算好的最小生成树图形的module
import matplotlib.pyplot as plt
from math import sin, cos


class mst(object):

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

    def graph_copy(self, variant):
        self.graphs = variant.graphs

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

    def kruskal(self):
        """
        kruskal 算法求最小生成树
        kruskal 算法的操作步骤：
        1. 先对所有的边进行排序，选择权重最短的一条边开始
        2. 按照权重的从小到大的顺序追加边，如果通过增加某条边会使得有新的点被连接到这条生成树上，追加它
        2.5 如果追加某条边并不会使得有新的点被连接到生成树上，不管它
        3. 持续追加所有边，直到所有的点都被连接到生成树上
        """
        # 对所有的权重进行排序，并同时记录每一个点(link)对应的权重
        # 首先读取矩阵中所有的已经联通的点
        link_list = []
        linked_point = []
        for i in range(0, self.point_numbers):
            for j in range(i, self.point_numbers):
                if self.graphs[i][j] != 10000:
                    link_list.append([[i, j], self.graphs[i][j]])
        # 其次对于这些点进行sort
        for i in range(1, len(link_list)):
            for j in range(0, len(link_list) - i):
                if link_list[j][1] > link_list[j+1][1]:
                    link_list[j], link_list[j+1] = link_list[j+1], link_list[j]
        # sort之后，linked_list里面记录的就都是权重从小到大排好序的了
        for i in range(0, len(link_list)):
            if link_list[i][0][0] not in linked_point or link_list[i][0][1] not in linked_point:
                self.links[link_list[i][0][0]][link_list[i][0][1]] = 1
                linked_point.append(link_list[i][0][0])
                linked_point.append(link_list[i][0][1])
        print("已经找到最小生成树")
        self.work = True

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


class spt(object):
    """
    求解最短路径树问题。使用dijkstra算法
    算法所需记录表：
    一个3*n数组，n为总共的点数
    第一列记录目前的index对应的点到出发点的距离
    第二列记录目前的index对应的点在生成树上对应的点
    第三列记录True or False，如果已经为【最短路径】，则记为True，否则默认为False
    """
    # 目前我写的的dijkstra算法存在无限递归的问题
    # 2021.6.9 明天需要修正
    def __init__(self, nums):
        self.point_numbers = nums
        self.points = list(range(0, nums))
        self.graphs = [[10000] * nums for row in range(nums)]
        self.link = [[10000] * nums for row in range(nums)]
        self.judge = [[10000] * 3 for row in range(nums)]
        self.work = False  # 是否已经完成最小生成树的查找

    def graph_copy(self, variant):
        # 这个函数用来从mst（最小生成树）的variant来copy内部的图的结构
        self.graphs = variant.graphs

    def input_link(self, a, b, value=1):
        """
        联通图的第a个点和第b个点。这里在输入图坐标的时候采用 0-index
        value 为第a个点和第b个点之间路径的权重，默认为1,即所有图的权重完全一样。
        """
        self.graphs[a][b] = value
        self.graphs[b][a] = value

    def find_linked_point(self, index):
        # find linked point of point "index", linked point should not be a point that
        linked_points = []
        for i in range(0, self.point_numbers):
            if self.graphs[index][i] != 10000:
                linked_points.append([[index, i], self.graphs[index][i]])
        return linked_points

    def dij(self, start_point):
        """
        1. 从任意一个点P开始，寻找这个点能够到达的所有点(P1,P2...Pn) P1~Pn的点所对应的权重分别为X1~Xn
        2. 将P1~Pn所对应的权重X1~Xn输入记录表.选择其中权重最小的一个(假设为Xp)，将第三列设置为0(True)
        3. 从选出来的权重最小点开始，重复1，此时各点Q1~Qm权重为Y1~Ym
        4. 如果有重复(即Qm和Pm是同一个点)的情况下，比较通过第2步的P路径进行连接的权重Xm
        和通过第3步的Q路径进行连接的权重Xp+Qm的大小，选择其中比较小的
        """
        self.judge[start_point][2] = 0
        # linked_points = [[10000]*self.point_numbers]
        linked_points = self.find_linked_point(start_point)
        zuixiao = 10000  # 用来找linked_points里面最小值的变量
        ind_i = 0
        for i in range(0, len(linked_points)):
            # 寻找权重最小的变量对应的值
            if linked_points[i][1] <= zuixiao and self.judge[i][2] != 0:
                zuixiao = linked_points[i][1]
                ind_i = i
            # 将所有的权重值和现有的self.judge中的权重值进行比较，如果权重值比其要小，更新self.judge中的权重值
            if linked_points[i][1] <= self.judge[linked_points[i][0][1]][0]:
                self.judge[linked_points[i][0][1]][0] = linked_points[i][1]
        # 把"ind_i"对应的self.judge的第三列设置为0
        self.judge[ind_i][2] = 0
        self.link[start_point][ind_i] = 1

        # 判断self.judge的第3列是否全为0(表示找到全部的最短连接)的
        flag = True
        for i in range(0, self.point_numbers):
            if self.judge[i][2] != 0:
                flag = False
                break

        if flag == True:
            print("已经找到最短路径树")
        else:
            return self.dij(linked_points[ind_i][0][1])  # 从linked_points[ind_i][0][1]开始递归

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
            print("最短路径树查找未完成")



if __name__ == '__main__':
    # 计算例， 一个总共五个点的双向图
    new_graph = spt(5)
    new_graph.input_link(0, 1, 3)
    new_graph.input_link(0, 2, 1)
    new_graph.input_link(0, 4, 2)
    new_graph.input_link(1, 4, 2)
    new_graph.input_link(1, 3, 4)
    new_graph.input_link(3, 4, 5)
    new_graph.input_link(2, 3, 6)
    # new_graph.prim(0)
    # new_graph.kruskal()
    new_graph.dij(0)
    new_graph.print_tree()
    new_graph.print_link()


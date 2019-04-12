import numpy as np

number_of_time_periods = 4
number_of_generating_units = 3
number_of_nodes = 3
number_of_lines = 3

generating_units_cost = np.array([100, 200, 300])
demand = np.array([[40, 40, 30, 40],
                   [200, 200, 200, 150],
                   [300, 100, 150, 200]])
lower_bound_power = np.array([20, 20, 20])
upper_bound_power = np.array([400, 400, 400])

maximum_flow = np.array([[200, 200, 200, 200],
                         [200, 200, 200, 200],
                         [200, 200, 200, 200]])
lower_bound_ramping = np.array([0, 0, 0])
upper_bound_ramping = np.array([160, 160, 160])

origin_node_line_relationship = np.array([[1, 0, 1],
                                         [0, 1, 0],
                                         [0, 0, 0]])

end_node_line_relationship = np.array([[0, 0, 0],
                                      [1, 0, 0],
                                      [0, 1, 1]])



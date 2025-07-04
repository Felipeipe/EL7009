import numpy as np

from pure_pursuit_planner import DifferentialRobot
from pure_pursuit_planner import PurePursuitPlanner
from rrt_planner import RRTPlanner

# For RRT and integration tests
def add_map_obstacles_1(input_map):
    # DO NOT MODIFY
    assert input_map.shape == (64, 64)
    input_map[20:22, 10:50] = 1
    input_map[22:42, 48:50] = 1
    input_map[40:42, 10:50] = 1

def add_map_obstacles_2(input_map):
    # DO NOT MODIFY
    assert input_map.shape == (64, 64)
    input_map[10:12, 14:50] = 1
    input_map[20:22, 14:50] = 1
    input_map[40:42, 14:50] = 1
    input_map[50:52, 14:50] = 1
    input_map[5:59 ,  7:9 ] = 1
    input_map[5:59 , 55:57] = 1


def add_map_obstacles_3(input_map):
    # DO NOT MODIFY
    assert input_map.shape == (64, 64)
    input_map[10:12, 0:60] = 1
    input_map[20:22, 5:64] = 1
    input_map[30:32, 0:60] = 1
    input_map[40:42, 5:64] = 1
    input_map[50:52, 0:60] = 1


def rrt_exps():

    max_attempts = 1

    input_map = np.zeros((64, 64))
    add_map_obstacles_3(input_map)

    rrt_planner = RRTPlanner(input_map,
                             init_position=[2, 60],
                             target_position=[2, 2],
                             nb_iterations=20000,
                             traverse_distance=2.0)
    plan = rrt_planner.generate_rrt()

    if plan is None:
        counter = 1
        while plan is None:
            rrt_planner.set_random_seed(counter)
            plan = rrt_planner.generate_rrt()
            counter+=1
            if counter > max_attempts:
                break

    rrt_planner.plot_rrt()


def pure_pursuit_exps():

    input_map = np.zeros((64, 64))

    # Parametric plan generation (do not modify the plan)
    time = np.linspace(-np.pi, np.pi, 200)

    x_position_plan = np.sin(time)**3
    y_position_plan = (13 * np.cos(time) - (5 * np.cos(2 * time)) - \
                      ( 2 * np.cos(3 * time)) - (np.cos(4 * time))) / 16.

    y_position_plan -= min(y_position_plan) + 1.0

    plan = np.zeros((len(time), 2))
    plan[:, 0] = x_position_plan
    plan[:, 1] = y_position_plan

    # Plan scaling
    plan = plan * 30 + 32

    diff_robot = DifferentialRobot(local_planner=PurePursuitPlanner())
    diff_robot.set_map(input_map)

    # TODO: modify the following line to change initial pose
    diff_robot.set_pose([20, 30])

    diff_robot._local_planner.set_plan(plan)

    diff_robot.visualize()


def integration_exps():

    input_map = np.zeros((64, 64))
    add_map_obstacles_1(input_map)

    diff_robot = DifferentialRobot(local_planner=PurePursuitPlanner())
    rrt_planner = RRTPlanner(input_map)
    diff_robot.set_map(input_map)

    diff_robot.set_pose([32, 32])
    rrt_planner.set_init_position([32, 32])
    rrt_planner.set_target_position([55, 32])

    plan = rrt_planner.generate_rrt()

    max_attemts = 10
    if plan is None:
        counter = 1
        while plan is None:
            rrt_planner.set_random_seed(counter)
            plan = rrt_planner.generate_rrt()
            counter+=1
            if counter > max_attemts:
                break

    diff_robot._local_planner.set_plan(plan)

    rrt_planner.plot_rrt()
    diff_robot.visualize()


if __name__ == '__main__':

    # rrt_exps()
    pure_pursuit_exps()
    # integration_exps()

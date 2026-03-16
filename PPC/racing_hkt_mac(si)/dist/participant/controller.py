
'''
PPC Hackathon — Participant Boilerplate
You must implement two functions: plan() and control()
'''

# ─── TYPES (for reference) ────────────────────────────────────────────────────

# Path: list of waypoints [{"x": float, "y": float}, ...]
# State: {"x", "y", "yaw", "vx", "vy", "yaw_rate"} 
# CmdFeedback: {"throttle", "steer"}         

# ─── CONTROLLER ───────────────────────────────────────────────────────────────
import numpy as np


def steering(path: list[dict], state: dict):
    L = 2.6 
    curr_x, curr_y = state['x'], state['y']
    curr_yaw = state['yaw'] 
    

    dists = [np.hypot(p['x'] - curr_x, p['y'] - curr_y) for p in path]
    closest_idx = np.argmin(dists)
    

    speed = np.hypot(state['vx'], state['vy'])
    look_ahead = np.clip(3.0 + 0.4 * speed, 4.0, 12.0)
    
    target_idx = closest_idx
    for i in range(closest_idx, len(path)):
        if dists[i] > look_ahead:
            target_idx = i
            break
    target_p = path[target_idx]

    p_near = path[closest_idx]
    p_next = path[min(closest_idx + 1, len(path)-1)]
    

    path_dx = p_next['x'] - p_near['x']
    path_dy = p_next['y'] - p_near['y']
    
    car_dx = curr_x - p_near['x']
    car_dy = curr_y - p_near['y']

    mag = np.hypot(path_dx, path_dy) + 1e-6
    cte = (car_dy * path_dx - car_dx * path_dy) / mag

    dx = target_p['x'] - curr_x
    dy = target_p['y'] - curr_y
    target_angle = np.arctan2(dy, dx)
    
    alpha = target_angle - curr_yaw
    alpha = (alpha + np.pi) % (2 * np.pi) - np.pi 

    steer = np.arctan2(2.0 * L * np.sin(alpha), look_ahead)
    

    cte_gain = 0.3
    steer -= (cte * cte_gain)
    prev_steer = state.get('prev_steer', 0.0)

    steer = 0.3 * prev_steer + 0.7 * steer 
    state['prev_steer'] = steer
    return np.clip(steer, -0.5, 0.5)

def throttle_algorithm(target_speed, current_speed, dt):
    kp=1.0

    error=target_speed-current_speed
    if error > 0:
        throttle = error * kp
        brake = 0.0
    else:
        throttle = 0.0
        brake = abs(error) * 0.5


    
    

    return np.clip(throttle, 0.0, 1.0), np.clip(brake, 0.0, 1.0)

def control(
    path: list[dict],
    state: dict,
    cmd_feedback: dict,
    step: int,
) -> tuple[float, float, float]:
    """
    Generate throttle, steer, brake for the current timestep.
    Called every 50ms during simulation.

    Args:
        path:         Your planned path (waypoints)
        state:        Noisy vehicle state observation
                        x, y        : position (m)
                        yaw         : heading (rad)
                        vx, vy      : velocity in body frame (m/s)
                        yaw_rate    : (rad/s)
        cmd_feedback: Last applied command with noise
                        throttle, steer, brake
        step:         Current simulation timestep index

    Returns:
        throttle  : float in [0.0, 1.0]   — 0=none, 1=full
        steer     : float in [-0.5, 0.5]  — rad, neg=left
        brake     : float in [0.0, 1.0]   — 0=none, 1=full
    
    Note: throttle and brake cannot both be > 0 simultaneously.
    """
    throttle = 0.0
    steer    = 0.0
    brake = 0.0
   
    # TODO: implement your controller here
    steer = steering(path, state)
    target_speed = 9 # m/s, adjust as needed
    global integral
    throttle, brake = throttle_algorithm(target_speed, state["vx"], 0.05)

    return throttle, steer, brake

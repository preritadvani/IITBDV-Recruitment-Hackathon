
'''
PPC Hackathon — Participant Boilerplate
You must implement two functions: plan() and control()
'''

# ─── TYPES (for reference) ────────────────────────────────────────────────────

# Cone: {"x": float, "y": float, "side": "left" | "right", "index": int}
# State: {"x", "y", "yaw", "vx", "vy", "yaw_rate"}  
# CmdFeedback: {"throttle", "steer"}        

# ─── PLANNER ──────────────────────────────────────────────────────────────────
import numpy as np
import numpy as np


def laplacian_smooth(path, beta=0.15, iterations=5):

    if len(path) < 3:
        return path

    new_path = path.copy()

    for _ in range(iterations):

        temp = new_path.copy()

        for i in range(1, len(path)-1):

            x_prev = temp[i-1]["x"]
            x_curr = temp[i]["x"]
            x_next = temp[i+1]["x"]

            y_prev = temp[i-1]["y"]
            y_curr = temp[i]["y"]
            y_next = temp[i+1]["y"]

            sx = x_curr + beta * (x_prev + x_next - 2*x_curr)
            sy = y_curr + beta * (y_prev + y_next - 2*y_curr)


            new_x = 0.8 * x_curr + 0.2 * sx
            new_y = 0.8 * y_curr + 0.2 * sy

            new_path[i] = {"x": new_x, "y": new_y}

    return new_path
def plan(cones: list[dict]) -> list[dict]:
    """
    Generate a path from the cone layout.
    Called ONCE before the simulation starts.

    Args:
        cones: List of cone dicts with keys x, y, side ("left"/"right"), index

    Returns:
        path: List of waypoints [{"x": float, "y": float}, ...]
              Ordered from start to finish.
    
    Tip: Try midline interpolation between matched left/right cones.
         You can also compute a curvature-optimised racing line.
    """
    path = []
    # TODO: implement your path planning here
    blue = np.array([[cone["x"], cone["y"]] for cone in cones if cone["side"] == "left"])
    yellow = np.array([[cone["x"], cone["y"]] for cone in cones if cone["side"] == "right"])
    midline=[]
    # implement a planning algorithm to generate a path from the blue and yellow cones
    n=min(len(blue), len(yellow))
    for i in range(n):

            mid_x = (blue[i][0] + yellow[i][0]) / 2
            mid_y = (blue[i][1] + yellow[i][1]) / 2

            midline.append({"x": float(mid_x), "y": float(mid_y)})
    midline=laplacian_smooth(midline,0.2,10)
    k=5
    last_part = midline[-k:]
    last_part = laplacian_smooth(last_part, 0.5, 10)

    midline[-k:] = last_part

    return midline

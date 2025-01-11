import json
import os
from datetime import datetime

TARGET_FOLDER = os.path.dirname(os.path.abspath(__file__))
GOAL_FILE = os.path.join(TARGET_FOLDER, "reading_goals.json")

TIME_FILE = os.path.join(TARGET_FOLDER, "reading_times.json")

def validate_time_input(value):
    if not value.isdigit() or int(value) <= 0:
        raise ValueError("Please enter a positive integer value.")
    return int(value)

def update_goal(goal_type, frequency, value):
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    goal_data = {
        "goal_type": goal_type,
        "frequency": frequency,
        "value": value,
        "created_at": current_date
    }

    with open(GOAL_FILE, "w") as file:
        json.dump([goal_data], file, indent=4)

    return f"Goal updated: {goal_type} ({frequency}) - {value}"

def get_current_goal():
    if os.path.exists(GOAL_FILE):
        with open(GOAL_FILE, "r") as file:
            data = json.load(file)
            if data:
                return data[0] 
    return None

def save_reading_start():
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(TIME_FILE, "w") as file:
        json.dump({"start_time": start_time}, file)


def save_reading_end():
    if not os.path.exists(TIME_FILE):
        return None

    end_time = datetime.now()
    with open(TIME_FILE, "r") as file:
        data = json.load(file)
        start_time = datetime.strptime(data["start_time"], "%Y-%m-%d %H:%M:%S")
        duration = (end_time - start_time).total_seconds() // 60 
    
    os.remove(TIME_FILE)

    return int(duration)

def update_goal_time_spent(minutes_spent):
    goal = get_current_goal()
    if not goal or goal["goal_type"] != "time":
        return None

    goal["value"] = max(0, goal["value"] - minutes_spent)  
    with open(GOAL_FILE, "w") as file:
        json.dump([goal], file, indent=4)

    return goal["value"]

def update_goal_pages_spent(pages_spent):
    goal = get_current_goal()
    if not goal or goal["goal_type"] == "time":
        return None

    goal["value"] = max(0, goal["value"] - pages_spent)  
    with open(GOAL_FILE, "w") as file:
        json.dump([goal], file, indent=4)

    return goal["value"]

import json
import os
from datetime import datetime

# Creează fișierul JSON în folderul target
TARGET_FOLDER = os.path.dirname(os.path.abspath(__file__))
GOAL_FILE = os.path.join(TARGET_FOLDER, "reading_goals.json")

# Fișier pentru stocarea timpilor
TIME_FILE = os.path.join(TARGET_FOLDER, "reading_times.json")

def validate_time_input(value):
    """Validate if the input value is a positive integer."""
    if not value.isdigit() or int(value) <= 0:
        raise ValueError("Please enter a positive integer value.")
    return int(value)

def update_goal(goal_type, frequency, value):
    """Update the goal in the JSON file by replacing the previous goal."""
    # Data curentă
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Structura noului goal
    goal_data = {
        "goal_type": goal_type,
        "frequency": frequency,
        "value": value,
        "created_at": current_date
    }

    # Suprascrie fișierul cu noul goal
    with open(GOAL_FILE, "w") as file:
        json.dump([goal_data], file, indent=4)

    return f"Goal updated: {goal_type} ({frequency}) - {value}"

def get_current_goal():
    """Retrieve the current goal from the JSON file."""
    if os.path.exists(GOAL_FILE):
        with open(GOAL_FILE, "r") as file:
            data = json.load(file)
            if data:
                return data[0]  # Return the first (and only) goal
    return None

def save_reading_start():
    """Salvează timpul de început al sesiunii de citit."""
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(TIME_FILE, "w") as file:
        json.dump({"start_time": start_time}, file)

def save_reading_end():
    """Salvează timpul de sfârșit și returnează diferența în minute."""
    if not os.path.exists(TIME_FILE):
        return None

    end_time = datetime.now()
    with open(TIME_FILE, "r") as file:
        data = json.load(file)
        start_time = datetime.strptime(data["start_time"], "%Y-%m-%d %H:%M:%S")
        duration = (end_time - start_time).total_seconds() // 60  # Diferența în minute
    
    # Șterge timpul de început
    os.remove(TIME_FILE)

    return int(duration)

def update_goal_time_spent(minutes_spent):
    """Actualizează timpul rămas din goal-ul curent."""
    goal = get_current_goal()
    if not goal or goal["goal_type"] != "time":
        return None

    goal["value"] = max(0, goal["value"] - minutes_spent)  # Scade timpul petrecut
    with open(GOAL_FILE, "w") as file:
        json.dump([goal], file, indent=4)

    return goal["value"]

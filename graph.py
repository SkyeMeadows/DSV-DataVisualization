import json
import os
import matplotlib.pyplot as plt # type: ignore

script_dir = os.path.dirname(__file__)
data_path = os.path.join(script_dir, "data.json")

with open(data_path) as file:
    data = json.load(file)

sorted_weapons = sorted(
    data.items(), 
    key=lambda item: item[1].get("Points", 0), 
    reverse=False
)

weapon_names = [name for name, _ in sorted_weapons]
points_values = [data["Points"] for _, data in sorted_weapons]

# Graph
plt.figure(figsize=(20,12))
plt.barh(weapon_names, points_values, color="red")
plt.xlabel("Point Cost")
plt.title("Weapon Point Cost Comparison")
plt.tight_layout()
plt.show()
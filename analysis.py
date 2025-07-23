import json
import os

script_dir = os.path.dirname(__file__)
data_path = os.path.join(script_dir, "data.json")

with open(data_path, "r") as file:
    data = json.load(file)

while True:
    weapon_name = input("Enter Weapon Display Name: ").strip()

    if weapon_name not in data:
        print("Weapon not found. Please try again")
    else:
        break

print("\nCurrent Attributes:")
for attr, value in data[weapon_name].items():
    print(f"    {attr}: {value}")

attribute = input("\nEnter Attribute to change or add: ").strip()
current_value = data[weapon_name].get(attribute, "<Not Set>")
print(f"Current Atttribute Value: {current_value}")

new_value = input("Enter New Value: ").strip()

# Convert to number if possible
try:
    if "." in new_value:
        new_value = float(new_value)
    else:
        new_value = int(new_value)
except ValueError:
    pass  # Leave as string

data[weapon_name][attribute] = new_value

with open(data_path, "w") as file:
    json.dump(data, file, indent=2)

print(f"\n{attribute} updated to {new_value} for '{weapon_name}'")
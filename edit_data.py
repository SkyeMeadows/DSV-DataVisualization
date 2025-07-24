import json
import os
from rapidfuzz import process

script_dir = os.path.dirname(__file__)
data_path = os.path.join(script_dir, "data.json")

count_values_changed = 0

attribute_list = ["Points", "Range (Km)", "Projectile Speed (m/s)", "Shots per Second", "Shots in Clip", "Penetration/Clip (HA Blocks)", "Splash Radius (meters)", "Cycle Time", "Max Energy Draw/s (MW)", "Charge Reload Time", "Effective Integrity"]

while True:

    with open(data_path, "r") as file:
        data = json.load(file)

    weapon_name_list = list(data.keys())

    while True:
        weapon_name = input("Enter Weapon Display Name: ").strip()

        match, score, _ = process.extractOne(weapon_name, weapon_name_list)

        if score >= 60:
            print(f"\nMatched: {match}, please exit program if incorrect.")
        
        if score < 60:
            print(f"\nCouldn't match weapon name.")

        if match in weapon_name_list:
            weapon_name = match

        if weapon_name not in data:
            print("Weapon not found. Please try again")
        else:
            break

    while True:
        with open(data_path, "r") as file:
            data = json.load(file)

        print(f"\nCurrent Attributes for {weapon_name}:")
        for attribute, value in data[weapon_name].items():
            print(f"    {attribute}: {value}")

        attribute = input("\nEnter Attribute to change or add: ").strip()

        match, score, _ = process.extractOne(attribute, attribute_list)

        if score >= 60:
            print(f"\nMatched: {match}, please exit program if incorrect.")
        
        if score < 60:
            print(f"\nCouldn't match weapon name.")

        if match in attribute_list:
            attribute = match

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

        count_values_changed += 1

        change_attribute_again = input("\nChange Another Attribute? [y/N]: ").strip()

        if change_attribute_again.lower() in ["y", "Y", "yes", "Yes", "YES"]:
            continue
        else:
            break
    
    run_again = input("\nRun Again? [Y/n]: ").strip()
        
    if run_again.lower() in ["n", "N", "no", "No", "NO"]:
        break
    else:
        continue

print(f"Amount of values changed: {count_values_changed}")
print("Program has exited")

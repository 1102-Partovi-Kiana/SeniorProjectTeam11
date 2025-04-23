import shutil
import os


# Paths to the files in your repository
source_files = [
    "flask_app/stack.xml",
    "flask_app/organize_with_sensors.xml",
    "flask_app/organize.xml",
    "flask_app/reach.xml",
    "flask_app/pick_and_place.xml",
    "flask_app/sensor_robot.xml",
    "flask_app/shared.xml"
]


# Destination directory in the venv path
venv_path = os.path.join(
    "venv38", "lib", "python3.8", "site-packages", "gym", "envs", "robotics", "assets", "fetch"
)


# Ensure the destination directory exists
os.makedirs(venv_path, exist_ok=True)

# Copy files, deleting the original at the destination if it exists
for source_file in source_files:
    destination_file = os.path.join(venv_path, os.path.basename(source_file))
   
    # If the file already exists at the destination, delete it
    if os.path.exists(destination_file):
        os.remove(destination_file)
        print(f"Deleted existing file: {destination_file}")
   
    # Copy the source file to the destination
    shutil.copy(source_file, destination_file)
    print(f"File {os.path.basename(source_file)} replaced at: {destination_file}")

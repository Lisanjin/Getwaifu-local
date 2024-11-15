import subprocess
import os

input_path = "./ui/"
for input_ui in os.listdir(input_path):
    if input_ui.endswith(".ui"):
        print(input_ui)
        input_ui = f"./ui/{input_ui}"
        output_py = input_ui.replace(".ui", ".py")
        subprocess.run(["pyuic6", "-o", output_py, input_ui])
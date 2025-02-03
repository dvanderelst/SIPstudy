import subprocess

# List of scripts to run in succession
scripts = [
    "SCRIPT_process_activity.py",
    "SCRIPT_process_location.py",
    "SCRIPT_process_drinking.py",
    "SCRIPT_process_steps.py"
]

def run_scripts(scripts):
    for script in scripts:
        try:
            print(f"Running {script}...")
            result = subprocess.run(["python", script], check=True, capture_output=True, text=True)
            print(f"Output of {script}:\n{result.stdout}")
        except subprocess.CalledProcessError as e:
            print(f"Error running {script}: {e.stderr}")
            print("Exiting script execution.")
            break

if __name__ == "__main__":
    run_scripts(scripts)

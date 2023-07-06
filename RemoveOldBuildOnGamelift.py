import boto3
import tkinter as tk
from tkinter import messagebox

def remove_builds(amount):
    # Create a GameLift client
    gamelift_client = boto3.client('gamelift')

    # Describe the existing builds
    response = gamelift_client.list_builds(Limit=9999)

    # Extract the builds
    builds = response['Builds']

    if not builds:
        print("No builds found.")
        return

    # Sort the builds in ascending order (oldest first)
    builds.sort(key=lambda x: x['CreationTime'])

    # Remove the specified number of builds
    for build in builds[:amount]:
        build_id = build['BuildId']
        gamelift_client.delete_build(BuildId=build_id)
        print(f"Build {build_id} has been removed.")

def display_build_removal_ui():
    root = tk.Tk()
    root.title("Build Removal")

    label = tk.Label(root, text="Enter the number of builds to remove:")
    label.pack()

    entry = tk.Entry(root)
    entry.pack()

    def remove_builds_ui():
        amount = int(entry.get())
        confirmed = messagebox.askyesno("Confirmation", f"Are you sure you want to remove {amount} builds?")
        if not confirmed:
            return

        remove_builds(amount)
        messagebox.showinfo("Build Removal", f"{amount} builds have been removed.")

        root.destroy()

    button = tk.Button(root, text="Remove Builds", command=remove_builds_ui)
    button.pack()

    root.mainloop()

display_build_removal_ui()

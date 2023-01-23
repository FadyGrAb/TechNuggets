import csv
import pathlib
import secrets
import threading
from time import sleep
from tkinter import Listbox, StringVar, Tk, filedialog, messagebox
from tkinter.ttk import Button, Frame, Label, Progressbar

from killer_script import get_result


class MyApp(Tk):
    def __init__(self, width=600, height=170):
        self.width = width
        self.height = height
        self.create_gui()

    def create_gui(self):
        # Main window
        x, y = self.get_center_position()

        self.title("My App")
        self.geometry(f"{self.width}x{self.height}+{x}+{y}")

        # Surveys folder:
        #################
        # Tkinter variable that the widgets can use.
        self.surveys_path = StringVar()

        # A Frame widget to hold the button and label
        frame_surveys = Frame(self)
        frame_surveys.pack(fill="both", expand=True)

        # Create the button widget.
        self.button_surveys = Button(
            # Put the button inside the previously created frame.
            frame_surveys,
            text="Surveys Folder",
            width=30,
            # The function/method that the button executes.
            # It's a lambda funtion because we need to pass parameters
            # to the method. I that wasn't the case, we would have referenced
            # the method directly without lambda.
            command=lambda: self.get_directory(self.surveys_path)
        )
        # Place the button widget.
        self.button_surveys.pack(side="left", pady=10, padx=5)

        label_surveys = Label(
            frame_surveys,
            textvariable=self.surveys_path,
            background="white",
        )
        label_surveys.pack(side="left", expand=True)

        # Results csv file saving path:
        ###############################
        self.results_path = StringVar()

        frame_results = Frame(self)
        frame_results.pack(fill="both", expand=True)

        self.button_results = Button(
            frame_results,
            text="Results file path",
            width=30,
            command=lambda: self.get_directory(self.results_path)
        )
        self.button_results.pack(side="left", pady=10, padx=5)

        label_results = Label(
            frame_results,
            textvariable=self.results_path,
            background="white"
        )
        label_results.pack(side="left", expand=True)

        # Go button:
        ############
        # This button executes our business logic.
        self.button_go = Button(
            self,
            text="Go!",
            state="disabled",
            # See! No lambda as we don't need to pass parameters to the method.
            command=self.go
        )
        self.button_go.pack(pady=10)

    def get_center_position(self):
        x_center = (self.winfo_screenwidth() - self.width) / 2
        y_center = (self.winfo_screenheight() - self.height) / 2
        return int(x_center), int(y_center)

    def get_directory(self, path_variable):
        directory = filedialog.askdirectory()
        if directory:
            # Set the passed path variable to the chosen dirctory.
            path_variable.set(directory)
        # Unlock the "go" button if both directories are entered by the user.
        self.unlock_go_button()

    def unlock_go_button(self):
        # If the user entered both directories, unlock the go button.
        if (self.surveys_path.get() != "") and \
                (self.results_path.get() != ""):
            self.button_go["state"] = "enabled"

    def go(self):
        # Our main handler method.

        # Disable the buttons so the user doesn't interupt the app while processing
        # the images.
        self.change_buttons_state("disabled")

        # Show the progressbar and the log list box.
        self.show_progressbar()
        self.show_log_listbox()

        # Run the business logic on another thread than the GUI.
        threading.Thread(target=self.process_images).start()

    def process_images(self):
        # To get the images, the real code would be:
        # images_path = pathlib.Path(self.surveys_path.get())
        # images = list(images_path.glob("*.jpg"))

        # Dummy images list.
        images = [secrets.token_urlsafe(5) + ".jpg" for _ in range(20)]

        # The results csv file saving directory.
        results_file = pathlib.Path(self.results_path) / "results.csv"

        # Write a csv file with DictWriter class from the csv module.
        with results_file.open(mode="w") as csv_results_file:
            header = ["filename", "q1", "q2", "q3", "q4", "q5"]
            csv_dictwriter = csv.DictWriter(
                csv_results_file, fieldnames=header)
            csv_dictwriter.writeheader()

            for idx, image in enumerate(images):
                # Use the function form the killer_script module to
                # execute the business logic.
                csv_dictwriter.writerow(get_result(image))

                # Update the progess bar and the log listbox.
                # Progressbar
                current_progess = (idx + 1) / len(images)
                self.progress_bar["value"] = current_progess * 100
                self.progress_value.set(f"{current_progess:.0%} completed")
                # Log listbox
                self.write_log(idx, image)

        # Show completion messagebox and change the buttons back to enabled.
        messagebox.showinfo(title="MyApp", message="I've finished!")
        self.change_buttons_state("enabled")

    def show_progressbar(self):
        # Progress bar
        self.progress_value = StringVar()

        self.progress_bar = Progressbar(
            self,
            orient="horizontal",
            length=100,
            mode='determinate'
        )
        self.progress_bar.pack(fill="both", expand=True, padx=5)

        self.label_progress_bar = Label(
            self,
            textvariable=self.progress_value,
            anchor="center",
        )
        self.label_progress_bar.pack(fill="both", expand=True)

    def show_log_listbox(self):
        # Make the main window a little taller.
        self.geometry("{}x{}".format(self.width, self.height + 230))

        # Create a listbox as a log container.
        try:
            # Delete all log entry if the listbox is already created.
            self.listbox_log.delete(0, "end")
        except:
            self.listbox_log = Listbox(self, height=10)
            self.listbox_log.pack(fill="both", expand=True, padx=5)

    def change_buttons_state(self, state):
        self.button_surveys["state"] = state
        self.button_results["state"] = state
        self.button_go["state"] = state

    def write_log(self, index, message):
        entry = f"SUCCESS: {message}"
        self.listbox_log.insert(index, entry)
        # Always make the new entry visible in the listbox
        self.listbox_log.see(index)

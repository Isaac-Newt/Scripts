import tkinter as tk
import tkinter.ttk as ttk
from test_module import *
import podcast_scraper as ps


class Application(tk.Frame):
    def __init__(self, superior = None):
        """__init__"""
        super().__init__(superior)
        self.superior = superior
        self.grid(row = 0, column = 0, padx = 32, pady = 32)
        self.create_widgets()

    def create_widgets(self):
        """Create window widgets"""
        # Create application frame
        self.tframe = ttk.Frame(self)
        self.mframe = ttk.Frame(self)
        self.bframe = ttk.Frame(self)

        # Informational Labels
        greeting: str = "Welcome to the Messy Jesus Business Podcast Archiver"
        self.greet = ttk.Label(self.tframe, text=greeting, font=(18))
        self.greet.grid(row=0, column=0, padx = 16, pady = 8)

        information: str = """
                    Select an option below to begin the archiving process.\n
                    New Episodes will retrieve only episodes published since the
                    last time this program was run, while All Episodes will
                    retrieve every Messy Jesus Business episode available online.                    
                    """
        self.info = ttk.Label(self.tframe, text=information)
        self.info.grid(row=1, column=0, padx = 16, pady=8)
        
        # Button to run the scraper script
        self.new = ttk.Button(self.mframe, text="New Episodes",
                               command = lambda: ps.main(self))
        self.new.grid(row=0, column=0, padx=16, pady=8)

        # Button to run the scraper script in all-episodes mode
        self.all = ttk.Button(self.mframe, text="All Episodes",
                               command = lambda: ps.main(self, True))
        self.all.grid(row=0, column=1, padx=16, pady=8)

        # Button to quit the application
        self.quit = ttk.Button(self.mframe, text="Quit",
                               command = self.superior.destroy)
        self.quit.grid(row=1, column=0, columnspan=2, padx = 16, pady = 8)

        # Status message for current operation
        self.status = ttk.Label(self.bframe, text="Ready to Begin", font=(18))
        self.status.grid(row=0, column=0, columnspan=2, padx=32, pady=16)

        # Add frames to main window
        self.tframe.grid(column=0, row=0)
        self.mframe.grid(column=0, row=1)
        self.bframe.grid(column=0, row=2)
        
root = tk.Tk()
root.title("Podcast Archiver")
app = Application(superior = root)
app.mainloop()

from pathlib import Path

import customtkinter as ctk
from tkinter import filedialog

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Knowledge Explorer")
        self.geometry("1100x700")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        print(screen_width, screen_height)
        self.minsize(900, 600)
        window_width = 900
        window_height = 600
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.main_frame = ctk.CTkFrame(self)
        self.create_layout()


    def create_layout(self):

        self.main_frame.pack(fill="both", expand=True)

        self.main_frame.grid_columnconfigure(0, weight=0, minsize=250)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        self.create_left_panel()
        self.create_right_panel()


    def create_left_panel(self):

        self.left_panel = ctk.CTkFrame(
            self.main_frame,
            width=250,
            fg_color="#3B3B3B"
        )
        print(self.left_panel.cget("width"))
        self.left_panel.grid(row=0, column=0, sticky="nsew")
        self.left_panel.grid_propagate(False)

        label = ctk.CTkLabel(
            self.left_panel,
            text="Documents"
        )
        label.pack(pady=20)

        self.add_button = ctk.CTkButton(
            self.left_panel,
            text="Add PDF",
            command=self.add_pdf
        )

        self.add_button.pack(fill="x", padx=15, pady=10)

        documents_label = ctk.CTkLabel(
            self.left_panel,
            text="Indexed Documents"
        )
        documents_label.pack(pady=(30, 10))

        self.document_list = ctk.CTkTextbox(
            self.left_panel,
            height=300
        )
        self.document_list.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )


    def create_right_panel(self):

        self.right_panel = ctk.CTkFrame(
            self.main_frame,
            fg_color="#2B2B2B"
        )
        self.right_panel.grid(row=0, column=1, sticky="nsew")
        self.create_question_frame()
        self.create_answers()
        self.create_sources()


    def create_sources(self):
        sources_label = ctk.CTkLabel(
            self.right_panel,
            text="Sources"
        )
        sources_label.pack(pady=(30, 10))

        self.sources_list = ctk.CTkTextbox(
            self.right_panel,
            height=100
        )
        self.sources_list.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

    def create_answers(self):
        answer_label = ctk.CTkLabel(
            self.right_panel,
            text="Answer"
            )
        answer_label.pack(pady=(30, 10))

        self.answer_list = ctk.CTkTextbox(
            self.right_panel,
            height=300
        )
        self.answer_list.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

    def create_question_frame(self):
        label = ctk.CTkLabel(
            self.right_panel,
            text="Question"
        )
        label.pack(pady=20)

        self.question_frame = ctk.CTkFrame(
            self.right_panel,
            fg_color="#2C2D3B"
        )
        self.question_frame.grid_columnconfigure(0, weight=1)
        self.question_frame.grid_columnconfigure(1, weight=0)
        self.question_frame.pack(fill="x", padx=25)

        self.question_entry = ctk.CTkEntry(
            self.question_frame,
            fg_color="#2C2D3B")

        self.ask_button = ctk.CTkButton(
            self.question_frame,
            width=120,
            text="Ask",
            command=self.ask_question
        )
        self.question_entry.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 10)
        )
        self.ask_button.grid(
            row=0,
            column=1
        )

    def ask_question(self):
        question = self.question_entry.get()
        self.answer_list.insert("end", f"Question: {question}\n")

    def add_pdf(self):

        filename = filedialog.askopenfilename(
            title="Select PDF",
            filetypes=[("PDF Files", "*.pdf")]
        )
        self.document_list.insert("end",Path(filename).name)
        print(filename)
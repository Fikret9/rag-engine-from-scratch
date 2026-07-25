import threading
from pathlib import Path

import customtkinter as ctk
from tkinter import filedialog


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MainWindow(ctk.CTk):

    def __init__(self,processor,chatbot, metadata_store):
        super().__init__()
        self.chatbot = chatbot
        self.processor = processor
        self.metadata_store = metadata_store

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

        self.main_frame = ctk.CTkFrame(
            self,
            fg_color="#0D1117"      # <-- CHANGED (was #1E2430)
        )
        self.create_layout()


    def create_layout(self):

        self.main_frame.pack(fill="both", expand=True)
        self.main_frame.grid_columnconfigure(0, weight=0, minsize=320)
        self.main_frame.grid_columnconfigure(1, weight=1)

        self.main_frame.grid_rowconfigure(0, weight=1)   # <-- ADD
        self.main_frame.grid_rowconfigure(1, weight=0)
         #

        self.create_left_panel()
        self.create_right_panel()


    def create_left_panel(self):

        self.left_panel = ctk.CTkFrame(
            self.main_frame,
            width=350,
            corner_radius=6,
            fg_color="#151B26"      # <-- CHANGED (was #252C3A)
        )

        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        self.left_panel.grid_propagate(False)

        title = ctk.CTkLabel(
            self.left_panel,
            text="📚 Documents",
            font=("Segoe UI", 16, "bold")      # <-- CHANGED (was 18)
        )

        title.pack(anchor="w", padx=15, pady=(15, 10))

        self.add_button = ctk.CTkButton(
            self.left_panel,
            text="+ Add Document",
            height=34,                   # <-- CHANGED (was 40)
            corner_radius=4,             # <-- NEW
            fg_color="#3574F0",          # <-- NEW
            hover_color="#4A84F5",       # <-- NEW
            font=("Segoe UI", 12),
            command=self.add_pdf
        )


        self.add_button.pack(fill="x", padx=15, pady=(0, 15))

        self.document_frame = ctk.CTkScrollableFrame(
            self.left_panel,
            fg_color="#151B26"      # <-- CHANGED
        )
        self.document_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        self.load_documents()


    def create_right_panel(self):

        self.right_panel = ctk.CTkFrame(
            self.main_frame,
            fg_color="#0D1117"      # <-- CHANGED (was #1E2430)
        )
        self.right_panel.grid(row=0, column=1, sticky="nsew")
        self.create_status()
        self.create_question_frame()
        self.create_answers()
        self.create_sources()


    def create_sources(self):
        sources_label = ctk.CTkLabel(
            self.right_panel,
            text="Sources",
            font=("Segoe UI", 13)              # <-- NEW
        )
        sources_label.pack(
            anchor="w",          # <-- NEW
            padx=25,             # <-- NEW
            pady=(18, 6)         # <-- CHANGED
        )

        self.sources_frame = ctk.CTkScrollableFrame(
            self.right_panel,
            height=100,
            fg_color="#111720",
            corner_radius=4,
            border_width=1,
            border_color="#2B394D"
        )

        self.sources_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )



    def create_answers(self):
        answer_label = ctk.CTkLabel(
            self.right_panel,
            text="Answer",
            font=("Segoe UI", 13)              # <-- NEW
        )
        answer_label.pack(
            anchor="w",          # <-- NEW
            padx=25,             # <-- NEW
            pady=(18, 6)         # <-- CHANGED
        )

        self.answer_list = ctk.CTkTextbox(
            self.right_panel,
            height=220,                  # <-- CHANGED (was 300)
            fg_color="#111720",
            corner_radius=4,
            border_width=1,              # <-- NEW
            border_color="#2B394D"       # <-- NEW
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
            text="Question",
            font=("Segoe UI", 13)              # <-- NEW
        )
        label.pack(
            anchor="w",          # <-- NEW
            padx=25,             # <-- NEW
            pady=(12, 6)         # <-- CHANGED
        )

        self.question_frame = ctk.CTkFrame(
            self.right_panel,
            fg_color="#161D2B",
            corner_radius=4,             # <-- NEW (match the rest)
            border_width=1,              # <-- NEW
            border_color="#2B394D"       # <-- NEW
        )
        self.question_frame.grid_columnconfigure(0, weight=1)
        self.question_frame.grid_columnconfigure(1, weight=0)
        self.question_frame.pack(fill="x", padx=25)

        self.question_entry = ctk.CTkEntry(
            self.question_frame,
            fg_color="#161D2B",
            border_color="#2B394D",
            corner_radius=4              # <-- NEW
        )
        self.question_entry.bind(
            "<Return>",
            lambda event: self.ask_question()
        )

        self.ask_button = ctk.CTkButton(
            self.question_frame,
            width=100,                   # <-- CHANGED (was 120)
            height=34,                   # <-- NEW
            corner_radius=4,             # <-- NEW
            fg_color="#3574F0",          # <-- NEW
            hover_color="#4A84F5",       # <-- NEW
            text="Ask",
            font=("Segoe UI", 12),
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
        self.ask_button.configure(
            text="⏳ Thinking",
            fg_color="#D97706",      # <-- amber
            hover_color="#D97706"
        )

        for widget in self.sources_frame.winfo_children():
            widget.destroy()

        self.update()
        question = self.question_entry.get()
        answer, results = self.chatbot.ask(question)

        self.answer_list.delete("1.0", "end")
        self.answer_list.insert("end", answer)

        for score, text, source in results:
            filename = Path(source).name
            if score >= 0.65:
                color = "#22C55E"
            elif score >= 0.50:
                color = "#FACC15"
            else:
                color = "#EF4444"

            card = ctk.CTkFrame(
                self.sources_frame,
                height=34,
                fg_color="#202A3A",
                corner_radius=4
            )

            card.pack(fill="x", padx=3, pady=3)
            card.pack_propagate(False)

            file_label = ctk.CTkLabel(
                card,
                text=f"📄 {filename}",
                font=("Segoe UI", 12)
            )

            file_label.pack(
                side="left",
                padx=10
            )

            score_label = ctk.CTkLabel(
                card,
                text=f"{score:.0%}",
                text_color=color,
                font=("Segoe UI", 12, "bold")
            )

            score_label.pack(
                side="right",
                padx=10
            )

        self.ask_button.configure(
            text="Ask",
            fg_color="#3574F0",
            hover_color="#4A84F5",
            state="normal"
        )


    def add_pdf(self):

        filename = filedialog.askopenfilename(
            title="Select PDF",
            filetypes=[
                ("Supported Documents", "*.pdf *.docx *.txt"),
                ("PDF Files", "*.pdf"),
                ("Word Documents", "*.docx"),
                ("Text Files", "*.txt"),
                ("All Files", "*.*"),
            ]
        )

        if not filename:
            return

        self.add_button.configure(
            text="⏳ Indexing...",
            fg_color="#D97706",
            hover_color="#D97706"
        )

        threading.Thread(
            target=self.index_document,
            args=(filename,),
            daemon=True
        ).start()

    def index_document(self, filename):
        self.processor.process_document(filename)
        self.after(0, self.index_complete)

    def index_complete(self):

        self.reload_documents()

        self.add_button.configure(
            text="+ Add PDF",
            state="normal",
            fg_color="#3574F0",
            hover_color="#4A84F5"
        )


    def load_documents(self):

        for filename in self.metadata_store.data:

            card = ctk.CTkFrame(
                self.document_frame,
                corner_radius=4,
                fg_color="#202A3A",     # <-- CHANGED (was #3A3A3A)
                height=40,                       # <-- CHANGED (was 44)
                border_width=0
            )

            card.pack(fill="x", padx=2, pady=3)
            card.pack_propagate(False)

            label = ctk.CTkLabel(
                card,
                text=f"📄 {filename}",
                anchor="w",
                font=("Segoe UI", 12)              # <-- CHANGED (was 13)
            )

            label.pack(side="left", fill="x", expand=True,padx=10)


            delete_btn = ctk.CTkButton(
                card,
                text="🗑",
                width=24,
                height=24,
                fg_color="transparent",
                text_color="#B35A5A",
                hover_color="#3B2323",
                command=lambda f=filename: self.delete_document(f)
            )

            delete_btn.pack(side="right",padx=6 )

    def create_status(self):

        docs = len(self.metadata_store.data)

        self.status_frame = ctk.CTkFrame(self.right_panel, fg_color="transparent")
        self.status_frame.pack(anchor="w", padx=25, pady=(16, 10))
        ctk.CTkLabel(self.status_frame, text="●", text_color="#22C55E",
             font=("Segoe UI", 12, "bold")).pack(side="left")

        ctk.CTkLabel(self.status_frame, text=" Ready",
             text_color="#D7DCE5", font=("Segoe UI", 11)).pack(side="left")

        ctk.CTkLabel(self.status_frame, text=" │ ",
             text_color="#5E6A7D", font=("Segoe UI", 11)).pack(side="left")

        ctk.CTkLabel(self.status_frame, text=f"📄 {docs} Documents",
             text_color="#D7DCE5", font=("Segoe UI", 11)).pack(side="left")

        ctk.CTkLabel(self.status_frame, text=" │ ",
             text_color="#5E6A7D", font=("Segoe UI", 11)).pack(side="left")

        ctk.CTkLabel(self.status_frame, text="🤖 ",
             text_color="#D7DCE5", font=("Segoe UI", 11)).pack(side="left")

        ctk.CTkLabel(self.status_frame, text="qwen2.5",
             text_color="#3574F0", font=("Segoe UI", 11, "bold")).pack(side="left")

    def delete_document(self, filename):
        self.processor.delete_document(filename)

        self.metadata_store.delete_document(filename)
        self.metadata_store.save()

        self.reload_documents()

    def reload_documents(self):
        # Remove existing cards
        for widget in self.document_frame.winfo_children():
            widget.destroy()

        # Build them again
        self.load_documents()

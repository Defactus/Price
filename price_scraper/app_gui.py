import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import asyncio
from scraper_logic import run_scraper  # We will extract logic to this

class PriceScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bot de Preços - Mercado Livre & Shopee")
        self.root.geometry("500x300")

        self.input_file = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # File Selection Frame
        frame_file = tk.Frame(self.root, pady=20)
        frame_file.pack(fill=tk.X)

        tk.Label(frame_file, text="Planilha de Produtos (.xlsx):").pack(side=tk.TOP, anchor='w', padx=20)

        entry_frame = tk.Frame(frame_file)
        entry_frame.pack(fill=tk.X, padx=20, pady=5)

        self.entry_file = tk.Entry(entry_frame, textvariable=self.input_file, width=40)
        self.entry_file.pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Button(entry_frame, text="Procurar...", command=self.browse_file).pack(side=tk.RIGHT, padx=5)

        # Start Button
        self.btn_start = tk.Button(self.root, text="Iniciar Raspagem", command=self.start_scraping,
                                  bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        self.btn_start.pack(pady=20)

        # Progress and Status
        self.status_var = tk.StringVar()
        self.status_var.set("Aguardando inicialização...")
        tk.Label(self.root, textvariable=self.status_var, wraplength=450).pack(pady=5)

        self.progress = ttk.Progressbar(self.root, orient=tk.HORIZONTAL, length=400, mode='determinate')
        self.progress.pack(pady=10)

    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Selecione a Planilha",
            filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*"))
        )
        if filename:
            self.input_file.set(filename)

    def update_status(self, text, progress_val=None):
        self.status_var.set(text)
        if progress_val is not None:
            self.progress['value'] = progress_val
        self.root.update_idletasks()

    def scraping_thread(self):
        try:
            # We run the asyncio event loop in this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(run_scraper(self.input_file.get(), self.update_status))
            loop.close()

            self.root.after(0, lambda: messagebox.showinfo("Sucesso", "Busca finalizada com sucesso!"))
            self.root.after(0, lambda: self.update_status("Finalizado!", 100))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}"))
            self.root.after(0, lambda: self.update_status("Erro na execução.", 0))
        finally:
            self.root.after(0, lambda: self.btn_start.config(state=tk.NORMAL))

    def start_scraping(self):
        if not self.input_file.get():
            messagebox.showwarning("Aviso", "Por favor, selecione a planilha de entrada.")
            return

        self.btn_start.config(state=tk.DISABLED)
        self.progress['value'] = 0
        self.update_status("Iniciando bot...")

        # Start scraping in a background thread so GUI doesn't freeze
        thread = threading.Thread(target=self.scraping_thread)
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = PriceScraperApp(root)
    root.mainloop()

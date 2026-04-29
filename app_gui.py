from __future__ import annotations

import os
import queue
import threading
from pathlib import Path
from tkinter import BooleanVar, StringVar, Tk, filedialog, messagebox, ttk
import tkinter as tk

from price_app.core import ScraperOptions, compare_products_sync


class PriceComparerApp:
    def __init__(self, root: Tk) -> None:
        self.root = root
        self.root.title("Comparador de Precos")
        self.root.geometry("760x520")
        self.root.minsize(680, 460)

        self.input_path = StringVar()
        self.output_path = StringVar()
        self.show_browser = BooleanVar(value=True)
        self.include_shopee = BooleanVar(value=False)
        self.running = False
        self.messages: queue.Queue[tuple[str, str]] = queue.Queue()

        self._build_ui()
        self.root.after(100, self._drain_messages)

    def _build_ui(self) -> None:
        container = ttk.Frame(self.root, padding=16)
        container.pack(fill=tk.BOTH, expand=True)
        container.columnconfigure(1, weight=1)
        container.rowconfigure(5, weight=1)

        ttk.Label(container, text="Planilha").grid(row=0, column=0, sticky="w", pady=(0, 8))
        ttk.Entry(container, textvariable=self.input_path).grid(row=0, column=1, sticky="ew", padx=8, pady=(0, 8))
        ttk.Button(container, text="Selecionar", command=self._select_input).grid(row=0, column=2, pady=(0, 8))

        ttk.Label(container, text="Resultado").grid(row=1, column=0, sticky="w", pady=(0, 8))
        ttk.Entry(container, textvariable=self.output_path).grid(row=1, column=1, sticky="ew", padx=8, pady=(0, 8))
        ttk.Button(container, text="Salvar como", command=self._select_output).grid(row=1, column=2, pady=(0, 8))

        options = ttk.Frame(container)
        options.grid(row=2, column=0, columnspan=3, sticky="w", pady=(4, 12))
        ttk.Checkbutton(options, text="Mostrar navegador", variable=self.show_browser).pack(side=tk.LEFT, padx=(0, 18))
        ttk.Checkbutton(options, text="Tentar Shopee (experimental)", variable=self.include_shopee).pack(side=tk.LEFT)

        actions = ttk.Frame(container)
        actions.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(0, 12))
        self.start_button = ttk.Button(actions, text="Iniciar busca", command=self._start)
        self.start_button.pack(side=tk.LEFT)
        ttk.Button(actions, text="Abrir resultado", command=self._open_result).pack(side=tk.LEFT, padx=8)

        self.progress = ttk.Progressbar(container, mode="indeterminate")
        self.progress.grid(row=4, column=0, columnspan=3, sticky="ew", pady=(0, 12))

        self.log_box = tk.Text(container, height=14, wrap=tk.WORD)
        self.log_box.grid(row=5, column=0, columnspan=3, sticky="nsew")
        self.log_box.configure(state=tk.DISABLED)

    def _select_input(self) -> None:
        filename = filedialog.askopenfilename(
            title="Selecione produtos.xlsx",
            filetypes=[("Excel", "*.xlsx"), ("Todos os arquivos", "*.*")],
        )
        if not filename:
            return
        self.input_path.set(filename)
        if not self.output_path.get():
            self.output_path.set(str(Path(filename).with_name("resultado_comparacao.xlsx")))

    def _select_output(self) -> None:
        filename = filedialog.asksaveasfilename(
            title="Salvar resultado",
            defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx")],
        )
        if filename:
            self.output_path.set(filename)

    def _start(self) -> None:
        if self.running:
            return
        if not self.input_path.get():
            messagebox.showerror("Planilha obrigatoria", "Selecione a planilha produtos.xlsx.")
            return
        if not self.output_path.get():
            self.output_path.set(str(Path(self.input_path.get()).with_name("resultado_comparacao.xlsx")))

        self.running = True
        self.start_button.configure(state=tk.DISABLED)
        self.progress.start(10)
        self._append_log("Iniciando busca...")

        worker = threading.Thread(target=self._run_worker, daemon=True)
        worker.start()

    def _run_worker(self) -> None:
        try:
            options = ScraperOptions(
                headless=not self.show_browser.get(),
                include_shopee=self.include_shopee.get(),
            )
            output = compare_products_sync(
                self.input_path.get(),
                self.output_path.get(),
                options,
                lambda message: self.messages.put(("log", message)),
            )
            self.messages.put(("done", str(output)))
        except Exception as exc:
            self.messages.put(("error", str(exc)))

    def _drain_messages(self) -> None:
        try:
            while True:
                kind, message = self.messages.get_nowait()
                if kind == "log":
                    self._append_log(message)
                elif kind == "done":
                    self._finish()
                    self._append_log(f"Resultado salvo em: {message}")
                    messagebox.showinfo("Concluido", f"Resultado salvo em:\n{message}")
                elif kind == "error":
                    self._finish()
                    self._append_log(f"Erro: {message}")
                    messagebox.showerror("Erro", message)
        except queue.Empty:
            pass
        self.root.after(100, self._drain_messages)

    def _finish(self) -> None:
        self.running = False
        self.progress.stop()
        self.start_button.configure(state=tk.NORMAL)

    def _append_log(self, message: str) -> None:
        self.log_box.configure(state=tk.NORMAL)
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.see(tk.END)
        self.log_box.configure(state=tk.DISABLED)

    def _open_result(self) -> None:
        path = self.output_path.get()
        if not path or not Path(path).exists():
            messagebox.showerror("Arquivo nao encontrado", "O resultado ainda nao existe.")
            return
        os.startfile(path)


def main() -> None:
    root = Tk()
    PriceComparerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()


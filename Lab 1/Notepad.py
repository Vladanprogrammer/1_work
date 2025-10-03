#!/usr/bin/env python3
"""
Простий блокнот на Python (Tkinter) для macOS / Linux / Windows.

Функції:
- Новий файл, Відкрити, Зберегти, Зберегти як
- Вирізати/Копіювати/Вставити
- Скасувати/Повторити
- Пошук і заміна
- Переключення обтікання рядка (word wrap)
- Горячі клавіші (Ctrl/Cmd + S, O, N, F, Q)

Запуск:
    python3 notepad_mac.py

Примітка для macOS: переконайся, що Python встановлений (рекомендується з python.org) і підтримує Tkinter.
"""

import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, font

APP_TITLE = "Простий Блокнот"

class Notepad(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry('900x600')

        # Стан
        self.filepath = None
        self._wrap = True

        # Текстовий віджет
        self.text = tk.Text(self, undo=True, wrap='word')
        self.scroll = tk.Scrollbar(self, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scroll.set)
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Меню
        self.create_menu()
        self.create_bindings()

    def create_menu(self):
        menubar = tk.Menu(self)

        # File
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label='Новий    (⌘N)', command=self.new_file)
        file_menu.add_command(label='Відкрити (⌘O)', command=self.open_file)
        file_menu.add_command(label='Зберегти (⌘S)', command=self.save_file)
        file_menu.add_command(label='Зберегти як...', command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label='Вийти (⌘Q)', command=self.exit_app)
        menubar.add_cascade(label='Файл', menu=file_menu)

        # Edit
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label='Скасувати', command=self.text.edit_undo)
        edit_menu.add_command(label='Повторити', command=self.text.edit_redo)
        edit_menu.add_separator()
        edit_menu.add_command(label='Вирізати', command=lambda: self.event_generate('<<Cut>>'))
        edit_menu.add_command(label='Копіювати', command=lambda: self.event_generate('<<Copy>>'))
        edit_menu.add_command(label='Вставити', command=lambda: self.event_generate('<<Paste>>'))
        edit_menu.add_separator()
        edit_menu.add_command(label='Знайти/Замінити (⌘F)', command=self.find_replace_dialog)
        menubar.add_cascade(label='Правка', menu=edit_menu)

        # View
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_checkbutton(label='Переносити рядки', onvalue=True, offvalue=False,
                                  variable=tk.BooleanVar(value=self._wrap), command=self.toggle_wrap)
        menubar.add_cascade(label='Вигляд', menu=view_menu)

        # Help
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label='Про', command=self.show_about)
        menubar.add_cascade(label='Довідка', menu=help_menu)

        self.config(menu=menubar)

    def create_bindings(self):
        # Крос-платформені гарячі клавіші
        if sys.platform == 'darwin':
            # macOS: Command
            self.bind_all('<Command-s>', lambda e: self.save_file())
            self.bind_all('<Command-o>', lambda e: self.open_file())
            self.bind_all('<Command-n>', lambda e: self.new_file())
            self.bind_all('<Command-q>', lambda e: self.exit_app())
            self.bind_all('<Command-f>', lambda e: self.find_replace_dialog())
        else:
            # Windows/Linux: Control
            self.bind_all('<Control-s>', lambda e: self.save_file())
            self.bind_all('<Control-o>', lambda e: self.open_file())
            self.bind_all('<Control-n>', lambda e: self.new_file())
            self.bind_all('<Control-q>', lambda e: self.exit_app())
            self.bind_all('<Control-f>', lambda e: self.find_replace_dialog())

    # File actions
    def new_file(self):
        if self.confirm_unsaved():
            self.text.delete('1.0', tk.END)
            self.filepath = None
            self.title(APP_TITLE)

    def open_file(self):
        if not self.confirm_unsaved():
            return
        path = filedialog.askopenfilename(filetypes=[('Text files', '*.txt *.py *.md *.csv *.log'), ('All files', '*.*')])
        if path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = f.read()
                self.text.delete('1.0', tk.END)
                self.text.insert(tk.END, data)
                self.filepath = path
                self.title(f"{os.path.basename(path)} — {APP_TITLE}")
            except Exception as e:
                messagebox.showerror('Помилка', f'Не вдалось відкрити файл:\n{e}')

    def save_file(self):
        if self.filepath:
            try:
                with open(self.filepath, 'w', encoding='utf-8') as f:
                    f.write(self.text.get('1.0', tk.END))
                messagebox.showinfo('Збережено', 'Файл збережено')
            except Exception as e:
                messagebox.showerror('Помилка', f'Не вдалось зберегти файл:\n{e}')
        else:
            self.save_file_as()

    def save_file_as(self):
        path = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Text files', '*.txt *.py *.md'), ('All files', '*.*')])
        if path:
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(self.text.get('1.0', tk.END))
                self.filepath = path
                self.title(f"{os.path.basename(path)} — {APP_TITLE}")
                messagebox.showinfo('Збережено', 'Файл збережено')
            except Exception as e:
                messagebox.showerror('Помилка', f'Не вдалось зберегти файл:\n{e}')

    def exit_app(self):
        if self.confirm_unsaved():
            self.destroy()

    def confirm_unsaved(self):
        content = self.text.get('1.0', tk.END).strip()
        if content and not self.filepath:
            res = messagebox.askyesnocancel('Збереження', 'Зберегти зміни перед виходом?')
            if res is None:
                return False
            if res:
                self.save_file_as()
        elif content and self.filepath:
            # Можна ще перевірити, чи змінився текст проти файлу — тут опустимо
            pass
        return True

    def toggle_wrap(self):
        self._wrap = not self._wrap
        self.text.configure(wrap='word' if self._wrap else 'none')

    def show_about(self):
        messagebox.showinfo('Про', f'{APP_TITLE}\nПростий блокнот на Python (Tkinter)')

    # Find & Replace dialog
    def find_replace_dialog(self):
        dlg = tk.Toplevel(self)
        dlg.title('Знайти/Замінити')
        dlg.transient(self)
        dlg.resizable(False, False)

        tk.Label(dlg, text='Знайти:').grid(row=0, column=0, sticky='w', padx=6, pady=6)
        find_ent = tk.Entry(dlg, width=30)
        find_ent.grid(row=0, column=1, padx=6, pady=6)
        find_ent.focus()

        tk.Label(dlg, text='Замінити на:').grid(row=1, column=0, sticky='w', padx=6, pady=6)
        repl_ent = tk.Entry(dlg, width=30)
        repl_ent.grid(row=1, column=1, padx=6, pady=6)

        case_var = tk.BooleanVar(value=False)
        tk.Checkbutton(dlg, text='Регістр має значення', variable=case_var).grid(row=2, column=0, columnspan=2, sticky='w', padx=6)

        def do_find():
            self.text.tag_remove('found', '1.0', tk.END)
            needle = find_ent.get()
            if not needle:
                return
            start = '1.0'
            flags = 0 if case_var.get() else tk.END
            count = tk.IntVar()
            while True:
                pos = self.text.search(needle, start, stopindex=tk.END, nocase=(not case_var.get()), count=count)
                if not pos:
                    break
                end = f"{pos}+{count.get()}c"
                self.text.tag_add('found', pos, end)
                start = end
            self.text.tag_config('found', background='yellow')

        def do_replace():
            needle = find_ent.get()
            repl = repl_ent.get()
            if not needle:
                return
            if not case_var.get():
                content = self.text.get('1.0', tk.END)
                new = content.replace(needle, repl)
                self.text.delete('1.0', tk.END)
                self.text.insert('1.0', new)
            else:
                # простий регістр-залежний прохід
                start = '1.0'
                count = tk.IntVar()
                while True:
                    pos = self.text.search(needle, start, stopindex=tk.END, nocase=False, count=count)
                    if not pos:
                        break
                    end = f"{pos}+{count.get()}c"
                    self.text.delete(pos, end)
                    self.text.insert(pos, repl)
                    start = f"{pos}+{len(repl)}c"

        tk.Button(dlg, text='Знайти', command=do_find).grid(row=3, column=0, padx=6, pady=8)
        tk.Button(dlg, text='Замінити всі', command=do_replace).grid(row=3, column=1, padx=6, pady=8)

        dlg.grab_set()


if __name__ == '__main__':
    app = Notepad()
    app.mainloop()

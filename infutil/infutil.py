import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import filecmp
import os

class FileUtilityApp:
    def __init__(self, root):
        self.root = root
        # Language settings
        self.current_lang = 'ru' # Default language
        self.translations = {
            'ru': {
                'title': "Утилита: Объединение и Сравнение файлов",
                'mode_merge': "Объединить файлы",
                'mode_compare': "Сравнить файлы/папки",
                'merge_files': "Файлы",
                'merge_folder': "Папка",
                'merge_extension': "Расширение:",
                'merge_recursive': "Включая подпапки",
                'merge_add': "Добавить",
                'merge_remove_selected': "Удалить выбранные",
                'merge_split': "Разделить результат на части",
                'merge_split_lines': "строк",
                'merge_split_mb': "мб",
                'merge_split_suffix': "строк / мб на файл",
                'merge_button': "Объединить",
                'merge_file_header': "--- Файл: {filename} ---",
                'merge_done': "Объединено в: {path}",
                'merge_error': "Не удалось объединить файлы: {error}",
                'merge_split_done_lines': "Файл разделен на {count} частей по {amount} строк.",
                'merge_split_done_mb': "Файл разделен на {count} частей по ~{size:.2f} МБ.",
                'merge_split_error': "Ошибка при разделении файла: {error}",
                'compare_choose_first': "Выбрать первое",
                'compare_choose_second': "Выбрать второе",
                'compare_button': "Сравнить",
                'compare_identical': "Файлы идентичны.",
                'compare_different': "Файлы отличаются.",
                'compare_error_files': "Ошибка при сравнении файлов: {error}",
                'compare_folders_identical': "Папки идентичны.",
                'compare_folders_diff_files': "Отличающиеся файлы: {files}",
                'compare_folders_only_left': "Только в первой папке: {files}",
                'compare_folders_only_right': "Только во второй папке: {files}",
                'compare_subfolder': "--- Подпапка: {name} ---",
                'compare_error_folders': "Ошибка при сравнении папок: {error}",
                'compare_mismatch': "Сравниваются только файл с файлом или папка с папкой.",
                'folder_dialog_title': "Выбор файлов",
                'folder_add_selected': "Добавить выбранные",
                'folder_added_info': "Добавлено {count} файлов",
                'error_no_files': "Нет выбранных файлов",
                'error_save_as': "Сохранить как",
                'warning_select_both_paths': "Оба пути должны быть выбраны",
                'warning_select_path': "Выберите путь",
                'folder_display': "[Папка] {name}",
                'file_display': "Файл",
                'dir_display': "Папка",
                'added_title': "Добавлено",
                'tree_name': "Имя"
            },
            'en': {
                'title': "File Utility: Merge & Compare",
                'mode_merge': "Merge Files",
                'mode_compare': "Compare Files/Folders",
                'merge_files': "Files",
                'merge_folder': "Folder",
                'merge_extension': "Extension:",
                'merge_recursive': "Include Subfolders",
                'merge_add': "Add",
                'merge_remove_selected': "Remove Selected",
                'merge_split': "Split result into parts",
                'merge_split_lines': "lines",
                'merge_split_mb': "mb",
                'merge_split_suffix': "lines / mb per file",
                'merge_button': "Merge",
                'merge_file_header': "--- File: {filename} ---",
                'merge_done': "Merged into: {path}",
                'merge_error': "Failed to merge files: {error}",
                'merge_split_done_lines': "File split into {count} parts of {amount} lines each.",
                'merge_split_done_mb': "File split into {count} parts of ~{size:.2f} MB each.",
                'merge_split_error': "Error splitting file: {error}",
                'compare_choose_first': "Choose First",
                'compare_choose_second': "Choose Second",
                'compare_button': "Compare",
                'compare_identical': "Files are identical.",
                'compare_different': "Files are different.",
                'compare_error_files': "Error comparing files: {error}",
                'compare_folders_identical': "Folders are identical.",
                'compare_folders_diff_files': "Different files: {files}",
                'compare_folders_only_left': "Only in first folder: {files}",
                'compare_folders_only_right': "Only in second folder: {files}",
                'compare_subfolder': "--- Subfolder: {name} ---",
                'compare_error_folders': "Error comparing folders: {error}",
                'compare_mismatch': "Only file-to-file or folder-to-folder comparison is supported.",
                'folder_dialog_title': "Select Files",
                'folder_add_selected': "Add Selected",
                'folder_added_info': "Added {count} files",
                'error_no_files': "No files selected",
                'error_save_as': "Save As",
                'warning_select_both_paths': "Both paths must be selected",
                'warning_select_path': "Please select a path",
                'folder_display': "[Folder] {name}",
                'file_display': "File",
                'dir_display': "Folder",
                'added_title': "Added",
                'tree_name': "Name"
            }
        }

        self.root.title(self._('title'))
        self.root.geometry("900x750")
        
        self.setup_language_switch()
        self.mode_var = tk.StringVar(value='merge')
        self.setup_mode_switch()
        self.setup_merge_ui()
        self.setup_compare_ui()
        self.update_mode_ui()

    def setup_language_switch(self):
        lang_frame = tk.Frame(self.root)
        lang_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Button(lang_frame, text="RU", command=lambda: self.switch_language('ru')).pack(side=tk.RIGHT, padx=5)
        tk.Button(lang_frame, text="EN", command=lambda: self.switch_language('en')).pack(side=tk.RIGHT)

    def switch_language(self, lang):
        self.current_lang = lang
        self.update_texts()

    def _(self, key):
        """Helper method to get translated text"""
        return self.translations[self.current_lang].get(key, key)

    def update_texts(self):
        """Update all texts in the UI based on current language"""
        self.root.title(self._('title'))
        
        # Update mode switch
        if hasattr(self, 'mode_frame') and self.mode_frame.winfo_exists():
            self.mode_frame.destroy()
        self.setup_mode_switch()
        
        # Update merge UI if visible
        if hasattr(self, 'merge_frame') and self.merge_frame.winfo_exists():
            # Update controls frame
            if hasattr(self, 'merge_controls_frame'):
                for widget in self.merge_controls_frame.winfo_children():
                    widget.destroy()
                self.setup_merge_controls()
            
            # Update options frame
            if hasattr(self, 'merge_options_frame'):
                for widget in self.merge_options_frame.winfo_children():
                    widget.destroy()
                self.setup_merge_options()
                
            # Update buttons
            if hasattr(self, 'merge_remove_btn'):
                self.merge_remove_btn.config(text=self._('merge_remove_selected'))
            if hasattr(self, 'merge_btn'):
                self.merge_btn.config(text=self._('merge_button'))
        
        # Update compare UI if visible
        if hasattr(self, 'compare_frame') and self.compare_frame.winfo_exists():
            if hasattr(self, 'compare_choose1_btn'):
                self.compare_choose1_btn.config(text=self._('compare_choose_first'))
            if hasattr(self, 'compare_choose2_btn'):
                self.compare_choose2_btn.config(text=self._('compare_choose_second'))
            if hasattr(self, 'compare_btn'):
                self.compare_btn.config(text=self._('compare_button'))

    def setup_mode_switch(self):
        self.mode_frame = tk.Frame(self.root)
        self.mode_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Radiobutton(self.mode_frame, text=self._('mode_merge'), variable=self.mode_var, value='merge', command=self.update_mode_ui).pack(side=tk.LEFT)
        tk.Radiobutton(self.mode_frame, text=self._('mode_compare'), variable=self.mode_var, value='compare', command=self.update_mode_ui).pack(side=tk.LEFT)

    def update_mode_ui(self):
        if self.mode_var.get() == 'merge':
            self.merge_frame.pack(fill=tk.BOTH, expand=True)
            self.compare_frame.pack_forget()
        else:
            self.merge_frame.pack_forget()
            self.compare_frame.pack(fill=tk.BOTH, expand=True)

    def setup_merge_ui(self):
        self.merge_frame = tk.Frame(self.root)
        self.merge_controls_frame = tk.Frame(self.merge_frame)
        self.merge_controls_frame.pack(fill=tk.X, padx=10, pady=5)
        self.setup_merge_controls()
        
        self.listbox_files = tk.Listbox(self.merge_frame, selectmode=tk.EXTENDED)
        self.listbox_files.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.merge_remove_btn = tk.Button(self.merge_frame, text=self._('merge_remove_selected'), command=self.remove_selected)
        self.merge_remove_btn.pack(fill=tk.X, padx=10)
        
        self.merge_options_frame = tk.Frame(self.merge_frame)
        self.merge_options_frame.pack(fill=tk.X, padx=10, pady=(5, 0))
        self.setup_merge_options()
        
        self.merge_btn = tk.Button(self.merge_frame, text=self._('merge_button'), command=self.merge_files)
        self.merge_btn.pack(fill=tk.X, padx=10, pady=(5, 10))

    def setup_merge_controls(self):
        self.mode_files_var = tk.StringVar(value='files')
        tk.Radiobutton(self.merge_controls_frame, text=self._('merge_files'), variable=self.mode_files_var, value='files').pack(side=tk.LEFT)
        tk.Radiobutton(self.merge_controls_frame, text=self._('merge_folder'), variable=self.mode_files_var, value='folder').pack(side=tk.LEFT)
        
        self.extension_var = tk.StringVar(value="")
        tk.Label(self.merge_controls_frame, text=self._('merge_extension')).pack(side=tk.LEFT, padx=(10, 0))
        tk.Entry(self.merge_controls_frame, textvariable=self.extension_var, width=10).pack(side=tk.LEFT)
        
        self.recursive_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self.merge_controls_frame, text=self._('merge_recursive'), variable=self.recursive_var).pack(side=tk.LEFT, padx=10)
        
        tk.Button(self.merge_controls_frame, text=self._('merge_add'), command=self.select_files).pack(side=tk.RIGHT)

    def setup_merge_options(self):
        self.split_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self.merge_options_frame, text=self._('merge_split'), variable=self.split_var).pack(side=tk.LEFT)
        
        self.split_type = tk.StringVar(value='lines')
        tk.OptionMenu(self.merge_options_frame, self.split_type, self._('merge_split_lines'), self._('merge_split_mb')).pack(side=tk.LEFT)
        
        self.split_amount = tk.IntVar(value=1000)
        tk.Entry(self.merge_options_frame, textvariable=self.split_amount, width=10).pack(side=tk.LEFT)
        tk.Label(self.merge_options_frame, text=self._('merge_split_suffix')).pack(side=tk.LEFT)

    def select_files(self):
        mode = self.mode_files_var.get()
        if mode == 'files':
            files = filedialog.askopenfilenames(title=self._('warning_select_path'))
            if files:
                for file in files:
                    if file not in self.listbox_files.get(0, tk.END):
                        self.listbox_files.insert(tk.END, file)
        elif mode == 'folder':
            folder = filedialog.askdirectory(title=self._('warning_select_path'))
            if not folder:
                return
            ext = self.extension_var.get().strip()
            if ext and not ext.startswith('.'):
                ext = '.' + ext
            top = tk.Toplevel(self.root)
            top.title(self._('folder_dialog_title'))
            top.geometry("600x500")
            
            tree_frame = tk.Frame(top)
            tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            tree = ttk.Treeview(tree_frame, columns=("fullpath", "type"), show="tree")
            tree.heading("#0", text=self._('tree_name'))
            tree.column("#0", width=250)
            tree.column("fullpath", width=300)
            tree.column("type", width=50)
            
            vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=vsb.set)
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            vsb.pack(side=tk.RIGHT, fill=tk.Y)
            
            node_info = {}
            
            def insert_node(parent, path):
                basename = os.path.basename(path)
                is_dir = os.path.isdir(path)
                display_text = self._('folder_display').format(name=basename) if is_dir else basename
                node = tree.insert(parent, "end", text=display_text, values=(path, self._('dir_display') if is_dir else self._('file_display')))
                
                var = tk.BooleanVar(value=False)
                node_info[node] = {'var': var, 'path': path, 'is_dir': is_dir}
                
                if is_dir:
                    if self.recursive_var.get():
                        try:
                            for item in sorted(os.listdir(path)):
                                full = os.path.join(path, item)
                                if os.path.isdir(full) or not ext or full.endswith(ext):
                                    insert_node(node, full)
                        except PermissionError:
                            pass
                elif not ext or path.endswith(ext):
                    pass
                else:
                    tree.delete(node)
                    if node in node_info:
                        del node_info[node]
                    return
            
            insert_node('', folder)
            
            def on_tree_click(event):
                item = tree.identify_row(event.y)
                if item:
                    column = tree.identify_column(event.x)
                    if column == '#0':
                        if item in node_info:
                            current_value = node_info[item]['var'].get()
                            node_info[item]['var'].set(not current_value)
                            if node_info[item]['is_dir']:
                                self.update_children_state(tree, item, node_info, not current_value)
            
            tree.bind('<Button-1>', on_tree_click)
            
            def add_selected():
                added_count = 0
                for node_id, info in node_info.items():
                    if not info['is_dir'] and info['var'].get():
                        path = info['path']
                        if path not in self.listbox_files.get(0, tk.END):
                            self.listbox_files.insert(tk.END, path)
                            added_count += 1
                top.destroy()
                messagebox.showinfo(self._('added_title'), 
                                  self._('folder_added_info').format(count=added_count))
            
            tk.Button(top, text=self._('folder_add_selected'), command=add_selected).pack(pady=5)

    def update_children_state(self, tree, parent_node, node_info, state):
        for child in tree.get_children(parent_node):
            if child in node_info:
                node_info[child]['var'].set(state)
                if node_info[child]['is_dir']:
                    self.update_children_state(tree, child, node_info, state)

    def remove_selected(self):
        for i in reversed(self.listbox_files.curselection()):
            self.listbox_files.delete(i)

    def merge_files(self):
        files = list(self.listbox_files.get(0, tk.END))
        if not files:
            messagebox.showwarning("Error" if self.current_lang == 'en' else "Ошибка", 
                                 self._('error_no_files'))
            return
        output_path = filedialog.asksaveasfilename(title=self._('error_save_as'), defaultextension=".txt")
        if not output_path:
            return
        try:
            with open(output_path, 'w', encoding='utf-8') as out:
                for i, file in enumerate(files):
                    if i > 0:
                        out.write("\n")
                    out.write(self._('merge_file_header').format(filename=os.path.basename(file)) + "\n")
                    with open(file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        out.write(content)
            if self.split_var.get():
                if self.split_type.get() == self._('merge_split_lines') or self.split_type.get() == 'lines':
                    self.split_file_by_lines(output_path, self.split_amount.get())
                else:
                    self.split_file_by_size(output_path, self.split_amount.get() * 1024 * 1024)
            messagebox.showinfo("Done" if self.current_lang == 'en' else "Готово", 
                              self._('merge_done').format(path=output_path))
        except Exception as e:
            messagebox.showerror("Error" if self.current_lang == 'en' else "Ошибка", 
                               self._('merge_error').format(error=str(e)))

    def split_file_by_lines(self, filename, lines_per_file):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            for i in range(0, len(lines), lines_per_file):
                part_filename = f"{filename}_part{i // lines_per_file + 1}.txt"
                with open(part_filename, 'w', encoding='utf-8') as part_file:
                    part_file.writelines(lines[i:i + lines_per_file])
            messagebox.showinfo("Done" if self.current_lang == 'en' else "Готово", 
                              self._('merge_split_done_lines').format(
                                  count=((len(lines) - 1) // lines_per_file) + 1, 
                                  amount=lines_per_file))
        except Exception as e:
            messagebox.showerror("Error" if self.current_lang == 'en' else "Ошибка", 
                               self._('merge_split_error').format(error=str(e)))

    def split_file_by_size(self, filename, max_bytes):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                part = []
                size = 0
                count = 1
                for line in f:
                    line_size = len(line.encode('utf-8'))
                    if size + line_size > max_bytes and part:
                        with open(f"{filename}_part{count}.txt", 'w', encoding='utf-8') as pf:
                            pf.writelines(part)
                        count += 1
                        part = [line]
                        size = line_size
                    else:
                        part.append(line)
                        size += line_size
                if part:
                    with open(f"{filename}_part{count}.txt", 'w', encoding='utf-8') as pf:
                        pf.writelines(part)
            messagebox.showinfo("Done" if self.current_lang == 'en' else "Готово", 
                              self._('merge_split_done_mb').format(
                                  count=count, 
                                  size=max_bytes / (1024*1024)))
        except Exception as e:
            messagebox.showerror("Error" if self.current_lang == 'en' else "Ошибка", 
                               self._('merge_split_error').format(error=str(e)))

    def setup_compare_ui(self):
        self.compare_frame = tk.Frame(self.root)
        frame = tk.Frame(self.compare_frame, padx=10, pady=10)
        frame.pack(padx=10, pady=10)
        
        self.entry1 = tk.Entry(frame, width=50)
        self.entry1.grid(row=0, column=0, padx=5, pady=5)
        self.compare_choose1_btn = tk.Button(frame, text=self._('compare_choose_first'), command=lambda: self.choose_path(self.entry1))
        self.compare_choose1_btn.grid(row=0, column=1)
        
        self.entry2 = tk.Entry(frame, width=50)
        self.entry2.grid(row=1, column=0, padx=5, pady=5)
        self.compare_choose2_btn = tk.Button(frame, text=self._('compare_choose_second'), command=lambda: self.choose_path(self.entry2))
        self.compare_choose2_btn.grid(row=1, column=1)
        
        self.compare_btn = tk.Button(frame, text=self._('compare_button'), command=self.compare_paths)
        self.compare_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.result_text = tk.StringVar()
        tk.Label(frame, textvariable=self.result_text, justify=tk.LEFT, wraplength=700, 
                fg="blue").grid(row=3, column=0, columnspan=2)

    def choose_path(self, entry):
        path = filedialog.askopenfilename(title=self._('warning_select_path'))
        if not path:
            path = filedialog.askdirectory(title=self._('warning_select_path'))
        if path:
            entry.delete(0, tk.END)
            entry.insert(tk.END, path)

    def compare_paths(self):
        path1 = self.entry1.get()
        path2 = self.entry2.get()
        if not path1 or not path2:
            messagebox.showwarning("Error" if self.current_lang == 'en' else "Ошибка", 
                                 self._('warning_select_both_paths'))
            return
        if os.path.isfile(path1) and os.path.isfile(path2):
            try:
                with open(path1, 'rb') as f1, open(path2, 'rb') as f2:
                    if f1.read() == f2.read():
                        self.result_text.set(self._('compare_identical'))
                    else:
                        self.result_text.set(self._('compare_different'))
            except Exception as e:
                self.result_text.set(self._('compare_error_files').format(error=e))
        elif os.path.isdir(path1) and os.path.isdir(path2):
            try:
                dcmp = filecmp.dircmp(path1, path2)
                result = self.get_dir_diff(dcmp)
                if not result.strip():
                    self.result_text.set(self._('compare_folders_identical'))
                else:
                    self.result_text.set(result)
            except Exception as e:
                self.result_text.set(self._('compare_error_folders').format(error=e))
        else:
            self.result_text.set(self._('compare_mismatch'))

    def get_dir_diff(self, dcmp):
        output = []
        if dcmp.diff_files:
            output.append(self._('compare_folders_diff_files').format(files=', '.join(dcmp.diff_files)))
        if dcmp.left_only:
            output.append(self._('compare_folders_only_left').format(files=', '.join(dcmp.left_only)))
        if dcmp.right_only:
            output.append(self._('compare_folders_only_right').format(files=', '.join(dcmp.right_only)))
        for common_dir in dcmp.common_dirs:
            sub_dcmp = filecmp.dircmp(os.path.join(dcmp.left, common_dir), os.path.join(dcmp.right, common_dir))
            sub_result = self.get_dir_diff(sub_dcmp)
            if sub_result:
                output.append(self._('compare_subfolder').format(name=common_dir) + "\n" + sub_result)
        return "\n".join(output)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileUtilityApp(root)
    root.mainloop()
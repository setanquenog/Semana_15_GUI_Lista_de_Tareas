# ==========================
# ui/app_tkinter.py
# ==========================
import tkinter as tk
from tkinter import ttk, messagebox


class AppTareas(tk.Tk):
    def __init__(self, servicio):
        super().__init__()
        self.servicio = servicio
        self._id_seleccionado = None

        self.title("Lista de Tareas")
        self.geometry("500x400")

        self._configurar_ui()
        self._registrar_eventos()

    def _configurar_ui(self):
        frame = tk.Frame(self)
        frame.pack(pady=10)

        self.entry = tk.Entry(frame, width=40)
        self.entry.pack(side=tk.LEFT, padx=5)

        # ✅ BOTÓN VERDE (Añadir)
        self.btn_add = tk.Button(
            frame,
            text="➕ Añadir",
            bg="green",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self._agregar
        )
        self.btn_add.pack(side=tk.LEFT, padx=5)

        # ✅ BOTÓN AZUL (Completar)
        self.btn_done = tk.Button(
            self,
            text="✔ Completar",
            bg="skyblue",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self._completar
        )
        self.btn_done.pack(pady=5)

        # ✅ BOTÓN ROJO (Eliminar)
        self.btn_delete = tk.Button(
            self,
            text="🗑 Eliminar",
            bg="red",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self._eliminar
        )
        self.btn_delete.pack(pady=5)

        # 📋 TABLA
        self.tree = ttk.Treeview(self, columns=("id", "descripcion"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("descripcion", text="Tarea")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # 🎨 COLOR AZUL PARA COMPLETADAS
        self.tree.tag_configure("completado", foreground="blue")

    def _registrar_eventos(self):
        self.entry.bind("<Return>", lambda e: self._agregar())
        self.tree.bind("<<TreeviewSelect>>", self._seleccionar)
        self.tree.bind("<Double-1>", lambda e: self._completar())

    # ================= CRUD =================

    def _agregar(self):
        texto = self.entry.get()
        try:
            self.servicio.agregar_tarea(texto)
            self._actualizar_lista()
            self.entry.delete(0, tk.END)
        except ValueError as e:
            messagebox.showwarning("Error", str(e))

    def _completar(self):
        if self._id_seleccionado is None:
            messagebox.showwarning("Atención", "Seleccione una tarea")
            return

        self.servicio.completar_tarea(self._id_seleccionado)
        self._actualizar_lista()

    def _eliminar(self):
        if self._id_seleccionado is None:
            messagebox.showwarning("Atención", "Seleccione una tarea")
            return

        self.servicio.eliminar_tarea(self._id_seleccionado)
        self._actualizar_lista()

    # ================= UTIL =================

    def _actualizar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for t in self.servicio.obtener_todas():
            texto = t.descripcion

            if t.completado:
                texto += " [Hecho ✔]"
                self.tree.insert("", tk.END, values=(t.id, texto), tags=("completado",))
            else:
                self.tree.insert("", tk.END, values=(t.id, texto))

    def _seleccionar(self, event):
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            self._id_seleccionado = int(item["values"][0])
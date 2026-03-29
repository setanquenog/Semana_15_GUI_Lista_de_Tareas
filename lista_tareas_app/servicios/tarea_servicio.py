# ==========================
# servicios/tarea_servicio.py
# ==========================
from modelos.tarea import Tarea


class TareaServicio:
    def __init__(self):
        self._tareas = []
        self._contador_id = 1

    def agregar_tarea(self, descripcion: str):
        tarea = Tarea(self._contador_id, descripcion)
        self._contador_id += 1
        self._tareas.append(tarea)

    def obtener_todas(self):
        return list(self._tareas)  # 🔥 ESTE MÉTODO FALTABA

    def completar_tarea(self, id_tarea: int):
        for t in self._tareas:
            if t.id == id_tarea:
                t.completado = True
                return
        raise ValueError("Tarea no encontrada")

    def eliminar_tarea(self, id_tarea: int):
        for t in self._tareas:
            if t.id == id_tarea:
                self._tareas.remove(t)
                return
        raise ValueError("Tarea no encontrada")
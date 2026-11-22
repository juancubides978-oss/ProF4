import tkinter as tk
from tkinter import messagebox, ttk

from cliente import Cliente
from logger import registrar_error
from servicio import (
    AlquilerEquipos,
    AsesoriaEspecializada,
    ReservaSala,
)
from sistema import SistemaGestion


class AplicacionGestion:

    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Integral de Gestión - Clientes, Servicios y Reservas")
        self.root.geometry("940x620")
        self.root.minsize(820, 520)

        self.sistema = SistemaGestion()

        self._crear_interfaz()

    def _crear_interfaz(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_clientes = ttk.Frame(self.notebook, padding=10)
        self.tab_servicios = ttk.Frame(self.notebook, padding=10)
        self.tab_reservas = ttk.Frame(self.notebook, padding=10)

        self.notebook.add(self.tab_clientes, text="Clientes")
        self.notebook.add(self.tab_servicios, text="Servicios")
        self.notebook.add(self.tab_reservas, text="Reservas")

        self._construir_pestana_clientes()
        self._construir_pestana_servicios()
        self._construir_pestana_reservas()

    # ==========================================================
    # PESTAÑA 1: CLIENTES
    # ==========================================================
    def _construir_pestana_clientes(self):
        form = ttk.LabelFrame(self.tab_clientes, text="Nuevo Cliente", padding=10)
        form.pack(fill="x", pady=(0, 10))

        ttk.Label(form, text="ID:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_cli_id = ttk.Entry(form, width=12)
        self.entry_cli_id.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(form, text="Nombre:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.entry_cli_nombre = ttk.Entry(form, width=28)
        self.entry_cli_nombre.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        ttk.Label(form, text="Correo:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_cli_correo = ttk.Entry(form, width=25)
        self.entry_cli_correo.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(form, text="Teléfono:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.entry_cli_tel = ttk.Entry(form, width=20)
        self.entry_cli_tel.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        ttk.Button(
            form,
            text="Agregar Cliente",
            command=self._agregar_cliente
        ).grid(row=1, column=4, padx=10, pady=5)

        columnas = ("id", "nombre", "correo", "telefono")
        self.tree_clientes = ttk.Treeview(
            self.tab_clientes, columns=columnas, show="headings", height=12
        )
        self.tree_clientes.heading("id", text="ID")
        self.tree_clientes.heading("nombre", text="Nombre")
        self.tree_clientes.heading("correo", text="Correo")
        self.tree_clientes.heading("telefono", text="Teléfono")

        self.tree_clientes.column("id", width=70, anchor="center")
        self.tree_clientes.column("nombre", width=220)
        self.tree_clientes.column("correo", width=240)
        self.tree_clientes.column("telefono", width=150, anchor="center")

        self.tree_clientes.pack(fill="both", expand=True)

    def _agregar_cliente(self):
        try:
            cliente = Cliente(
                self.entry_cli_id.get().strip(),
                self.entry_cli_nombre.get().strip(),
                self.entry_cli_correo.get().strip(),
                self.entry_cli_tel.get().strip(),
            )
            self.sistema.agregar_cliente(cliente)
            self._refrescar_clientes()
            self._limpiar_campos_cliente()
            messagebox.showinfo("Éxito", "Cliente agregado correctamente.")
        except Exception as e:
            registrar_error(str(e))
            messagebox.showerror("Error al agregar cliente", str(e))

    def _limpiar_campos_cliente(self):
        self.entry_cli_id.delete(0, tk.END)
        self.entry_cli_nombre.delete(0, tk.END)
        self.entry_cli_correo.delete(0, tk.END)
        self.entry_cli_tel.delete(0, tk.END)

    def _refrescar_clientes(self):
        for fila in self.tree_clientes.get_children():
            self.tree_clientes.delete(fila)

        for cli in self.sistema.clientes:
            self.tree_clientes.insert(
                "",
                tk.END,
                values=(
                    cli.get_id_cliente(),
                    cli.get_nombre(),
                    cli.get_correo(),
                    cli.get_telefono(),
                ),
            )

        self._actualizar_combos_reservas()

    # ==========================================================
    # PESTAÑA 2: SERVICIOS
    # ==========================================================
    def _construir_pestana_servicios(self):
        form = ttk.LabelFrame(self.tab_servicios, text="Nuevo Servicio", padding=10)
        form.pack(fill="x", pady=(0, 10))

        ttk.Label(form, text="Tipo:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.combo_tipo_srv = ttk.Combobox(
            form,
            state="readonly",
            width=22,
            values=["ReservaSala", "AlquilerEquipos", "AsesoriaEspecializada"],
        )
        self.combo_tipo_srv.set("ReservaSala")
        self.combo_tipo_srv.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.combo_tipo_srv.bind("<<ComboboxSelected>>", self._actualizar_etiqueta_parametro)

        ttk.Label(form, text="ID:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.entry_srv_id = ttk.Entry(form, width=14)
        self.entry_srv_id.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        ttk.Label(form, text="Nombre:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_srv_nombre = ttk.Entry(form, width=25)
        self.entry_srv_nombre.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(form, text="Tarifa/Costo base:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.entry_srv_costo = ttk.Entry(form, width=14)
        self.entry_srv_costo.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        self.label_srv_extra = ttk.Label(form, text="Capacidad (entero):")
        self.label_srv_extra.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_srv_extra = ttk.Entry(form, width=14)
        self.entry_srv_extra.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Button(
            form,
            text="Agregar Servicio",
            command=self._agregar_servicio
        ).grid(row=2, column=3, padx=10, pady=5)

        columnas = ("id", "tipo", "nombre", "tarifa", "detalle")
        self.tree_servicios = ttk.Treeview(
            self.tab_servicios, columns=columnas, show="headings", height=12
        )
        self.tree_servicios.heading("id", text="ID")
        self.tree_servicios.heading("tipo", text="Tipo")
        self.tree_servicios.heading("nombre", text="Nombre")
        self.tree_servicios.heading("tarifa", text="Tarifa")
        self.tree_servicios.heading("detalle", text="Parámetro / Info")

        self.tree_servicios.column("id", width=80, anchor="center")
        self.tree_servicios.column("tipo", width=180)
        self.tree_servicios.column("nombre", width=200)
        self.tree_servicios.column("tarifa", width=100, anchor="e")
        self.tree_servicios.column("detalle", width=220)

        self.tree_servicios.pack(fill="both", expand=True)

    def _actualizar_etiqueta_parametro(self, event=None):
        tipo = self.combo_tipo_srv.get()
        if tipo == "ReservaSala":
            self.label_srv_extra.config(text="Capacidad (entero):")
        elif tipo == "AlquilerEquipos":
            self.label_srv_extra.config(text="Cantidad equipos:")
        else:
            self.label_srv_extra.config(text="Horas asesoría:")

    def _agregar_servicio(self):
        try:
            tipo = self.combo_tipo_srv.get()
            id_srv = self.entry_srv_id.get().strip()
            nombre = self.entry_srv_nombre.get().strip()

            costo_raw = self.entry_srv_costo.get().strip()
            extra_raw = self.entry_srv_extra.get().strip()

            if not costo_raw or not extra_raw:
                raise ValueError("Debes completar la tarifa/costo y el parámetro adicional.")

            costo = float(costo_raw)

            if tipo == "ReservaSala":
                capacidad = int(extra_raw)
                servicio = ReservaSala(id_srv, nombre, costo, capacidad)
            elif tipo == "AlquilerEquipos":
                cantidad = int(extra_raw)
                servicio = AlquilerEquipos(id_srv, nombre, costo, cantidad)
            else:
                horas = int(extra_raw)
                servicio = AsesoriaEspecializada(id_srv, nombre, costo, horas)

            self.sistema.agregar_servicio(servicio)
            self._refrescar_servicios()
            self._limpiar_campos_servicio()
            messagebox.showinfo("Éxito", "Servicio agregado correctamente.")
        except Exception as e:
            registrar_error(str(e))
            messagebox.showerror("Error al agregar servicio", str(e))

    def _limpiar_campos_servicio(self):
        self.entry_srv_id.delete(0, tk.END)
        self.entry_srv_nombre.delete(0, tk.END)
        self.entry_srv_costo.delete(0, tk.END)
        self.entry_srv_extra.delete(0, tk.END)

    def _refrescar_servicios(self):
        for fila in self.tree_servicios.get_children():
            self.tree_servicios.delete(fila)

        for srv in self.sistema.servicios:
            tipo = type(srv).__name__
            if isinstance(srv, ReservaSala):
                tarifa = srv.costo_hora
                detalle = f"Capacidad: {srv.capacidad}"
            elif isinstance(srv, AlquilerEquipos):
                tarifa = srv.costo_dia
                detalle = f"Cantidad: {srv.cantidad}"
            else:
                tarifa = srv.tarifa_hora
                detalle = f"Horas: {srv.horas}"

            self.tree_servicios.insert(
                "",
                tk.END,
                values=(srv.id_servicio, tipo, srv.nombre, tarifa, detalle),
            )

        self._actualizar_combos_reservas()

    # ==========================================================
    # PESTAÑA 3: RESERVAS
    # ==========================================================
    def _construir_pestana_reservas(self):
        form = ttk.LabelFrame(self.tab_reservas, text="Nueva Reserva", padding=10)
        form.pack(fill="x", pady=(0, 10))

        ttk.Label(form, text="Cliente:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.combo_res_cliente = ttk.Combobox(form, state="readonly", width=28)
        self.combo_res_cliente.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(form, text="Servicio:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.combo_res_servicio = ttk.Combobox(form, state="readonly", width=28)
        self.combo_res_servicio.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        ttk.Label(form, text="Duración:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_res_duracion = ttk.Entry(form, width=12)
        self.entry_res_duracion.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(form, text="Fecha (AAAA-MM-DD):").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.entry_res_fecha = ttk.Entry(form, width=16)
        self.entry_res_fecha.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        ttk.Button(
            form,
            text="Crear Reserva",
            command=self._crear_reserva
        ).grid(row=1, column=4, padx=10, pady=5)

        columnas = ("idx", "cliente", "servicio", "duracion", "fecha", "estado")
        self.tree_reservas = ttk.Treeview(
            self.tab_reservas, columns=columnas, show="headings", height=10
        )
        self.tree_reservas.heading("idx", text="#")
        self.tree_reservas.heading("cliente", text="Cliente")
        self.tree_reservas.heading("servicio", text="Servicio")
        self.tree_reservas.heading("duracion", text="Duración")
        self.tree_reservas.heading("fecha", text="Fecha")
        self.tree_reservas.heading("estado", text="Estado")

        self.tree_reservas.column("idx", width=45, anchor="center")
        self.tree_reservas.column("cliente", width=180)
        self.tree_reservas.column("servicio", width=190)
        self.tree_reservas.column("duracion", width=80, anchor="center")
        self.tree_reservas.column("fecha", width=110, anchor="center")
        self.tree_reservas.column("estado", width=110, anchor="center")

        self.tree_reservas.pack(fill="both", expand=True)

        acciones = ttk.Frame(self.tab_reservas, padding=(0, 8))
        acciones.pack(fill="x")

        ttk.Button(acciones, text="Confirmar", command=self._confirmar_reserva).pack(side="left", padx=4)
        ttk.Button(acciones, text="Procesar", command=self._procesar_reserva).pack(side="left", padx=4)
        ttk.Button(acciones, text="Cancelar", command=self._cancelar_reserva).pack(side="left", padx=4)
        ttk.Button(acciones, text="Calcular Total", command=self._calcular_total_reserva).pack(side="left", padx=4)
        ttk.Button(acciones, text="Ver Detalle", command=self._ver_detalle_reserva).pack(side="left", padx=4)

    def _actualizar_combos_reservas(self):
        if hasattr(self, "combo_res_cliente"):
            self.combo_res_cliente["values"] = [
                f"{c.get_id_cliente()} - {c.get_nombre()}" for c in self.sistema.clientes
            ]
        if hasattr(self, "combo_res_servicio"):
            self.combo_res_servicio["values"] = [
                f"{s.id_servicio} - {s.nombre}" for s in self.sistema.servicios
            ]

    def _obtener_reserva_seleccionada(self):
        seleccion = self.tree_reservas.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona una reserva de la tabla.")
            return None
        indice = self.tree_reservas.index(seleccion[0])
        return self.sistema.reservas[indice]

    def _crear_reserva(self):
        try:
            idx_cli = self.combo_res_cliente.current()
            idx_srv = self.combo_res_servicio.current()
            if idx_cli < 0 or idx_srv < 0:
                raise ValueError("Debes seleccionar un cliente y un servicio.")

            duracion_raw = self.entry_res_duracion.get().strip()
            if not duracion_raw:
                raise ValueError("Debes ingresar una duración.")

            cliente = self.sistema.clientes[idx_cli]
            servicio = self.sistema.servicios[idx_srv]
            duracion = int(duracion_raw)
            fecha = self.entry_res_fecha.get().strip()

            self.sistema.crear_reserva(cliente, servicio, duracion, fecha)
            self._refrescar_reservas()
            self.entry_res_duracion.delete(0, tk.END)
            self.entry_res_fecha.delete(0, tk.END)
            messagebox.showinfo("Éxito", "Reserva creada en estado Pendiente.")
        except Exception as e:
            registrar_error(str(e))
            messagebox.showerror("Error al crear reserva", str(e))

    def _confirmar_reserva(self):
        res = self._obtener_reserva_seleccionada()
        if not res:
            return
        try:
            res.confirmar()
            self._refrescar_reservas()
            messagebox.showinfo("Reserva confirmada", "La reserva ahora está Confirmada.")
        except Exception as e:
            registrar_error(str(e))
            messagebox.showerror("Error", str(e))

    def _procesar_reserva(self):
        res = self._obtener_reserva_seleccionada()
        if not res:
            return
        try:
            res.procesar()
            self._refrescar_reservas()
            messagebox.showinfo("Reserva procesada", "La reserva ahora está Procesada.")
        except Exception as e:
            registrar_error(str(e))
            messagebox.showerror("Error", str(e))

    def _cancelar_reserva(self):
        res = self._obtener_reserva_seleccionada()
        if not res:
            return
        try:
            res.cancelar()
            self._refrescar_reservas()
            messagebox.showinfo("Reserva cancelada", "La reserva ha sido Cancelada.")
        except Exception as e:
            registrar_error(str(e))
            messagebox.showerror("Error", str(e))

    def _calcular_total_reserva(self):
        res = self._obtener_reserva_seleccionada()
        if not res:
            return
        try:
            total = res.calcular_total()
            messagebox.showinfo("Total de reserva", f"Total calculado: ${total}")
        except Exception as e:
            registrar_error(str(e))
            messagebox.showerror("Error al calcular total", str(e))

    def _ver_detalle_reserva(self):
        res = self._obtener_reserva_seleccionada()
        if not res:
            return
        messagebox.showinfo("Detalle de reserva", res.mostrar_detalle())

    def _refrescar_reservas(self):
        for fila in self.tree_reservas.get_children():
            self.tree_reservas.delete(fila)

        for i, res in enumerate(self.sistema.reservas, start=1):
            self.tree_reservas.insert(
                "",
                tk.END,
                values=(
                    i,
                    res.cliente.get_nombre(),
                    res.servicio.nombre,
                    res.duracion,
                    res.fecha,
                    res.estado,
                ),
            )


def main():
    root = tk.Tk()
    app = AplicacionGestion(root)
    root.mainloop()


if __name__ == "__main__":
    main()

import inspect
import re
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

TIPOS_SERVICIO_ETIQUETAS = {
    "ReservaSala": "Reserva de Sala",
    "AlquilerEquipos": "Alquiler de Equipos",
    "AsesoriaEspecializada": "Asesoría Especializada",
}

ETIQUETAS_A_TIPO_SERVICIO = {v: k for k, v in TIPOS_SERVICIO_ETIQUETAS.items()}

UNIDADES_TIEMPO = ["horas", "minutos", "días"]

# Porcentajes sugeridos editables por tipo de servicio (IVA %, Descuento %)
CONDICIONES_POR_TIPO_SERVICIO = {
    "ReservaSala": {"iva": 19.0, "descuento": 0.0},
    "AlquilerEquipos": {"iva": 19.0, "descuento": 5.0},
    "AsesoriaEspecializada": {"iva": 19.0, "descuento": 10.0},
}


class AplicacionGestion:

    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Integral de Gestión - Clientes, Servicios y Reservas")
        self.root.geometry("980x670")
        self.root.minsize(850, 560)

        self.sistema = SistemaGestion()
        self.meta_reservas = []

        style = ttk.Style()
        if "clam" in style.theme_names():
            style.theme_use("clam")

        self._crear_interfaz()

    def _crear_interfaz(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_clientes = ttk.Frame(self.notebook, padding=10)
        self.tab_servicios = ttk.Frame(self.notebook, padding=10)
        self.tab_reservas = ttk.Frame(self.notebook, padding=10)

        self.notebook.add(self.tab_clientes, text="👥 Clientes")
        self.notebook.add(self.tab_servicios, text="🛠️ Servicios")
        self.notebook.add(self.tab_reservas, text="📅 Reservas")

        self._construir_pestana_clientes()
        self._construir_pestana_servicios()
        self._construir_pestana_reservas()

    # ==========================================================
    # PESTAÑA 1: CLIENTES
    # ==========================================================
    def _construir_pestana_clientes(self):
        form = ttk.LabelFrame(self.tab_clientes, text=" Registrar Nuevo Cliente ", padding=10)
        form.pack(fill="x", padx=6, pady=(0, 10))

        ttk.Label(form, text="ID:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_cli_id = ttk.Entry(form, width=14)
        self.entry_cli_id.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(form, text="Nombre completo:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.entry_cli_nombre = ttk.Entry(form, width=30)
        self.entry_cli_nombre.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        ttk.Label(form, text="Correo electrónico:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_cli_correo = ttk.Entry(form, width=26)
        self.entry_cli_correo.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(form, text="Teléfono:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.entry_cli_tel = ttk.Entry(form, width=22)
        self.entry_cli_tel.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        frame_btn_cli = ttk.Frame(form)
        frame_btn_cli.grid(row=2, column=0, columnspan=4, pady=(8, 2))
        ttk.Button(
            frame_btn_cli,
            text="Guardar Cliente",
            command=self._agregar_cliente
        ).pack(side="left", padx=5)
        ttk.Button(
            frame_btn_cli,
            text="Limpiar Campos",
            command=self._limpiar_campos_cliente
        ).pack(side="left", padx=5)

        frame_tabla = ttk.LabelFrame(self.tab_clientes, text=" Clientes Registrados ", padding=6)
        frame_tabla.pack(fill="both", expand=True, padx=6, pady=4)

        columnas = ("id", "nombre", "correo", "telefono")
        self.tree_clientes = ttk.Treeview(
            frame_tabla, columns=columnas, show="headings", height=11
        )
        self.tree_clientes.heading("id", text="ID")
        self.tree_clientes.heading("nombre", text="Nombre")
        self.tree_clientes.heading("correo", text="Correo")
        self.tree_clientes.heading("telefono", text="Teléfono")

        self.tree_clientes.column("id", width=80, anchor="center")
        self.tree_clientes.column("nombre", width=220)
        self.tree_clientes.column("correo", width=240)
        self.tree_clientes.column("telefono", width=150, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree_clientes.yview)
        self.tree_clientes.configure(yscrollcommand=scrollbar.set)

        self.tree_clientes.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

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
        form = ttk.LabelFrame(self.tab_servicios, text=" Registrar Nuevo Servicio ", padding=10)
        form.pack(fill="x", padx=6, pady=(0, 10))

        ttk.Label(form, text="Tipo de servicio:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.combo_tipo_srv = ttk.Combobox(
            form,
            state="readonly",
            width=24,
            values=list(TIPOS_SERVICIO_ETIQUETAS.values()),
        )
        self.combo_tipo_srv.set("Reserva de Sala")
        self.combo_tipo_srv.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.combo_tipo_srv.bind("<<ComboboxSelected>>", self._actualizar_etiqueta_parametro)

        ttk.Label(form, text="Referencia / Nombre (opcional):").grid(
            row=0, column=2, padx=5, pady=5, sticky="w"
        )
        self.entry_srv_nombre = ttk.Entry(form, width=28)
        self.entry_srv_nombre.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        ttk.Label(form, text="Tarifa / Costo base ($):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_srv_costo = ttk.Entry(form, width=16)
        self.entry_srv_costo.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.label_srv_extra = ttk.Label(form, text="Capacidad (entero):")
        self.label_srv_extra.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.entry_srv_extra = ttk.Entry(form, width=16)
        self.entry_srv_extra.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        frame_btn_srv = ttk.Frame(form)
        frame_btn_srv.grid(row=2, column=0, columnspan=4, pady=(8, 2))
        ttk.Button(
            frame_btn_srv,
            text="Registrar Servicio",
            command=self._agregar_servicio
        ).pack(side="left", padx=5)
        ttk.Button(
            frame_btn_srv,
            text="Limpiar Campos",
            command=self._limpiar_campos_servicio
        ).pack(side="left", padx=5)

        frame_tabla = ttk.LabelFrame(self.tab_servicios, text=" Servicios Disponibles ", padding=6)
        frame_tabla.pack(fill="both", expand=True, padx=6, pady=4)

        columnas = ("id", "tipo", "nombre", "tarifa", "detalle")
        self.tree_servicios = ttk.Treeview(
            frame_tabla, columns=columnas, show="headings", height=11
        )
        self.tree_servicios.heading("id", text="Código")
        self.tree_servicios.heading("tipo", text="Tipo de servicio")
        self.tree_servicios.heading("nombre", text="Referencia / Nombre")
        self.tree_servicios.heading("tarifa", text="Tarifa")
        self.tree_servicios.heading("detalle", text="Parámetro / Info")

        self.tree_servicios.column("id", width=90, anchor="center")
        self.tree_servicios.column("tipo", width=180)
        self.tree_servicios.column("nombre", width=220)
        self.tree_servicios.column("tarifa", width=110, anchor="e")
        self.tree_servicios.column("detalle", width=220)

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree_servicios.yview)
        self.tree_servicios.configure(yscrollcommand=scrollbar.set)

        self.tree_servicios.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _obtener_tipo_interno(self):
        etiqueta = self.combo_tipo_srv.get()
        return ETIQUETAS_A_TIPO_SERVICIO.get(etiqueta, etiqueta)

    def _generar_id_servicio(self):
        siguiente = len(self.sistema.servicios) + 1
        return f"SRV-{siguiente:03d}"

    def _resolver_nombre_servicio(self, tipo_interno, nombre_escrito, valor_extra):
        limpio = (nombre_escrito or "").strip()
        if limpio:
            return limpio
        if tipo_interno == "ReservaSala":
            return f"Sala ({valor_extra} personas)"
        if tipo_interno == "AlquilerEquipos":
            return f"Equipos (x{valor_extra})"
        return f"Asesoría ({valor_extra} h)"

    def _texto_legible_servicio(self, srv):
        tipo_interno = type(srv).__name__
        etiqueta_tipo = TIPOS_SERVICIO_ETIQUETAS.get(tipo_interno, tipo_interno)
        id_srv = getattr(srv, "id_servicio", "")
        nombre_srv = getattr(srv, "nombre", "") or etiqueta_tipo
        if id_srv:
            return f"{id_srv} - {nombre_srv}"
        return nombre_srv

    def _actualizar_etiqueta_parametro(self, event=None):
        tipo = self._obtener_tipo_interno()
        if tipo == "ReservaSala":
            self.label_srv_extra.config(text="Capacidad (entero):")
        elif tipo == "AlquilerEquipos":
            self.label_srv_extra.config(text="Cantidad equipos:")
        else:
            self.label_srv_extra.config(text="Horas asesoría:")

    def _agregar_servicio(self):
        try:
            tipo = self._obtener_tipo_interno()
            nombre_escrito = self.entry_srv_nombre.get().strip()

            costo_raw = self.entry_srv_costo.get().strip()
            extra_raw = self.entry_srv_extra.get().strip()

            if not costo_raw or not extra_raw:
                raise ValueError("Debes completar la tarifa/costo y el parámetro adicional.")

            costo = float(costo_raw)
            id_srv = self._generar_id_servicio()

            if tipo == "ReservaSala":
                capacidad = int(extra_raw)
                nombre = self._resolver_nombre_servicio(tipo, nombre_escrito, capacidad)
                servicio = ReservaSala(id_srv, nombre, costo, capacidad)
            elif tipo == "AlquilerEquipos":
                cantidad = int(extra_raw)
                nombre = self._resolver_nombre_servicio(tipo, nombre_escrito, cantidad)
                servicio = AlquilerEquipos(id_srv, nombre, costo, cantidad)
            else:
                horas = int(extra_raw)
                nombre = self._resolver_nombre_servicio(tipo, nombre_escrito, horas)
                servicio = AsesoriaEspecializada(id_srv, nombre, costo, horas)

            self.sistema.agregar_servicio(servicio)
            self._refrescar_servicios()
            self._limpiar_campos_servicio()
            messagebox.showinfo("Éxito", f"Servicio agregado como '{servicio.nombre}'.")
        except Exception as e:
            registrar_error(str(e))
            messagebox.showerror("Error al agregar servicio", str(e))

    def _limpiar_campos_servicio(self):
        self.entry_srv_nombre.delete(0, tk.END)
        self.entry_srv_costo.delete(0, tk.END)
        self.entry_srv_extra.delete(0, tk.END)

    def _refrescar_servicios(self):
        for fila in self.tree_servicios.get_children():
            self.tree_servicios.delete(fila)

        for srv in self.sistema.servicios:
            tipo_interno = type(srv).__name__
            tipo_etiqueta = TIPOS_SERVICIO_ETIQUETAS.get(tipo_interno, tipo_interno)
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
                values=(srv.id_servicio, tipo_etiqueta, srv.nombre, tarifa, detalle),
            )

        self._actualizar_combos_reservas()

    # ==========================================================
    # PESTAÑA 3: RESERVAS
    # ==========================================================
    def _construir_pestana_reservas(self):
        form = ttk.LabelFrame(self.tab_reservas, text=" Gestión y Procesamiento de Reservas ", padding=10)
        form.pack(fill="x", padx=6, pady=(0, 10))

        ttk.Label(form, text="Cliente:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.combo_res_cliente = ttk.Combobox(form, state="readonly", width=28)
        self.combo_res_cliente.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(form, text="Servicio:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.combo_res_servicio = ttk.Combobox(form, state="readonly", width=34)
        self.combo_res_servicio.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        self.combo_res_servicio.bind("<<ComboboxSelected>>", self._cargar_porcentajes_servicio_seleccionado)

        ttk.Label(form, text="Tiempo:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        frame_tiempo = ttk.Frame(form)
        frame_tiempo.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.entry_res_duracion = ttk.Entry(frame_tiempo, width=10)
        self.entry_res_duracion.pack(side="left", padx=(0, 6))

        self.combo_res_unidad = ttk.Combobox(
            frame_tiempo,
            state="readonly",
            width=11,
            values=UNIDADES_TIEMPO,
        )
        self.combo_res_unidad.set("horas")
        self.combo_res_unidad.pack(side="left")

        ttk.Label(form, text="Fecha y Hora:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        frame_fecha_hora = ttk.Frame(form)
        frame_fecha_hora.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        self.entry_res_fecha = ttk.Entry(frame_fecha_hora, width=12)
        self.entry_res_fecha.pack(side="left", padx=(0, 6))

        ttk.Label(frame_fecha_hora, text="Hora (HH:MM):").pack(side="left", padx=(0, 4))
        self.entry_res_hora = ttk.Entry(frame_fecha_hora, width=7)
        self.entry_res_hora.insert(0, "08:00")
        self.entry_res_hora.pack(side="left")

        ttk.Label(form, text="Aumento / IVA (%):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_res_iva = ttk.Entry(form, width=12)
        self.entry_res_iva.insert(0, "19")
        self.entry_res_iva.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(form, text="Descuento (%):").grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.entry_res_descuento = ttk.Entry(form, width=12)
        self.entry_res_descuento.insert(0, "0")
        self.entry_res_descuento.grid(row=2, column=3, padx=5, pady=5, sticky="w")

        frame_botones = ttk.Frame(form)
        frame_botones.grid(row=3, column=0, columnspan=4, pady=(10, 2))

        ttk.Button(frame_botones, text="Crear Reserva", command=self._crear_reserva).pack(side="left", padx=4)
        ttk.Button(frame_botones, text="Confirmar", command=self._confirmar_reserva).pack(side="left", padx=4)
        ttk.Button(frame_botones, text="Procesar", command=self._procesar_reserva).pack(side="left", padx=4)
        ttk.Button(frame_botones, text="Cancelar", command=self._cancelar_reserva).pack(side="left", padx=4)
        ttk.Button(frame_botones, text="Calcular Total", command=self._calcular_total_reserva).pack(side="left", padx=4)
        ttk.Button(frame_botones, text="Ver Detalle", command=self._ver_detalle_reserva).pack(side="left", padx=4)

        frame_tabla = ttk.LabelFrame(self.tab_reservas, text=" Listado de Reservas ", padding=6)
        frame_tabla.pack(fill="both", expand=True, padx=6, pady=4)

        columnas = ("idx", "cliente", "servicio", "duracion", "fecha", "estado")
        self.tree_reservas = ttk.Treeview(
            frame_tabla, columns=columnas, show="headings", height=9
        )
        self.tree_reservas.heading("idx", text="#")
        self.tree_reservas.heading("cliente", text="Cliente")
        self.tree_reservas.heading("servicio", text="Servicio")
        self.tree_reservas.heading("duracion", text="Tiempo")
        self.tree_reservas.heading("fecha", text="Fecha / Hora")
        self.tree_reservas.heading("estado", text="Estado")

        self.tree_reservas.column("idx", width=45, anchor="center")
        self.tree_reservas.column("cliente", width=180)
        self.tree_reservas.column("servicio", width=230)
        self.tree_reservas.column("duracion", width=110, anchor="center")
        self.tree_reservas.column("fecha", width=145, anchor="center")
        self.tree_reservas.column("estado", width=110, anchor="center")

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree_reservas.yview)
        self.tree_reservas.configure(yscrollcommand=scrollbar.set)

        self.tree_reservas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _cargar_porcentajes_servicio_seleccionado(self, event=None):
        idx_srv = self.combo_res_servicio.current()
        if idx_srv < 0 or idx_srv >= len(self.sistema.servicios):
            return
        srv = self.sistema.servicios[idx_srv]
        tipo_interno = type(srv).__name__
        condiciones = CONDICIONES_POR_TIPO_SERVICIO.get(
            tipo_interno, {"iva": 0.0, "descuento": 0.0}
        )
        self.entry_res_iva.delete(0, tk.END)
        self.entry_res_iva.insert(0, f"{condiciones['iva']:g}")

        self.entry_res_descuento.delete(0, tk.END)
        self.entry_res_descuento.insert(0, f"{condiciones['descuento']:g}")

    def _formatear_duracion_legible(self, valor, unidad):
        if float(valor).is_integer():
            valor_fmt = str(int(float(valor)))
        else:
            valor_fmt = f"{float(valor):g}"

        if unidad == "horas":
            etiqueta = "hora" if float(valor) == 1 else "horas"
        elif unidad == "minutos":
            etiqueta = "minuto" if float(valor) == 1 else "minutos"
        else:
            etiqueta = "día" if float(valor) == 1 else "días"

        return f"{valor_fmt} {etiqueta}"

    def _convertir_a_horas(self, valor, unidad):
        if unidad == "horas":
            horas = float(valor)
        elif unidad == "minutos":
            horas = float(valor) / 60.0
        else:
            horas = float(valor) * 24.0

        if horas.is_integer():
            return int(horas)
        return round(horas, 4)

    def _validar_y_formatear_hora(self, hora_raw):
        limpia = (hora_raw or "").strip()
        if not limpia:
            return "08:00"
        if not re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d$", limpia):
            raise ValueError("La hora debe tener formato HH:MM (ej. 08:00 o 14:30).")
        return limpia

    def _leer_porcentajes_economicos(self):
        iva_raw = self.entry_res_iva.get().strip().replace(",", ".") or "0"
        desc_raw = self.entry_res_descuento.get().strip().replace(",", ".") or "0"
        iva = float(iva_raw)
        descuento = float(desc_raw)
        if not (0 <= iva <= 100):
            raise ValueError("El porcentaje de aumento / IVA debe estar entre 0 y 100.")
        if not (0 <= descuento <= 100):
            raise ValueError("El porcentaje de descuento debe estar entre 0 y 100.")
        return iva, descuento

    def _aplicar_iva_y_descuento(self, subtotal, iva_pct, desc_pct):
        con_descuento = float(subtotal) * (1.0 - (desc_pct / 100.0))
        total = con_descuento * (1.0 + (iva_pct / 100.0))
        return round(total, 2)

    def _actualizar_combos_reservas(self):
        if hasattr(self, "combo_res_cliente"):
            self.combo_res_cliente["values"] = [
                f"{c.get_id_cliente()} - {c.get_nombre()}" for c in self.sistema.clientes
            ]
            if self.combo_res_cliente.current() < 0 and self.sistema.clientes:
                self.combo_res_cliente.current(0)

        if hasattr(self, "combo_res_servicio"):
            seleccion_anterior = self.combo_res_servicio.current()
            self.combo_res_servicio["values"] = [
                self._texto_legible_servicio(s) for s in self.sistema.servicios
            ]
            if self.sistema.servicios:
                if seleccion_anterior < 0:
                    self.combo_res_servicio.current(0)
                    self._cargar_porcentajes_servicio_seleccionado()

    def _obtener_reserva_seleccionada(self):
        seleccion = self.tree_reservas.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona una reserva de la tabla.")
            return None
        indice = self.tree_reservas.index(seleccion[0])
        return self.sistema.reservas[indice]

    def _obtener_info_tiempo_reserva(self, res):
        try:
            idx = self.sistema.reservas.index(res)
        except ValueError:
            idx = -1

        if 0 <= idx < len(self.meta_reservas):
            meta = self.meta_reservas[idx]
            tiempo_str = self._formatear_duracion_legible(meta["valor"], meta["unidad"])
            hora_str = meta.get("hora", "")
        else:
            tiempo_str = self._formatear_duracion_legible(res.duracion, "horas")
            hora_str = ""

        return tiempo_str, hora_str

    def _crear_reserva(self):
        try:
            idx_cli = self.combo_res_cliente.current()
            idx_srv = self.combo_res_servicio.current()
            if idx_cli < 0 or idx_srv < 0:
                raise ValueError("Debes seleccionar un cliente y un servicio.")

            duracion_raw = self.entry_res_duracion.get().strip().replace(",", ".")
            if not duracion_raw:
                raise ValueError("Debes ingresar una duración o tiempo.")

            valor_tiempo = float(duracion_raw)
            if valor_tiempo <= 0:
                raise ValueError("El tiempo debe ser mayor que cero.")

            unidad = self.combo_res_unidad.get() or "horas"
            duracion_backend = self._convertir_a_horas(valor_tiempo, unidad)

            cliente = self.sistema.clientes[idx_cli]
            servicio = self.sistema.servicios[idx_srv]
            fecha = self.entry_res_fecha.get().strip()
            hora = self._validar_y_formatear_hora(self.entry_res_hora.get())

            self.sistema.crear_reserva(cliente, servicio, duracion_backend, fecha)
            self.meta_reservas.append({
                "valor": valor_tiempo,
                "unidad": unidad,
                "hora": hora,
            })

            self._refrescar_reservas()
            self.entry_res_duracion.delete(0, tk.END)
            self.entry_res_fecha.delete(0, tk.END)
            tiempo_texto = self._formatear_duracion_legible(valor_tiempo, unidad)
            messagebox.showinfo(
                "Éxito",
                f"Reserva creada ({tiempo_texto}, hora {hora}) en estado Pendiente."
            )
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
            iva_pct, desc_pct = self._leer_porcentajes_economicos()
            firma = inspect.signature(res.calcular_total)
            params = firma.parameters

            if "impuesto" in params and "descuento" in params:
                total = res.calcular_total(impuesto=iva_pct, descuento=desc_pct)
                mensaje = (
                    f"Aumento / IVA aplicado: {iva_pct:g}%\n"
                    f"Descuento aplicado: {desc_pct:g}%\n"
                    f"Total calculado: ${total}"
                )
            else:
                subtotal = res.calcular_total()
                total = self._aplicar_iva_y_descuento(subtotal, iva_pct, desc_pct)
                mensaje = (
                    f"Subtotal base: ${subtotal}\n"
                    f"Descuento: {desc_pct:g}%\n"
                    f"Aumento / IVA: {iva_pct:g}%\n"
                    f"Total final: ${total}"
                )

            tiempo_str, hora_str = self._obtener_info_tiempo_reserva(res)
            if tiempo_str:
                mensaje += f"\nTiempo: {tiempo_str}"
            if hora_str:
                mensaje += f"\nHora de reserva: {hora_str}"

            messagebox.showinfo("Total de reserva", mensaje)
        except Exception as e:
            if e.__cause__:
                detalle = e.__cause__
            else:
                detalle = e
            print("ERROR REAL:", repr(detalle))
            registrar_error(f"{str(e)} | Causa: {detalle}")
            messagebox.showerror("Error al calcular total", f"{e}\n\ndetalle: {detalle}")

    def _ver_detalle_reserva(self):
        res = self._obtener_reserva_seleccionada()
        if not res:
            return
        tiempo_str, hora_str = self._obtener_info_tiempo_reserva(res)
        detalle = res.mostrar_detalle()
        if tiempo_str:
            detalle += f"\nTiempo: {tiempo_str}"
        if hora_str:
            detalle += f"\nHora: {hora_str}"
        messagebox.showinfo("Detalle de reserva", detalle)

    def _refrescar_reservas(self):
        for fila in self.tree_reservas.get_children():
            self.tree_reservas.delete(fila)

        for i, res in enumerate(self.sistema.reservas, start=1):
            tiempo_str, hora_str = self._obtener_info_tiempo_reserva(res)
            fecha_hora_str = f"{res.fecha} {hora_str}".strip()

            self.tree_reservas.insert(
                "",
                tk.END,
                values=(
                    i,
                    res.cliente.get_nombre(),
                    self._texto_legible_servicio(res.servicio),
                    tiempo_str,
                    fecha_hora_str,
                    res.estado,
                ),
            )


def main():
    root = tk.Tk()
    app = AplicacionGestion(root)
    root.mainloop()


if __name__ == "__main__":
    main()

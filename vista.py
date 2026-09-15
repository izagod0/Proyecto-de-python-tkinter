import tkinter as tk
from tkinter import ttk, messagebox


class VistaHotel:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Reservaciones - Hotel")
        self.root.geometry("1150x720")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True, fill='both')

        # 1. Crear los Frames para las 4 pestañas
        self.frame_habitaciones = ttk.Frame(self.notebook)
        self.frame_clientes = ttk.Frame(self.notebook)
        self.frame_reservaciones = ttk.Frame(self.notebook)
        self.frame_historial = ttk.Frame(self.notebook)

        self.notebook.add(self.frame_habitaciones, text='Habitaciones')
        self.notebook.add(self.frame_clientes, text='Clientes')
        self.notebook.add(self.frame_reservaciones, text='Reservaciones')
        self.notebook.add(self.frame_historial, text='Historial')

        # 2. Llamar a los constructores de cada pestaña
        self.crear_pestana_habitaciones()
        self.crear_pestana_clientes()
        self.crear_pestana_reservaciones()
        self.crear_pestana_historial()

    # ==========================================
    # PESTAÑA HABITACIONES
    # ==========================================
    def crear_pestana_habitaciones(self):
        # --- Tabla ---
        frame_tabla = tk.Frame(self.frame_habitaciones)
        frame_tabla.pack(pady=10, padx=20, fill="x")
        tk.Label(frame_tabla, text="Listado de Habitaciones",
                 font=("Arial", 12, "bold")).pack()

        self.tree_hab = ttk.Treeview(frame_tabla, columns=("ID", "Numero", "Estado"),
                                     show="headings")
        self.tree_hab.heading("ID", text="Habitacion ID")
        self.tree_hab.heading("Numero", text="Número")
        self.tree_hab.heading("Estado", text="Estado")
        self.tree_hab.pack(fill="x", pady=10)

        # --- Formulario ---
        frame_form = tk.LabelFrame(self.frame_habitaciones, text="Agregar/Editar Habitación")
        frame_form.pack(pady=10, padx=20, fill="x")

        tk.Label(frame_form, text="Habitacion ID:").grid(row=0, column=0, padx=10, pady=10)
        self.entry_id_hab = tk.Entry(frame_form, width=15, state="readonly")
        self.entry_id_hab.grid(row=0, column=1)

        tk.Label(frame_form, text="Numero:").grid(row=0, column=2, padx=10, pady=10)
        self.entry_numero_hab = tk.Entry(frame_form, width=15)
        self.entry_numero_hab.grid(row=0, column=3)

        tk.Label(frame_form, text="Estado:").grid(row=0, column=4, padx=10, pady=10)
        self.combo_estado = ttk.Combobox(frame_form, values=["Libre", "Reservado", "Cancelado"],
                                         state="readonly", width=12)
        self.combo_estado.current(0)
        self.combo_estado.grid(row=0, column=5)

        # --- Botones ---
        self.btn_nueva_hab = tk.Button(frame_form, text="Agregar", width=10)
        self.btn_nueva_hab.grid(row=0, column=6, padx=5)

        self.btn_editar_hab = tk.Button(frame_form, text="Editar", width=10)
        self.btn_editar_hab.grid(row=0, column=7, padx=5)

        self.btn_eliminar_hab = tk.Button(frame_form, text="Eliminar", width=10)
        self.btn_eliminar_hab.grid(row=0, column=8, padx=5)

    def limpiar_form_habitacion(self):
        """Limpia el formulario de habitaciones."""
        self.entry_id_hab.config(state="normal")
        self.entry_id_hab.delete(0, tk.END)
        self.entry_id_hab.config(state="readonly")
        self.entry_numero_hab.delete(0, tk.END)
        self.combo_estado.current(0)

    # ==========================================
    # PESTAÑA CLIENTES
    # ==========================================
    def crear_pestana_clientes(self):
        # --- Tabla ---
        frame_tabla = tk.Frame(self.frame_clientes)
        frame_tabla.pack(pady=10, padx=20, fill="x")
        tk.Label(frame_tabla, text="Listado de Clientes y Hospedaje",
                 font=("Arial", 12, "bold")).pack()

        self.tree_clientes = ttk.Treeview(
            frame_tabla,
            columns=("ID", "Nombre", "Direccion", "Email", "Telefono", "Hospedado_En"),
            show="headings"
        )
        self.tree_clientes.heading("ID", text="ID")
        self.tree_clientes.heading("Nombre", text="Nombre")
        self.tree_clientes.heading("Direccion", text="Dirección")
        self.tree_clientes.heading("Email", text="Email")
        self.tree_clientes.heading("Telefono", text="Teléfono")
        self.tree_clientes.heading("Hospedado_En", text="Hospedado En")

        # Anchos de columna
        self.tree_clientes.column("ID", width=50, anchor="center")
        self.tree_clientes.column("Nombre", width=130)
        self.tree_clientes.column("Direccion", width=150)
        self.tree_clientes.column("Email", width=160)
        self.tree_clientes.column("Telefono", width=100, anchor="center")
        self.tree_clientes.column("Hospedado_En", width=110, anchor="center")

        # Scroll horizontal
        scroll_x = ttk.Scrollbar(frame_tabla, orient="horizontal",
                                 command=self.tree_clientes.xview)
        self.tree_clientes.configure(xscrollcommand=scroll_x.set)
        scroll_x.pack(fill="x")

        self.tree_clientes.pack(fill="x", pady=10)

        # --- Formulario ---
        frame_form = tk.LabelFrame(self.frame_clientes, text="Registro de Cliente")
        frame_form.pack(pady=10, padx=20, fill="x")

        tk.Label(frame_form, text="ID:").grid(row=0, column=0, pady=5, sticky="e")
        self.entry_id_cliente = tk.Entry(frame_form, state="readonly")
        self.entry_id_cliente.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(frame_form, text="Nombre:").grid(row=0, column=2, pady=5, sticky="e")
        self.entry_nombre = tk.Entry(frame_form)
        self.entry_nombre.grid(row=0, column=3, pady=5, padx=5)

        tk.Label(frame_form, text="Dirección:").grid(row=1, column=0, pady=5, sticky="e")
        self.entry_direccion = tk.Entry(frame_form)
        self.entry_direccion.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(frame_form, text="Email:").grid(row=1, column=2, pady=5, sticky="e")
        self.entry_email = tk.Entry(frame_form)
        self.entry_email.grid(row=1, column=3, pady=5, padx=5)

        tk.Label(frame_form, text="Teléfono:").grid(row=2, column=0, pady=5, sticky="e")
        self.entry_telefono = tk.Entry(frame_form)
        self.entry_telefono.grid(row=2, column=1, pady=5, padx=5)

        self.btn_salvar = tk.Button(frame_form, text="Salvar Cliente")
        self.btn_salvar.grid(row=2, column=2, pady=10, padx=5)

        self.btn_editar_cliente = tk.Button(frame_form, text="Editar Cliente")
        self.btn_editar_cliente.grid(row=2, column=3, pady=10, padx=5)

        self.btn_nuevo_cliente = tk.Button(frame_form, text="Nuevo Cliente",
                                           command=self.limpiar_form_cliente)
        self.btn_nuevo_cliente.grid(row=3, column=0, columnspan=4, pady=5)

    def limpiar_form_cliente(self):
        """Limpia el formulario de clientes para ingresar uno nuevo."""
        for entry in [self.entry_id_cliente, self.entry_nombre, self.entry_direccion,
                      self.entry_email, self.entry_telefono]:
            entry.config(state="normal")
            entry.delete(0, tk.END)
        self.entry_id_cliente.config(state="readonly")

    # ==========================================
    # PESTAÑA RESERVACIONES
    # ==========================================
    def crear_pestana_reservaciones(self):
        # --- Tabla ---
        frame_tabla = tk.Frame(self.frame_reservaciones)
        frame_tabla.pack(pady=10, padx=20, fill="x")
        tk.Label(frame_tabla, text="Reservaciones Activas",
                 font=("Arial", 12, "bold")).pack()

        self.tree_res = ttk.Treeview(frame_tabla,
                                     columns=("ResID", "Cliente", "Habitacion", "Salida"),
                                     show="headings")
        self.tree_res.heading("ResID", text="ID Reserva")
        self.tree_res.heading("Cliente", text="Cliente")
        self.tree_res.heading("Habitacion", text="Habitación")
        self.tree_res.heading("Salida", text="Fecha Salida")
        self.tree_res.pack(fill="x", pady=10)

        # --- Formulario ---
        frame_res = tk.Frame(self.frame_reservaciones)
        frame_res.pack(pady=10)

        tk.Label(frame_res, text="Gestión de Reservación",
                 font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(frame_res, text="ReservacionID:").grid(row=1, column=0, sticky="e", pady=5, padx=5)
        self.entry_res_id = tk.Entry(frame_res, width=30, state="readonly")
        self.entry_res_id.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(frame_res, text="Seleccionar Cliente:").grid(row=2, column=0, sticky="e", pady=5, padx=5)
        self.combo_res_cliente = ttk.Combobox(frame_res, width=27, state="readonly")
        self.combo_res_cliente.grid(row=2, column=1, pady=5, padx=5)

        tk.Label(frame_res, text="Habitaciones Disponibles:").grid(row=3, column=0, sticky="e", pady=5, padx=5)
        self.combo_res_hab = ttk.Combobox(frame_res, width=27, state="readonly")
        self.combo_res_hab.grid(row=3, column=1, pady=5, padx=5)

        tk.Label(frame_res, text="Fecha Reservación:").grid(row=4, column=0, sticky="e", pady=5, padx=5)
        self.entry_res_fecha = tk.Entry(frame_res, width=30)
        self.entry_res_fecha.grid(row=4, column=1, pady=5, padx=5)

        tk.Label(frame_res, text="Hora Reservación:").grid(row=5, column=0, sticky="e", pady=5, padx=5)
        self.entry_res_hora = tk.Entry(frame_res, width=30)
        self.entry_res_hora.grid(row=5, column=1, pady=5, padx=5)

        tk.Label(frame_res, text="Fecha Salida:").grid(row=6, column=0, sticky="e", pady=5, padx=5)
        self.entry_res_salida = tk.Entry(frame_res, width=30)
        self.entry_res_salida.grid(row=6, column=1, pady=5, padx=5)

        tk.Label(frame_res, text="Costo:").grid(row=7, column=0, sticky="e", pady=5, padx=5)
        self.entry_res_costo = tk.Entry(frame_res, width=30)
        self.entry_res_costo.grid(row=7, column=1, pady=5, padx=5)

        # Botones
        self.btn_reservar = tk.Button(frame_res, text="Confirmar Reservación", width=20)
        self.btn_reservar.grid(row=8, column=0, pady=20)

        self.btn_editar_res = tk.Button(frame_res, text="Editar Reservación", width=20)
        self.btn_editar_res.grid(row=8, column=1, pady=20)

        self.btn_nueva_res = tk.Button(frame_res, text="Nueva Reservación", width=20,
                                       command=self.limpiar_form_reservacion)
        self.btn_nueva_res.grid(row=9, column=0, columnspan=2, pady=5)

    def limpiar_form_reservacion(self):
        """Limpia el formulario de reservaciones."""
        for entry in [self.entry_res_id, self.entry_res_fecha, self.entry_res_hora,
                      self.entry_res_salida, self.entry_res_costo]:
            entry.config(state="normal")
            entry.delete(0, tk.END)
        self.entry_res_id.config(state="readonly")
        self.combo_res_cliente.set("")
        self.combo_res_hab.set("")

    # ==========================================
    # PESTAÑA HISTORIAL
    # ==========================================
    def crear_pestana_historial(self):
        frame_tabla = tk.Frame(self.frame_historial)
        frame_tabla.pack(pady=10, padx=20, fill="both", expand=True)

        tk.Label(frame_tabla, text="Registro de Movimientos del Sistema",
                 font=("Arial", 12, "bold")).pack()

        self.tree_historial = ttk.Treeview(frame_tabla, columns=("Fecha", "Movimiento"),
                                           show="headings")
        self.tree_historial.heading("Fecha", text="Fecha y Hora")
        self.tree_historial.heading("Movimiento", text="Acción Realizada")

        self.tree_historial.column("Fecha", width=150)
        self.tree_historial.column("Movimiento", width=600)

        self.tree_historial.pack(fill="both", expand=True, pady=10)

    # ==========================================
    # MENSAJES
    # ==========================================
    def mostrar_mensaje(self, titulo, mensaje, tipo="info"):
        if tipo == "info":
            messagebox.showinfo(titulo, mensaje)
        elif tipo == "error":
            messagebox.showerror(titulo, mensaje)
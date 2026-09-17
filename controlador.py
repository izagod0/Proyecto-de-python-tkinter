import modelo
from vista import VistaHotel
import tkinter as tk
from datetime import datetime


class ControladorHotel:
    def __init__(self, root):
        self.vista = VistaHotel(root)

        # --- Conexiones HABITACIONES ---
        self.vista.tree_hab.bind("<ButtonRelease-1>", self.seleccionar_habitacion)
        self.vista.btn_editar_hab.config(command=self.editar_habitacion)
        self.vista.btn_eliminar_hab.config(command=self.eliminar_habitacion)
        self.vista.btn_nueva_hab.config(command=self.salvar_habitacion)

        # --- Conexiones CLIENTES ---
        self.vista.tree_clientes.bind("<ButtonRelease-1>", self.seleccionar_cliente)
        self.vista.btn_salvar.config(command=self.salvar_cliente)
        self.vista.btn_editar_cliente.config(command=self.editar_cliente)

        # --- Conexiones RESERVACIONES ---
        self.vista.tree_res.bind("<ButtonRelease-1>", self.seleccionar_reservacion)
        self.vista.btn_reservar.config(command=self.confirmar_reservacion)
        self.vista.btn_editar_res.config(command=self.editar_reservacion)

        # Cargar todos los datos en las tablas al abrir el programa
        self.limpiar_reservaciones_inactivas()
        self.actualizar_tabla_historial()
        self.actualizar_tabla_habitaciones()
        self.actualizar_tabla_clientes()
        self.actualizar_listas_reservacion()
        self.actualizar_tabla_reservaciones()

    # ==========================================
    # FUNCIONES AUXILIARES DE VALIDACIÓN Y LIMPIEZA
    # ==========================================
    def limpiar_reservaciones_inactivas(self):
        """
        Elimina reservaciones activas si la fecha de salida ya expiró
        o si la habitación asociada cambió a estado 'Libre' o 'Cancelado'.
        """
        reservaciones = modelo.obtener_reservaciones()
        if not reservaciones:
            return

        habitaciones = {h[0]: h[2] for h in modelo.obtener_habitaciones()}
        hoy = datetime.now().date()
        formatos = ["%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d"]

        for res in reservaciones:
            res_id = res[0]
            cliente = res[1]
            hab_str = res[2]
            salida_str = res[5]

            hab_id = hab_str.split(" - ")[0].strip() if " - " in hab_str else hab_str

            # 1. Si la habitación asociada ya no está en estado 'Reservado'
            estado_hab = habitaciones.get(hab_id, "Libre")
            if estado_hab.lower() != "reservado":
                modelo.eliminar_registro(modelo.ARCHIVO_RESERVACIONES, res_id)
                modelo.registrar_movimiento(
                    f"SISTEMA: Reservación #{res_id} de '{cliente}' eliminada de activas (Habitación {hab_id} en estado '{estado_hab}')."
                )
                continue

            # 2. Si la fecha de salida ya pasó (expiró)
            f_sal = None
            for fmt in formatos:
                try:
                    f_sal = datetime.strptime(salida_str.strip(), fmt).date()
                    break
                except ValueError:
                    pass

            if f_sal and f_sal < hoy:
                modelo.eliminar_registro(modelo.ARCHIVO_RESERVACIONES, res_id)
                numero_hab = hab_str.split("Hab: ")[1].strip() if "Hab: " in hab_str else ""
                modelo.editar_habitacion(hab_id, numero_hab, "Libre")
                modelo.registrar_movimiento(
                    f"SISTEMA: Reservación #{res_id} finalizada por fecha de salida cumplida ({salida_str}). Habitación {hab_id} liberada."
                )

    def _validar_costo(self, costo_str):
        """Valida que el costo no esté vacío, no sea negativo y no tenga más de un punto decimal."""
        costo_str = costo_str.strip()
        if not costo_str:
            return False, "El costo no puede estar vacío."

        if costo_str.count('.') > 1:
            return False, "El costo no puede contener más de un punto decimal."

        try:
            val = float(costo_str)
            if val < 0:
                return False, "El costo no puede ser un número negativo."
        except ValueError:
            return False, "El costo debe ser un número válido."

        return True, ""

    def _validar_fechas(self, fecha_res_str, fecha_sal_str):
        """Valida formato de fechas y asegura que la fecha de salida sea posterior a la de entrada."""
        formatos = ["%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d"]
        f_res, f_sal = None, None

        for fmt in formatos:
            if not f_res:
                try:
                    f_res = datetime.strptime(fecha_res_str.strip(), fmt)
                except ValueError:
                    pass
            if not f_sal:
                try:
                    f_sal = datetime.strptime(fecha_sal_str.strip(), fmt)
                except ValueError:
                    pass

        if not f_res or not f_sal:
            return False, "Formato de fecha inválido. Usa el formato DD-MM-AAAA."

        if f_sal <= f_res:
            return False, "La fecha de salida debe ser posterior a la fecha de reservación."

        return True, ""

    # ==========================================
    # ACTUALIZAR INTERFAZ
    # ==========================================
    def actualizar_tabla_historial(self):
        for item in self.vista.tree_historial.get_children():
            self.vista.tree_historial.delete(item)
        for mov in modelo.obtener_historial():
            if len(mov) >= 2:
                self.vista.tree_historial.insert("", tk.END, values=(mov[0], mov[1]))

    def actualizar_tabla_habitaciones(self):
        for item in self.vista.tree_hab.get_children():
            self.vista.tree_hab.delete(item)
        for hab in modelo.obtener_habitaciones():
            self.vista.tree_hab.insert("", tk.END, values=(hab[0], hab[1], hab[2]))

    def actualizar_tabla_clientes(self):
        for item in self.vista.tree_clientes.get_children():
            self.vista.tree_clientes.delete(item)

        clientes = modelo.obtener_clientes()
        reservaciones = modelo.obtener_reservaciones()

        hospedajes = {}
        for res in reservaciones:
            id_cliente_res = res[1].split(" - ")[0].strip()
            hospedajes[id_cliente_res] = res[2]

        for cli in clientes:
            id_cliente = cli[0].strip()
            estado_hospedaje = hospedajes.get(id_cliente, "Ninguna")
            self.vista.tree_clientes.insert(
                "", tk.END,
                values=(cli[0], cli[1], cli[2], cli[3], cli[4], estado_hospedaje)
            )

    def actualizar_tabla_reservaciones(self):
        self.limpiar_reservaciones_inactivas()
        for item in self.vista.tree_res.get_children():
            self.vista.tree_res.delete(item)
        for res in modelo.obtener_reservaciones():
            self.vista.tree_res.insert("", tk.END,
                                       values=(res[0], res[1], res[2], res[5]))

    def actualizar_listas_reservacion(self):
        clientes = modelo.obtener_clientes()
        lista_clientes = [f"{c[0]} - {c[1]}" for c in clientes]
        self.vista.combo_res_cliente['values'] = lista_clientes

        habs_libres = modelo.obtener_habitaciones_libres()
        lista_habs = [f"{h[0]} - Hab: {h[1]}" for h in habs_libres]
        self.vista.combo_res_hab['values'] = lista_habs

    # ==========================================
    # HABITACIONES
    # ==========================================
    def seleccionar_habitacion(self, event):
        item_seleccionado = self.vista.tree_hab.focus()
        if not item_seleccionado:
            return
        valores = self.vista.tree_hab.item(item_seleccionado, 'values')

        self.vista.entry_id_hab.config(state="normal")
        self.vista.entry_id_hab.delete(0, tk.END)
        self.vista.entry_id_hab.insert(0, valores[0])
        self.vista.entry_id_hab.config(state="readonly")

        self.vista.entry_numero_hab.delete(0, tk.END)
        self.vista.entry_numero_hab.insert(0, valores[1])

        self.vista.combo_estado.set(valores[2])

    def salvar_habitacion(self):
        hab_id = modelo.generar_id_habitacion()
        numero = self.vista.entry_numero_hab.get()
        estado = self.vista.combo_estado.get()

        if not numero:
            self.vista.mostrar_mensaje("Error", "El Número de habitación es obligatorio", "error")
            return

        if modelo.guardar_habitacion(hab_id, numero, estado):
            modelo.registrar_movimiento(
                f"AGREGÓ: Nueva habitación '{numero}' (ID {hab_id}) en estado '{estado}'")
            self.vista.mostrar_mensaje("Éxito", f"Habitación registrada con ID {hab_id}")
            self.vista.limpiar_form_habitacion()
            self.actualizar_tabla_habitaciones()
            self.actualizar_listas_reservacion()
            self.actualizar_tabla_historial()

    def editar_habitacion(self):
        hab_id = self.vista.entry_id_hab.get()
        numero = self.vista.entry_numero_hab.get()
        estado = self.vista.combo_estado.get()

        if not hab_id:
            self.vista.mostrar_mensaje("Error", "Seleccione una habitación de la tabla", "error")
            return

        if modelo.editar_habitacion(hab_id, numero, estado):
            modelo.registrar_movimiento(
                f"EDITÓ: Habitación '{hab_id}' cambió a número '{numero}', estado '{estado}'")
            self.vista.mostrar_mensaje("Éxito", "Habitación actualizada.")
            self.vista.limpiar_form_habitacion()
            self.actualizar_tabla_habitaciones()
            self.actualizar_tabla_reservaciones()
            self.actualizar_tabla_clientes()
            self.actualizar_listas_reservacion()
            self.actualizar_tabla_historial()

    def eliminar_habitacion(self):
        hab_id = self.vista.entry_id_hab.get()
        if not hab_id:
            self.vista.mostrar_mensaje("Error", "Seleccione una habitación de la tabla", "error")
            return

        if modelo.eliminar_registro(modelo.ARCHIVO_HABITACIONES, hab_id):
            modelo.registrar_movimiento(f"ELIMINÓ: Habitación '{hab_id}' borrada del sistema.")
            self.vista.limpiar_form_habitacion()
            self.vista.mostrar_mensaje("Éxito", "Habitación eliminada.")
            self.actualizar_tabla_habitaciones()
            self.actualizar_tabla_reservaciones()
            self.actualizar_tabla_clientes()
            self.actualizar_listas_reservacion()
            self.actualizar_tabla_historial()

    # ==========================================
    # CLIENTES
    # ==========================================
    def seleccionar_cliente(self, event):
        item = self.vista.tree_clientes.focus()
        if not item:
            return
        valores = self.vista.tree_clientes.item(item, 'values')

        self.vista.entry_id_cliente.config(state="normal")
        self.vista.entry_id_cliente.delete(0, tk.END)
        self.vista.entry_id_cliente.insert(0, valores[0])
        self.vista.entry_id_cliente.config(state="readonly")

        self.vista.entry_nombre.delete(0, tk.END)
        self.vista.entry_nombre.insert(0, valores[1])

        self.vista.entry_direccion.delete(0, tk.END)
        self.vista.entry_direccion.insert(0, valores[2])

        self.vista.entry_email.delete(0, tk.END)
        self.vista.entry_email.insert(0, valores[3])

        self.vista.entry_telefono.delete(0, tk.END)
        self.vista.entry_telefono.insert(0, valores[4])

    def salvar_cliente(self):
        cliente_id = modelo.generar_id_cliente()
        nombre = self.vista.entry_nombre.get()
        direccion = self.vista.entry_direccion.get()
        email = self.vista.entry_email.get()
        telefono = self.vista.entry_telefono.get()

        if not nombre:
            self.vista.mostrar_mensaje("Error", "El Nombre es obligatorio", "error")
            return

        if modelo.guardar_cliente(cliente_id, nombre, direccion, email, telefono):
            modelo.registrar_movimiento(
                f"AGREGÓ: Nuevo cliente '{nombre}' con ID '{cliente_id}'")
            self.vista.mostrar_mensaje("Éxito", f"Cliente guardado con ID {cliente_id}")
            self.vista.limpiar_form_cliente()
            self.actualizar_tabla_clientes()
            self.actualizar_listas_reservacion()
            self.actualizar_tabla_historial()

    def editar_cliente(self):
        cliente_id = self.vista.entry_id_cliente.get()
        nombre = self.vista.entry_nombre.get()
        direccion = self.vista.entry_direccion.get()
        email = self.vista.entry_email.get()
        telefono = self.vista.entry_telefono.get()

        if not cliente_id:
            self.vista.mostrar_mensaje("Error", "Seleccione un cliente de la tabla", "error")
            return

        if not nombre:
            self.vista.mostrar_mensaje("Error", "El Nombre es obligatorio", "error")
            return

        if modelo.editar_cliente(cliente_id, nombre, direccion, email, telefono):
            modelo.registrar_movimiento(
                f"EDITÓ: Cliente '{cliente_id} - {nombre}'")
            self.vista.mostrar_mensaje("Éxito", "Cliente actualizado.")
            self.vista.limpiar_form_cliente()
            self.actualizar_tabla_clientes()
            self.actualizar_tabla_historial()
            self.actualizar_listas_reservacion()

    # ==========================================
    # RESERVACIONES
    # ==========================================
    def seleccionar_reservacion(self, event):
        item = self.vista.tree_res.focus()
        if not item:
            return
        valores = self.vista.tree_res.item(item, 'values')
        res_id = valores[0]

        reserva = modelo.buscar_reservacion_por_id(res_id)
        if not reserva:
            return

        self.vista.entry_res_id.config(state="normal")
        self.vista.entry_res_id.delete(0, tk.END)
        self.vista.entry_res_id.insert(0, reserva["id"])
        self.vista.entry_res_id.config(state="readonly")

        self.vista.combo_res_cliente.set(reserva["cliente"])

        habs_libres = modelo.obtener_habitaciones_libres()
        lista_habs = [f"{h[0]} - Hab: {h[1]}" for h in habs_libres]
        if reserva["habitacion"] not in lista_habs:
            lista_habs.append(reserva["habitacion"])
        self.vista.combo_res_hab['values'] = lista_habs
        self.vista.combo_res_hab.set(reserva["habitacion"])

        for entry, valor in [
            (self.vista.entry_res_fecha, reserva["fecha"]),
            (self.vista.entry_res_hora, reserva["hora"]),
            (self.vista.entry_res_salida, reserva["salida"]),
            (self.vista.entry_res_costo, reserva["costo"]),
        ]:
            entry.delete(0, tk.END)
            entry.insert(0, valor)

    def confirmar_reservacion(self):
        res_id = modelo.generar_id_reservacion()
        cliente_seleccionado = self.vista.combo_res_cliente.get()
        hab_seleccionada = self.vista.combo_res_hab.get()
        fecha = self.vista.entry_res_fecha.get()
        hora = self.vista.entry_res_hora.get()
        salida = self.vista.entry_res_salida.get()
        costo = self.vista.entry_res_costo.get()

        if not cliente_seleccionado or not hab_seleccionada:
            self.vista.mostrar_mensaje("Error", "Faltan datos clave para reservar", "error")
            return

        # 1. Validar que el cliente no tenga ya una reservación activa (1 persona = 1 habitación)
        id_cliente_nuevo = cliente_seleccionado.split(" - ")[0].strip()
        for res in modelo.obtener_reservaciones():
            id_cliente_existente = res[1].split(" - ")[0].strip()
            if id_cliente_nuevo == id_cliente_existente:
                self.vista.mostrar_mensaje("Cliente ocupado", "Este cliente ya tiene una reservación activa.", "error")
                return

        # 2. Validaciones de fecha y costo
        valido_fecha, msg_fecha = self._validar_fechas(fecha, salida)
        if not valido_fecha:
            self.vista.mostrar_mensaje("Error en fechas", msg_fecha, "error")
            return

        valido_costo, msg_costo = self._validar_costo(costo)
        if not valido_costo:
            self.vista.mostrar_mensaje("Error en costo", msg_costo, "error")
            return

        hab_id = hab_seleccionada.split(" - ")[0].strip()
        numero_hab = hab_seleccionada.split("Hab: ")[1].strip()

        libres = [h[0] for h in modelo.obtener_habitaciones_libres()]
        if hab_id not in libres:
            self.vista.mostrar_mensaje("Error", "Esta habitación ya fue ocupada.", "error")
            return

        modelo.guardar_reservacion(res_id, cliente_seleccionado, hab_seleccionada,
                                   fecha, hora, salida, costo)
        modelo.editar_habitacion(hab_id, numero_hab, "Reservado")
        modelo.registrar_movimiento(
            f"RESERVÓ: Cliente '{cliente_seleccionado}' ocupó la habitación '{hab_id}'.")

        self.vista.mostrar_mensaje("Éxito", f"Reservación #{res_id} confirmada.")
        self.vista.limpiar_form_reservacion()

        self.actualizar_tabla_habitaciones()
        self.actualizar_listas_reservacion()
        self.actualizar_tabla_clientes()
        self.actualizar_tabla_reservaciones()
        self.actualizar_tabla_historial()

    def editar_reservacion(self):
        res_id = self.vista.entry_res_id.get()
        cliente = self.vista.combo_res_cliente.get()
        hab = self.vista.combo_res_hab.get()
        fecha = self.vista.entry_res_fecha.get()
        hora = self.vista.entry_res_hora.get()
        salida = self.vista.entry_res_salida.get()
        costo = self.vista.entry_res_costo.get()

        if not res_id:
            self.vista.mostrar_mensaje("Error", "Seleccione una reservación de la tabla", "error")
            return

        if not cliente or not hab:
            self.vista.mostrar_mensaje("Error", "Cliente y Habitación son obligatorios", "error")
            return

        # 1. Validar que el cliente no tenga otra reservación activa distinta a la actual
        id_cliente_nuevo = cliente.split(" - ")[0].strip()
        for res in modelo.obtener_reservaciones():
            if res[0] != res_id:
                id_cliente_existente = res[1].split(" - ")[0].strip()
                if id_cliente_nuevo == id_cliente_existente:
                    self.vista.mostrar_mensaje("Cliente ocupado", "Este cliente ya tiene otra reservación activa.", "error")
                    return

        # 2. Validaciones de fecha y costo
        valido_fecha, msg_fecha = self._validar_fechas(fecha, salida)
        if not valido_fecha:
            self.vista.mostrar_mensaje("Error en fechas", msg_fecha, "error")
            return

        valido_costo, msg_costo = self._validar_costo(costo)
        if not valido_costo:
            self.vista.mostrar_mensaje("Error en costo", msg_costo, "error")
            return

        if modelo.editar_reservacion(res_id, cliente, hab, fecha, hora, salida, costo):
            modelo.registrar_movimiento(
                f"EDITÓ: Reservación '{res_id}' del cliente '{cliente}'")
            self.vista.mostrar_mensaje("Éxito", "Reservación actualizada.")
            self.vista.limpiar_form_reservacion()
            self.actualizar_tabla_reservaciones()
            self.actualizar_tabla_historial()
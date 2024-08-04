import json

class CuentaBancaria:
    def __init__(self, numero_cuenta, saldo_inicial, titular):
        self.numero_cuenta = numero_cuenta
        self.saldo = saldo_inicial
        self.titular = titular

    def depositar(self, cantidad):
        #Método para depositar una cantidad de dinero en la cuenta.
        try:
            cantidad = float(cantidad)
            if cantidad <= 0:
                raise ValueError("La cantidad a depositar debe ser positiva.")
            self.saldo += cantidad
            print(f"Depositado: ${cantidad}. Nuevo saldo: ${self.saldo}.")
        except ValueError as e:
            print(e)

    def retirar(self, cantidad):
        #Método para retirar una cantidad de dinero de la cuenta.
        try:
            cantidad = float(cantidad)
            if cantidad <= 0:
                raise ValueError("La cantidad a retirar debe ser positiva.")
            if cantidad > self.saldo:
                raise ValueError("Fondos insuficientes.")
            self.saldo -= cantidad
            print(f"Retirado: ${cantidad}. Nuevo saldo: ${self.saldo}.")
        except ValueError as e:
            print(e)

    def consultar_saldo(self):
        #Método para consultar el saldo de la cuenta.
        return self.saldo

    def to_dict(self):
        #Convierte la cuenta a un diccionario para serialización.
        return {
            'numero_cuenta': self.numero_cuenta,
            'saldo': self.saldo,
            'titular': self.titular
        }

    def __str__(self):
        return (f"Cuenta Bancaria\n"
                f"Titular: {self.titular}\n"
                f"Número de cuenta: {self.numero_cuenta}\n"
                f"Saldo: ${self.saldo}")


class CuentaBancariaCorriente(CuentaBancaria):
    def __init__(self, numero_cuenta, saldo_inicial, titular, descubierto_autorizado):
        super().__init__(numero_cuenta, saldo_inicial, titular)
        self.descubierto_autorizado = descubierto_autorizado

    def retirar(self, cantidad):
        #Método para retirar una cantidad de dinero, considerando el descubierto autorizado.
        try:
            cantidad = float(cantidad)
            if cantidad <= 0:
                raise ValueError("La cantidad a retirar debe ser positiva.")
            if cantidad > (self.saldo + self.descubierto_autorizado):
                raise ValueError("Fondos insuficientes, incluso con descubierto autorizado.")
            self.saldo -= cantidad
            print(f"Retirado: ${cantidad}. Nuevo saldo: ${self.saldo}.")
        except ValueError as e:
            print(e)

    def consultar_descubierto(self):
        #Método para consultar el límite de descubierto autorizado.
        return self.descubierto_autorizado

    def ajustar_descubierto(self, nuevo_limite):
        #Método para ajustar el límite de descubierto autorizado.
        try:
            nuevo_limite = float(nuevo_limite)
            if nuevo_limite < 0:
                raise ValueError("El límite de descubierto no puede ser negativo.")
            self.descubierto_autorizado = nuevo_limite
            print(f"Nuevo límite de descubierto autorizado: ${self.descubierto_autorizado}.")
        except ValueError as e:
            print(e)

    def to_dict(self):
        #Convierte la cuenta corriente a un diccionario para serialización.
        return {
            **super().to_dict(),
            'descubierto_autorizado': self.descubierto_autorizado
        }

    def __str__(self):
        return (super().__str__() + 
                f"\nDescubierto autorizado: ${self.descubierto_autorizado}")


class CuentaBancariaAhorro(CuentaBancaria):
    def __init__(self, numero_cuenta, saldo_inicial, titular, tasa_interes):
        super().__init__(numero_cuenta, saldo_inicial, titular)
        self.tasa_interes = tasa_interes

    def aplicar_intereses(self):
        #Método para aplicar intereses al saldo de la cuenta.
        try:
            interes = self.saldo * (self.tasa_interes / 100)
            self.saldo += interes
            print(f"Intereses aplicados: ${interes}. Nuevo saldo: ${self.saldo}.")
        except Exception as e:
            print(f"Error al aplicar intereses: {e}")

    def consultar_tasa_interes(self):
        #Método para consultar la tasa de interés.
        return self.tasa_interes

    def to_dict(self):
        #Convierte la cuenta de ahorro a un diccionario para serialización.
        return {
            **super().to_dict(),
            'tasa_interes': self.tasa_interes
        }

    def __str__(self):
        return (super().__str__() + 
                f"\nTasa de interés: {self.tasa_interes}%")

class GestorCuentas:
    def __init__(self):
        self.cuentas = {}

    def crear_cuenta(self, tipo, numero_cuenta, saldo_inicial, titular, *args):
        #Método para crear una nueva cuenta bancaria.
        try:
            if numero_cuenta in self.cuentas:
                raise ValueError("La cuenta ya existe.")
            
            saldo_inicial = float(saldo_inicial)
            if saldo_inicial < 0:
                raise ValueError("El saldo inicial no puede ser negativo.")
            
            if tipo == 'corriente':
                if len(args) != 1:
                    raise ValueError("Faltan argumentos para el tipo de cuenta corriente.")
                descubierto_autorizado = float(args[0])
                if descubierto_autorizado < 0:
                    raise ValueError("El descubierto autorizado no puede ser negativo.")
                cuenta = CuentaBancariaCorriente(numero_cuenta, saldo_inicial, titular, descubierto_autorizado)
            elif tipo == 'ahorro':
                if len(args) != 1:
                    raise ValueError("Faltan argumentos para el tipo de cuenta de ahorro.")
                tasa_interes = float(args[0])
                if tasa_interes < 0:
                    raise ValueError("La tasa de interés no puede ser negativa.")
                cuenta = CuentaBancariaAhorro(numero_cuenta, saldo_inicial, titular, tasa_interes)
            else:
                raise ValueError("Tipo de cuenta no válido.")
            
            self.cuentas[numero_cuenta] = cuenta
            print(f"Cuenta {tipo} creada con éxito.")
        except ValueError as e:
            print(e)

    def leer_cuenta(self, numero_cuenta):
        #Método para leer la información de una cuenta bancaria.
        cuenta = self.cuentas.get(numero_cuenta)
        if cuenta:
            print(cuenta)
        else:
            print("Cuenta no encontrada.")

    def actualizar_cuenta(self, numero_cuenta, **kwargs):
        #Método para actualizar detalles de una cuenta bancaria.
        try:
            cuenta = self.cuentas.get(numero_cuenta)
            if not cuenta:
                raise ValueError("Cuenta no encontrada.")
            
            for clave, valor in kwargs.items():
                if clave == 'saldo':
                    valor = float(valor)
                    if valor < 0:
                        raise ValueError("El saldo no puede ser negativo.")
                    cuenta.saldo = valor
                elif clave == 'descubierto_autorizado' and isinstance(cuenta, CuentaBancariaCorriente):
                    valor = float(valor)
                    if valor < 0:
                        raise ValueError("El límite de descubierto no puede ser negativo.")
                    cuenta.descubierto_autorizado = valor
                elif clave == 'tasa_interes' and isinstance(cuenta, CuentaBancariaAhorro):
                    valor = float(valor)
                    if valor < 0:
                        raise ValueError("La tasa de interés no puede ser negativa.")
                    cuenta.tasa_interes = valor
                else:
                    raise ValueError(f"Propiedad '{clave}' no válida para el tipo de cuenta.")
            
            print(f"Cuenta {numero_cuenta} actualizada con éxito.")
        except ValueError as e:
            print(e)

    def eliminar_cuenta(self, numero_cuenta):
        #Método para eliminar una cuenta bancaria.
        try:
            if self.cuentas.pop(numero_cuenta, None) is None:
                raise ValueError("Cuenta no encontrada.")
            print(f"Cuenta {numero_cuenta} eliminada con éxito.")
        except ValueError as e:
            print(e)

    def guardar_datos(self, archivo):
        #Método para guardar las cuentas en un archivo JSON.
        try:
            with open(archivo, 'w') as f:
                data = {numero: cuenta.to_dict() for numero, cuenta in self.cuentas.items()}
                json.dump(data, f, indent=4)
            print(f"Datos guardados en {archivo}.")
        except Exception as e:
            print(f"Error al guardar datos: {e}")

    def cargar_datos(self, archivo):
        #Método para cargar las cuentas desde un archivo JSON.
        try:
            with open(archivo, 'r') as f:
                data = json.load(f)
                self.cuentas = {}
                for numero, cuenta_data in data.items():
                    tipo = cuenta_data.get('tipo')
                    if tipo == 'corriente':
                        cuenta = CuentaBancariaCorriente(
                            numero_cuenta=numero,
                            saldo_inicial=cuenta_data['saldo'],
                            titular=cuenta_data['titular'],
                            descubierto_autorizado=cuenta_data['descubierto_autorizado']
                        )
                    elif tipo == 'ahorro':
                        cuenta = CuentaBancariaAhorro(
                            numero_cuenta=numero,
                            saldo_inicial=cuenta_data['saldo'],
                            titular=cuenta_data['titular'],
                            tasa_interes=cuenta_data['tasa_interes']
                        )
                    else:
                        continue  # Si el tipo no es válido, se ignora
                    self.cuentas[numero] = cuenta
            print(f"Datos cargados desde {archivo}.")
        except FileNotFoundError:
            print(f"El archivo {archivo} no existe.")
        except json.JSONDecodeError:
            print(f"Error al leer el archivo {archivo}. Puede estar dañado o no es un archivo JSON válido.")
        except Exception as e:
            print(f"Error al cargar datos: {e}")
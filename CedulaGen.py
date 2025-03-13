#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import random

# Letras válidas en la cédula nicaragüense (23 letras, sin la Ñ ni vocales con tilde)
LETRAS_VALIDAS = "ABCDEFGHJKLMNPQRSTUVWXY"

# Diccionario que asocia el "código de departamento" con su nombre.
# (En la práctica, los primeros 2 dígitos del municipio.)
DEPARTAMENTOS = {
    "00": "Managua",
    "04": "Carazo",
    "08": "Chinandega",
    "12": "Chontales",
    "16": "Estelí",
    "20": "Granada",
    "24": "Jinotega",
    "28": "León",
    "32": "Madriz",
    "36": "Boaco",
    "40": "Masaya",
    "44": "Matagalpa",
    "48": "Nueva Segovia",
    "52": "Río San Juan",
    "56": "Rivas",
    # Para las regiones autónomas, suelen usarse:
    "60": "RAAN (Costa Caribe Norte)",
    "61": "RAAN (Costa Caribe Norte)",  # A veces varía
    "62": "RAAS (Costa Caribe Sur)",
    # etc.
}

# Para generar una cédula, usaremos un "municipio por defecto" según departamento.
# Puedes adaptarlo si deseas manejar varios municipios.
MUNICIPIOS_POR_DEFECTO = {
    "00": "001",  # Managua
    "04": "041",  # Jinotepe (Carazo)
    "08": "081",  # Chinandega
    "12": "121",  # Juigalpa (Chontales)
    "16": "161",  # Estelí
    "20": "201",  # Granada
    "24": "241",  # Jinotega
    "28": "281",  # León
    "32": "321",  # Somoto (Madriz)
    "36": "361",  # Boaco
    "40": "401",  # Masaya
    "44": "441",  # Matagalpa
    "48": "481",  # Ocotal (Nueva Segovia)
    "52": "521",  # San Carlos (Río San Juan)
    "56": "561",  # Rivas
    "60": "601",  # Puerto Cabezas (RAAN)
    "62": "621",  # Bluefields (RAAS)
}


def quitar_guiones(cedula: str) -> str:
    """Quita todos los guiones de la cadena y la pone en mayúsculas."""
    return cedula.replace("-", "").upper()


def es_cedula_valida(cedula: str) -> bool:
    """
    Verifica la estructura general (14 caracteres), 
    el patrón numérico, la fecha y la letra final.
    """
    if len(cedula) != 14:
        return False

    # Verificamos que los primeros 13 sean dígitos y el último sea letra A-Y
    if not (cedula[:13].isdigit() and cedula[13] in LETRAS_VALIDAS):
        return False

    # Fecha: DDMMYY en posiciones [3:9]
    dd = cedula[3:5]
    mm = cedula[5:7]
    yy = cedula[7:9]

    if not (dd.isdigit() and mm.isdigit() and yy.isdigit()):
        return False

    # Chequeamos día, mes válidos:
    dia = int(dd)
    mes = int(mm)
    anio_abrev = int(yy)

    # Interpretamos el año (ejemplo simple):
    if anio_abrev < 30:
        anio_completo = 2000 + anio_abrev
    else:
        anio_completo = 1900 + anio_abrev

    # Validamos la fecha con un try/except usando datetime
    try:
        datetime.date(anio_completo, mes, dia)
    except ValueError:
        return False

    # Verificar la letra final:
    # Tomamos los primeros 13 dígitos como número entero
    sin_letra = cedula[:13]  # PPPDDMMYYSSSS
    numero_sin_letra = int(sin_letra)
    # Calculamos la posición (mod 23)
    pos_letra = numero_sin_letra % 23
    letra_calculada = LETRAS_VALIDAS[pos_letra]

    if letra_calculada != cedula[13]:
        return False

    return True


def obtener_departamento(cedula: str) -> str:
    """
    Devuelve el nombre del departamento según los 2 primeros dígitos 
    del municipio (cedula[0:2]).
    """
    cod_dpto = cedula[0:2]
    return DEPARTAMENTOS.get(cod_dpto, "Desconocido")


def calcular_edad(cedula: str) -> int:
    """
    Calcula la edad a partir de la cédula, 
    asumiendo DDMMYY en posiciones [3:9].
    """
    dd = cedula[3:5]
    mm = cedula[5:7]
    yy = cedula[7:9]

    dia = int(dd)
    mes = int(mm)
    anio_abrev = int(yy)

    # Interpretación simple del año
    if anio_abrev < 30:
        anio = 2000 + anio_abrev
    else:
        anio = 1900 + anio_abrev

    hoy = datetime.date.today()
    try:
        fecha_nac = datetime.date(anio, mes, dia)
    except ValueError:
        return -1  # Fecha inválida

    # Cálculo de edad
    edad = hoy.year - fecha_nac.year
    # Ajustar si el cumpleaños aún no ha ocurrido este año
    cumple_este_anio = datetime.date(hoy.year, mes, dia)
    if hoy < cumple_este_anio:
        edad -= 1

    return edad


def validar_cedula(cedula_usuario: str):
    """
    Función principal para la opción de validar cédula:
    - Quita guiones
    - Verifica validez
    - Si es válida, muestra departamento y edad
    """
    cedula_limpia = quitar_guiones(cedula_usuario)

    if es_cedula_valida(cedula_limpia):
        depto = obtener_departamento(cedula_limpia)
        edad = calcular_edad(cedula_limpia)
        print(f"\nLa cédula '{cedula_usuario}' ES válida.")
        print(f"Departamento: {depto}")
        if edad >= 0:
            print(f"Edad aproximada: {edad} años")
        else:
            print("No se pudo calcular la edad (fecha inválida).")
    else:
        print(f"\nLa cédula '{cedula_usuario}' NO es válida.")


def generar_cedula(cod_dpto: str, dia: int, mes: int, anio: int) -> str:
    """
    Genera un número de cédula válido según:
      - Código de departamento (2 dígitos) + un municipio por defecto (total 3 dígitos).
      - Día, mes, año (2 dígitos) en DDMMYY.
      - Sufijo aleatorio de 4 dígitos.
      - Letra calculada.
    Retorna la cédula en formato PPPDDMMYYSSSSL (14 caracteres).
    """
    # Obtenemos un municipio "por defecto" asociado a ese departamento.
    # Si no existe, tomamos '001'.
    municipio = MUNICIPIOS_POR_DEFECTO.get(cod_dpto, "001")

    # Ajuste a 2 dígitos para día, mes, y 2 dígitos para año
    dd = f"{dia:02d}"
    mm = f"{mes:02d}"

    # Para el año, usamos solo los últimos 2 dígitos:
    yy = anio % 100
    yy_str = f"{yy:02d}"

    # Generamos sufijo aleatorio de 4 dígitos
    sufijo = random.randint(0, 9999)
    sufijo_str = f"{sufijo:04d}"

    # Parte numérica (13 dígitos)
    parte_numerica = municipio + dd + mm + yy_str + sufijo_str  # PPPDDMMYYSSSS

    # Calculamos la letra:
    numero_sin_letra = int(parte_numerica)
    pos_letra = numero_sin_letra % 23
    letra = LETRAS_VALIDAS[pos_letra]

    return parte_numerica + letra


def menu_principal():
    """
    Muestra un menú simple para probar ambas funciones:
      1) Validar cédula
      2) Generar cédula
      3) Salir
    """
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1) Validar cédula")
        print("2) Generar cédula")
        print("3) Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            ced = input("Ingrese la cédula (con o sin guiones): ")
            validar_cedula(ced)

        elif opcion == "2":
            print("\nDepartamentos disponibles (códigos de 2 dígitos):")
            for k, v in DEPARTAMENTOS.items():
                print(f"  {k} -> {v}")

            cod = input("Ingrese el código de departamento (ej: 08 para Chinandega): ")
            d = int(input("Día de nacimiento (1-31): "))
            m = int(input("Mes de nacimiento (1-12): "))
            y = int(input("Año completo de nacimiento (ej: 1985, 2001): "))

            nueva_cedula = generar_cedula(cod, d, m, y)
            print(f"\nCédula generada: {nueva_cedula}")

        elif opcion == "3":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Intente de nuevo.")


# Punto de entrada si deseas ejecutarlo como script:
if __name__ == "__main__":
    menu_principal()

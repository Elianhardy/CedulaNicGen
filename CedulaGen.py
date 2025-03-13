#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import random

# Letras válidas en la cédula nicaragüense (23 letras, sin la Ñ)
LETRAS_VALIDAS = "ABCDEFGHJKLMNPQRSTUVWXY"

# Diccionario de departamentos (código de dos dígitos)
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
    "60": "RAAN (Costa Caribe Norte)",
    "62": "RAAS (Costa Caribe Sur)",
}

# Diccionario de municipios para cada departamento.
# La clave es el código de departamento y el valor es un diccionario
# donde las claves son los códigos municipales (3 dígitos) y el valor el nombre.
MUNICIPIOS = {
    "00": {  # Managua
        "001": "Managua",
        "002": "San Rafael del Sur",
        "003": "Tipitapa",
        "004": "Villa El Carmen",
        "005": "San Francisco Libre",
        "006": "Mateare",
        "007": "Ticuantepe",
        "008": "Ciudad Sandino",
        "009": "El Crucero"
    },
    "04": {  # Carazo
        "041": "Jinotepe",
        "042": "Diriamba",
        "043": "Dolores",
        "044": "Santa Teresa",
        "045": "La Paz de Carazo",
        "046": "El Rosario",
        "047": "La Conquista",
        "048": "San Marcos"
    },
    "08": {  # Chinandega
        "081": "Chinandega",
        "082": "Corinto",
        "083": "El Realejo",
        "084": "Chichigalpa",
        "085": "Posoltega",
        "086": "El Viejo",
        "087": "Puerto Morazán",
        "088": "Somotillo",
        "089": "Villa Nueva",
        "090": "Santo Tomás del Norte",
        "091": "Cinco Pinos",
        "092": "San Francisco del Norte",
        "093": "San Pedro del Norte"
    },
    "12": {  # Chontales
        "121": "Juigalpa",
        "122": "Acoyapa",
        "123": "Santo Tomás",
        "124": "Villa Sandino",
        "125": "San Pedro de Lóvago",
        "126": "La Libertad",
        "127": "Santo Domingo",
        "128": "Comalapa",
        "129": "San Francisco de Cuapa",
        "130": "El Coral"
    },
    "16": {  # Estelí
        "161": "Estelí",
        "162": "Pueblo Nuevo",
        "163": "Condega",
        "164": "San Juan de Limay",
        "165": "La Trinidad",
        "166": "San Nicolás"
    },
    "20": {  # Granada
        "201": "Granada",
        "202": "Nandaime",
        "203": "Diriá",
        "204": "Diriomo"
    },
    "24": {  # Jinotega
        "241": "Jinotega",
        "242": "San Rafael del Norte",
        "243": "San Sebastián de Yalí",
        "244": "La Concordia",
        "245": "San José de Bocay",
        "246": "El Cuá",
        "247": "Santa María de Pantasma",
        "248": "Wiwilí de Jinotega"
    },
    "28": {  # León
        "281": "León",
        "282": "Nagarote",
        "283": "Quezalguaque",
        "284": "El Jicaral",
        "285": "El Sauce",
        "286": "La Paz Centro",
        "287": "Achuapa",
        "288": "Santa Rosa del Peñón",
        "289": "Telica",
        "290": "Larreynaga (Malpaisillo)"
    },
    "32": {  # Madriz
        "321": "Somoto",
        "322": "Telpaneca",
        "323": "San Juan del Río Coco",
        "324": "Palacagüina",
        "325": "Yalagüina",
        "326": "Totogalpa",
        "327": "Las Sabanas",
        "328": "San Lucas",
        "329": "San José de Cusmapa"
    },
    "36": {  # Boaco
        "361": "Boaco",
        "362": "Camoapa",
        "363": "Santa Lucía",
        "364": "San José de los Remates",
        "365": "San Lorenzo",
        "366": "Teustepe"
    },
    "40": {  # Masaya
        "401": "Masaya",
        "402": "Nindirí",
        "403": "Tisma",
        "404": "Catarina",
        "405": "San Juan de Oriente",
        "406": "Niquinohomo",
        "407": "Nandasmo",
        "408": "Masatepe",
        "409": "La Concepción"
    },
    "44": {  # Matagalpa
        "441": "Matagalpa",
        "442": "San Ramón",
        "443": "Sébaco",
        "444": "San Dionisio",
        "445": "Esquipulas",
        "446": "Río Blanco",
        "447": "San Isidro",
        "448": "Terrabona",
        "449": "Rancho Grande",
        "450": "Matiguás",
        "451": "Muy Muy",
        "452": "Tuma - La Dalia",
        "453": "Ciudad Darío"
    },
    "48": {  # Nueva Segovia
        "481": "Ocotal",
        "482": "Santa María",
        "483": "Macuelizo",
        "484": "Dipilto",
        "485": "Jalapa",
        "486": "El Jícaro",
        "487": "Murra",
        "488": "Quilalí",
        "489": "Wiwilí (Nva. Segovia)",
        "490": "Ciudad Antigua",
        "491": "Mozonte",
        "492": "San Fernando"
    },
    "52": {  # Río San Juan
        "521": "San Carlos",
        "522": "El Castillo",
        "523": "San Miguelito",
        "524": "Morrito",
        "525": "El Almendro",
        "526": "San Juan del Norte"
    },
    "56": {  # Rivas
        "561": "Rivas",
        "562": "Moyogalpa",
        "563": "Altagracia",
        "564": "San Jorge",
        "565": "Tola",
        "566": "Belén",
        "567": "Potosí",
        "568": "Buenos Aires",
        "569": "Cárdenas",
        "570": "San Juan del Sur"
    },
    "60": {  # RAAN (Costa Caribe Norte) – listado simplificado
        "601": "Puerto Cabezas",
        "602": "Siuna",
        "603": "El Ayote",
        "604": "Bonanza",
        "605": "Mulukukú"
    },
    "62": {  # RAAS (Costa Caribe Sur) – listado simplificado
        "621": "Bluefields",
        "622": "Corn Island",
        "623": "El Rama",
        "624": "Kukra Hill",
        "625": "La Desembocadura de Río Grande"
    },
}


def quitar_guiones(cedula: str) -> str:
    """Quita todos los guiones de la cadena y la convierte a mayúsculas."""
    return cedula.replace("-", "").upper()


def es_cedula_valida(cedula: str) -> bool:
    """
    Verifica la estructura general (14 caracteres), el formato, la fecha y la letra.
    Formato esperado: PPPDDMMYYSSSSL
    """
    if len(cedula) != 14:
        return False

    # Los primeros 13 deben ser dígitos y el último una letra válida.
    if not (cedula[:13].isdigit() and cedula[13] in LETRAS_VALIDAS):
        return False

    # Validar fecha (DDMMYY en posiciones 3 a 8)
    dd = cedula[3:5]
    mm = cedula[5:7]
    yy = cedula[7:9]

    if not (dd.isdigit() and mm.isdigit() and yy.isdigit()):
        return False

    dia = int(dd)
    mes = int(mm)
    anio_abrev = int(yy)
    # Interpretación simple del año:
    anio_completo = 2000 + anio_abrev if anio_abrev < 30 else 1900 + anio_abrev

    try:
        datetime.date(anio_completo, mes, dia)
    except ValueError:
        return False

    # Calcular la letra de control
    sin_letra = cedula[:13]
    numero_sin_letra = int(sin_letra)
    pos_letra = numero_sin_letra % 23
    letra_calculada = LETRAS_VALIDAS[pos_letra]

    return (letra_calculada == cedula[13])


def obtener_departamento(cedula: str) -> str:
    """Devuelve el nombre del departamento según los dos primeros dígitos del código municipal."""
    cod_dpto = cedula[0:2]
    return DEPARTAMENTOS.get(cod_dpto, "Desconocido")


def calcular_edad(cedula: str) -> int:
    """
    Calcula la edad a partir de la fecha de nacimiento contenida en la cédula (DDMMYY).
    Se asume: YY < 30 -> 20YY; de lo contrario 19YY.
    """
    dd = cedula[3:5]
    mm = cedula[5:7]
    yy = cedula[7:9]

    dia = int(dd)
    mes = int(mm)
    anio_abrev = int(yy)
    anio = 2000 + anio_abrev if anio_abrev < 30 else 1900 + anio_abrev

    hoy = datetime.date.today()
    try:
        fecha_nac = datetime.date(anio, mes, dia)
    except ValueError:
        return -1

    edad = hoy.year - fecha_nac.year
    if hoy < datetime.date(hoy.year, mes, dia):
        edad -= 1
    return edad


def generar_cedula(municipio: str, dia: int, mes: int, anio: int) -> str:
    """
    Genera una cédula válida usando:
      - Código municipal (3 dígitos) seleccionado por el usuario.
      - Fecha de nacimiento en formato DDMMYY.
      - Sufijo aleatorio de 4 dígitos.
      - Letra de control calculada.
    Retorna la cédula en formato PPPDDMMYYSSSSL (14 caracteres).
    """
    dd = f"{dia:02d}"
    mm = f"{mes:02d}"
    yy_str = f"{anio % 100:02d}"

    sufijo = random.randint(0, 9999)
    sufijo_str = f"{sufijo:04d}"

    parte_numerica = municipio + dd + mm + yy_str + sufijo_str
    numero_sin_letra = int(parte_numerica)
    pos_letra = numero_sin_letra % 23
    letra = LETRAS_VALIDAS[pos_letra]

    return parte_numerica + letra


def validar_cedula(cedula_usuario: str):
    """
    Opción para validar una cédula:
      - Quita guiones.
      - Verifica formato, fecha y letra.
      - Muestra departamento y edad si es válida.
    """
    cedula_limpia = quitar_guiones(cedula_usuario)

    if es_cedula_valida(cedula_limpia):
        depto = obtener_departamento(cedula_limpia)
        edad = calcular_edad(cedula_limpia)
        print(f"\nLa cédula '{cedula_usuario}' ES válida.")
        print(f"Departamento: {depto}")
        print(f"Edad aproximada: {edad} años" if edad >= 0 else "No se pudo calcular la edad (fecha inválida).")
    else:
        print(f"\nLa cédula '{cedula_usuario}' NO es válida.")


def menu_generar_cedula():
    """
    Función para la opción de generar cédula.
    Permite seleccionar el departamento, muestra los municipios disponibles y solicita:
      - El código municipal (PPP)
      - Día, mes y año de nacimiento.
    """
    print("\nDepartamentos disponibles (códigos de 2 dígitos):")
    for k, v in DEPARTAMENTOS.items():
        print(f"  {k} -> {v}")

    cod_dpto = input("Ingrese el código de departamento (ej: 08 para Chinandega): ").strip()
    if cod_dpto not in MUNICIPIOS:
        print("Código de departamento no encontrado en la lista de municipios.")
        return

    print(f"\nMunicipios en {DEPARTAMENTOS[cod_dpto]}:")
    for cod_muni, nombre in MUNICIPIOS[cod_dpto].items():
        print(f"  {cod_muni} -> {nombre}")

    muni_seleccionado = input("Ingrese el código municipal (3 dígitos) de la lista anterior: ").strip()
    if muni_seleccionado not in MUNICIPIOS[cod_dpto]:
        print("Código municipal inválido para este departamento.")
        return

    try:
        dia = int(input("Día de nacimiento (1-31): "))
        mes = int(input("Mes de nacimiento (1-12): "))
        anio = int(input("Año completo de nacimiento (ej: 1985, 2001): "))
    except ValueError:
        print("Error: Debe ingresar valores numéricos para la fecha.")
        return

    nueva_cedula = generar_cedula(muni_seleccionado, dia, mes, anio)
    print(f"\nCédula generada: {nueva_cedula}")


def menu_principal():
    """
    Menú principal que permite:
      1) Validar cédula
      2) Generar cédula (seleccionando departamento y municipio)
      3) Salir
    """
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1) Validar cédula")
        print("2) Generar cédula")
        print("3) Salir")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            ced = input("Ingrese la cédula (con o sin guiones): ")
            validar_cedula(ced)
        elif opcion == "2":
            menu_generar_cedula()
        elif opcion == "3":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Intente de nuevo.")


if __name__ == "__main__":
    menu_principal()

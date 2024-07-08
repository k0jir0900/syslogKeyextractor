import argparse
import csv
import re

def parse_syslog(file_path, key_separator=' ', kv_separator='='):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    events = {}
    keys = set()

    for line in lines:
        # Extraer el nombre del evento (valor antes de la primera coma)
        event_type = line.split(',', 1)[0].strip()

        # Separar el resto de la línea
        if key_separator in line:
            _, kv_pairs = line.split(key_separator, 1)
        else:
            kv_pairs = ''

        # Crear un diccionario para el evento
        if event_type not in events:
            events[event_type] = {}

        # Separar los pares key:value
        for kv in kv_pairs.split(key_separator):
            if kv_separator in kv:
                key, value = kv.split(kv_separator, 1)
                key = key.strip()
                value = value.strip()
                events[event_type][key] = value
                keys.add(key)

    return events, keys

def write_to_csv(events, keys, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')

        # Escribir las llaves debajo de cada evento
        header = []
        for event in events:
            header.append(event)
        writer.writerow(header)

        # Encontrar el máximo número de llaves entre todos los eventos
        max_keys = max(len(event) for event in events.values())

        # Escribir las llaves y tipos de datos en el archivo CSV
        for i in range(max_keys):
            row = []
            for event_type, event in events.items():
                event_keys = list(event.keys())
                if i < len(event_keys):
                    key = event_keys[i]
                    value_type = identify_value_type(event[key]).lower()
                    row.append(f"{key}:{value_type}")
                else:
                    row.append('')
            writer.writerow(row)

def identify_value_type(value):
    # Función para identificar el tipo de dato del valor
    value = value.strip()
    if re.match(r"^(true|false)$", value, re.IGNORECASE):
        return "bool"
    elif re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?$", value):
        return "datetime"
    elif re.match(r"^-?\d+\.\d+$", value):
        return "decimal"
    elif re.match(r"^\{?[A-F0-9]{8}(?:-[A-F0-9]{4}){3}-[A-F0-9]{12}\}?$", value, re.IGNORECASE):
        return "guid"
    elif re.match(r"^-?\d+$", value):
        try:
            int_value = int(value)
            if int_value.bit_length() <= 32:
                return "int"
            else:
                return "long"
        except ValueError:
            return "dynamic"
    elif re.match(r"^-?\d+\.\d+(?:E[+-]?\d+)?$", value):
        return "real"
    elif re.match(r"^-?(\d+\.?\d*|\.\d+):(\d+\.?\d*|\.\d+):(\d+\.?\d*|\.\d+)$", value):
        return "timespan"
    else:
        return "string"

def main():
    parser = argparse.ArgumentParser(description='Parse a syslog file and extract keys and event types.')
    parser.add_argument('-f', '--file', required=True, help='Path to the syslog file')
    parser.add_argument('-ks', '--key_separator', default=' ', help='Separator for keys (default: )')
    parser.add_argument('-kv', '--kv_separator', default='=', help='Separator for key:value pairs (default: =)')
    parser.add_argument('-o', '--output', default='eventKey_sample.csv', help='Output CSV file name')

    args = parser.parse_args()

    events, keys = parse_syslog(args.file, args.key_separator, args.kv_separator)

    write_to_csv(events, keys, args.output)
    print(f"CSV file '{args.output}' generated successfully.")

if __name__ == '__main__':
    main()

#  -  syslogkeyextractor
#  -  Author: k0jir0900
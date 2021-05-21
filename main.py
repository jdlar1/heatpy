# /usr/bin/env python

import os

import yaml
import matplotlib.pyplot as plt

from heatpy import Domain


def main():
    """Función principal del programa"""

    config = load_config('config.yml')
    meshfile = os.path.join('mesh_files', config['meshfile'])

    tray = Domain(meshfile)

    print(tray)



def load_config(filename: str = 'config.yml'):
    """Carga la configuración que debe encontrarse en un archivo con formato YAML

    Args:
        filename (str, optional): Nombre del archivo. Defaults to 'config.yml'.

    Returns:
        dict: Configuración representada en un diccionario
    """

    try:
        with open('config.yml') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
    except FileExistsError:
        print('Archivo de configuración no encontrado')

    return config


if __name__ == '__main__':
    main()

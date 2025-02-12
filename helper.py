import logging
import sys
import random
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
# Crear un formato para los logs
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Añadir el manejador al logger
logger.addHandler(console_handler)
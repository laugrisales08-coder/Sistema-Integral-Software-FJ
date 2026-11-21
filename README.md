# Sistema Integral de Gestión de Clientes, Servicios y Reservas — Software FJ

Proyecto académico en Python para el curso Programación.

## Requisitos
- Python 3.9 o superior.
- No requiere instalar librerías externas.

## Archivos
- `main.py`: inicia el programa y presenta el menú.
- `modelos.py`: contiene las clases abstractas, clientes, servicios y reservas.
- `sistema.py`: administra las listas internas y registra eventos.
- `excepciones.py`: define excepciones personalizadas.
- `software_fj.log`: se crea automáticamente al ejecutar el programa.

## Cómo ejecutar
1. Descargue y descomprima la carpeta.
2. Abra una terminal dentro de la carpeta `SoftwareFJ`.
3. Ejecute: `python main.py`
4. Seleccione la opción 1 para ejecutar la demostración.

En algunos equipos el comando puede ser `py main.py`.

## Funcionalidades implementadas
- Programación orientada a objetos: abstracción, herencia, encapsulación y polimorfismo.
- Tres tipos de servicios: salas, alquiler de equipos y asesorías.
- Registro de clientes, servicios y reservas mediante listas en memoria.
- Confirmación, cancelación y procesamiento de reservas.
- Validaciones y excepciones personalizadas.
- Registro de eventos y errores en un archivo de log.
- Demostración de más de 10 operaciones válidas e inválidas.
- Uso de `try/except`, `try/except/else` y `try/except/finally`.

## Nota académica
Python no permite sobrecarga tradicional de métodos como otros lenguajes. En este proyecto se ofrece flexibilidad en `calcular_costo` mediante parámetros opcionales (`impuesto` y `descuento`), para realizar distintas variantes del cálculo.

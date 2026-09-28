# Bitácora

**Fecha:** 21 y 22/09/2026
**Consigna / ejercicio número:** Actividad 1 – práctica ("Organizando Información con Estructuras de Datos")

---

## Antes de resolver

**¿Qué creo que tengo que hacer?**
Guardar los datos de 11 columnas de la EPH (tipo y % de completitud), definir al menos 3 roles que digan qué columnas ve cada uno y cómo se ordenan, y hacer un programa que muestre el informe según el rol. Sin rol: todas las columnas por completitud descendente.

**¿Qué palabras de la consigna me dieron pistas?**
- "usando únicamente colecciones" → listas, tuplas, sets y diccionarios, sin clases ni archivos.
- "opcionalmente, un porcentaje mínimo" → no todos los roles tienen ese dato, así que la estructura tiene que permitir que falte.
- "Se valorará el uso de map(), filter()".
- Las preguntas de la bitácora mencionan `ROLES` y criterios inválidos como "promedio" → hay que validar.

**¿Qué dudas tengo antes de empezar?**
- Si "usando únicamente colecciones" me permite usar `map()`, `filter()` y `lambda`, porque la consigna dice que se valoran pero en ese momento todavía no los habíamos visto en clase.
- Qué estructura conviene para los roles: si una lista de diccionarios o un diccionario de diccionarios.
- Cómo represento que el porcentaje mínimo es **opcional**: si pongo la clave en 0 para todos o directamente no la pongo.
- Qué hacer en los casos que la consigna no aclara: si piden un rol que no existe, o una columna que no está en el dataset.
- De dónde saco los porcentajes de completitud, si no estamos leyendo el archivo real de la EPH.

**¿Necesitaste usar la IA? ¿Qué dudas no pudiste aclarar con los contenidos de la clase?**
- Sí, la usé para discutir el diseño mientras escribía: sobre todo para decidir cómo separar los datos de la lógica y en cuántas funciones convenía dividir el trabajo.
- La duda que no pude resolver con el material que tenía al empezar fue la de `map`, `filter` y `lambda`. La aclaré al leer los apuntes de la **clase 4**, donde están explicados junto con `sorted(..., key=lambda ...)`. Confirmado eso, dejé la solución con `filter` y `map`.
- La otra duda es de criterio más que de Python: la consigna no dice qué hacer ante un rol o un criterio inválido, así que lo decidí yo (avisar y usar un valor por defecto).

---

## Mientras resolvía

### Decisiones de diseño

1. **Columnas: diccionario de diccionarios** (`COLUMNAS`). La clave es el nombre de la columna y el valor es `{"tipo": ..., "completitud": ...}`. Así accedo directo con `COLUMNAS["ITF"]` sin recorrer nada, y como las claves son únicas no puede haber columnas repetidas.
2. **Roles: diccionario de diccionarios** (`ROLES`). La clave es el nombre del rol. Cada rol tiene `columnas` (lista), `criterio`, `orden` y opcionalmente `minimo`. Como `minimo` es opcional, uso `.get("minimo", 0)`: si no está, vale 0 y no filtra nada.
3. **Separé datos y lógica en dos archivos:** `src/config.py` (solo datos) y `src/informe.py` (solo funciones).
4. **Una función por tarea:** `config_del_rol`, `validar_config`, `filtrar_columnas` (usa `filter`), `ordenar_columnas` (usa `sorted` con `key`), `generar_informe` (usa `map`) e `imprimir_informe`.
5. **Separé generar de imprimir:** `generar_informe` devuelve una lista y `imprimir_informe` la muestra. Así puedo comprobar el resultado en el notebook sin mirar la pantalla (ver última celda).
6. **Orden "A" / "B":** usé las letras que pide la consigna (A ascendente, B descendente).
7. **Casos no válidos:** rol inexistente → aviso y lista vacía. Criterio u orden inválido → aviso y valor por defecto. Columna inexistente en un rol → aviso y se ignora.
8. **Salida en columnas:** para que el informe se lea alineado uso f-strings con ancho (`f"{nombre:12} {tipo:5} {completitud:6}%"`), que es el formato que vimos en la clase 1.
9. **Prueba por teclado:** consulté y me pidieron que el ejercicio se pueda testear desde el notebook ingresando el rol por teclado, no pasándolo escrito en el código. Agregué una celda con `input()` que pide el rol y llama a `imprimir_informe()`. Por dentro no cambia nada: `input()` devuelve un string y ese string es el que se pasa como parámetro. Le puse `.lower()` para que "Docente" funcione igual que "docente". Si se ingresa un rol que no existe, salta el aviso.

### Errores / problemas encontrados y cómo los resolví
- Al ordenar por completitud noté que muchas columnas empatan en 100% y que quedaban en el orden en que estaban escritas en el diccionario. Consulté y me confirmaron que el orden entre las que empatan es indistinto, así que lo dejé como lo resuelve Python.
- La consigna escribe el orden como "A: ascendente, B: descendente". Me quedó la duda de si la B era un error y tenía que ser D. Decidí respetar la letra de la consigna y usar A/B, y dejarlo anotado acá por las dudas.
- Al principio la función que imprimía era la misma que armaba el informe, así que para chequear un caso tenía que leer la salida a ojo. Lo separé en `generar_informe` (devuelve la lista) e `imprimir_informe` (la muestra) y recién ahí pude verificar con código, por ejemplo que `CAT_OCUP` no aparezca cuando el mínimo es 80.

### ¿Cómo me di cuenta de que funcionaba?
El notebook `actividad1.ipynb` tiene casos de prueba: sin rol, los 3 roles, orden por nombre descendente, mínimo 100, criterio `"promedio"`, una columna inexistente (`SEXO`) y un rol inexistente (`director`). En `investigador` (mínimo 80) verifiqué que `CAT_OCUP` (58.3%) no aparece.

---

## Preguntas orientadoras

**¿Qué ventajas tienen las estructuras elegidas con respecto a otras vistas en la teoría?**
El diccionario permite buscar una columna o un rol por nombre directamente. Con una lista de tuplas tendría que recorrerla hasta encontrar el nombre, y además la tupla es inmutable, así que no podría actualizar la completitud. Con listas de listas accedería por índice (`fila[2]`), que es menos claro que `["completitud"]`. Para las columnas de interés de cada rol usé una **lista** porque no necesito buscar dentro de ella, solo recorrerla, y `sorted()` devuelve una lista. Un set también evitaría duplicados, pero no respeta el orden en que se escribieron.

**¿Qué valores elegiste para los roles y los porcentajes, y por qué?**
- Completitud: las variables de diseño de la encuesta (PONDERA, REGION, AGLOMERADO, ANO4, TRIMESTRE, MAS_500) y ESTADO en 100%, porque siempre están. EDAD 99.6%. ITF y GDECCFR 84.7% (hay hogares que no declaran ingresos, y el decil sale del ingreso, por eso tienen el mismo valor). CAT_OCUP 58.3% porque solo aplica a personas ocupadas. Son valores simulados, porque el ejercicio no lee el dataset real, pero los elegí para que sean verosímiles y para que queden distintos entre sí: si todas valieran 100%, no se notaría el efecto del orden ni del umbral.
- Roles, elegidos para cubrir combinaciones distintas:
  - `docente`: columnas generales, por nombre ascendente, sin mínimo.
  - `investigador`: incluye ingresos, por completitud descendente, mínimo 80 (quiere solo columnas confiables). Elegí 80 porque parte el conjunto en un punto donde se ve el efecto: deja afuera a CAT_OCUP (58.3%) y adentro a ITF y GDECCFR (84.7%).
  - `analista`: por completitud ascendente, para ver primero las columnas con más datos faltantes.

**¿Cómo garantizaste que el programa pueda validarse con diferentes roles, criterios y umbrales?**
Las funciones reciben `roles` y `columnas` como parámetros (con `ROLES` y `COLUMNAS` como valor por defecto). En el notebook paso un diccionario `ROLES_PRUEBA` con combinaciones que no están en los roles reales, sin tener que modificar `config.py`.

**¿Por qué conviene separar la configuración de los roles (`ROLES`) de la lógica que genera el informe?**
Porque cambian por motivos distintos. Agregar un rol o cambiar un umbral es cambiar datos, y no debería obligarme a tocar funciones que ya andan (y arriesgarme a romperlas). Además, la misma lógica sirve para cualquier configuración, como muestran los casos de prueba.

**¿Qué parámetros se pueden definir con valores por defecto?**
`rol=None` (informe completo), `roles=ROLES`, `columnas=COLUMNAS`, `minimo=0` (sin filtro), `criterio="completitud"` y `orden="B"`. Dentro de cada rol, `minimo` también es opcional. Los parámetros con valor por defecto van al final de la lista, como vimos en la clase 4.

Algo a tener en cuenta: los valores por defecto se evalúan **una sola vez**, cuando se define la función. Entonces `roles=ROLES` queda apuntando al diccionario que existía en ese momento. Si después se reasigna `ROLES` a otro diccionario, la función sigue usando el viejo. Por eso, para probar otras configuraciones, las paso explícitamente con `roles=ROLES_PRUEBA`. Se puede comprobar corriendo `generar_informe.__defaults__` en una celda.

Además, las funciones no leen variables globales directamente: todo lo que usan les llega por parámetro. En la clase vimos que usar globales no es buena práctica.

**Si agregás una nueva columna al dataset, ¿en qué partes del código impacta? ¿Y si solo querés que un rol existente la incluya?**
Solo en `COLUMNAS` de `config.py`: se agrega una entrada nueva. El informe sin rol la muestra automáticamente porque usa todas las claves de `COLUMNAS`. Para que un rol la incluya, se agrega el nombre a la lista `"columnas"` de ese rol en `ROLES`. En ningún caso se toca `informe.py`.

**¿Qué pasaría si un rol tuviera un criterio distinto a "nombre" o "completitud" (por ejemplo, "promedio")? ¿Cómo lo detectarías y qué harías para que no falle?**
`validar_config` compara el criterio contra `CRITERIOS_VALIDOS`. Si no está, muestra un aviso y usa el criterio por defecto (`"completitud"`), así el informe se genera igual. Lo mismo con el orden. Está probado en el notebook con el rol de prueba `criterio_invalido`.

**¿Qué cambiarías si por defecto el informe debiera salir según uno de los roles?**
Agregaría en `config.py` una constante, por ejemplo `ROL_DEFECTO = "docente"`, y en `config_del_rol`, cuando `rol` es `None`, usaría `roles.get(ROL_DEFECTO)` en lugar de armar la configuración con todas las columnas. Es un cambio en un solo lugar.

---

## Al terminar

**¿Qué descubrí o entendí mejor a partir de esto?**
- Que `.get(clave, valor_por_defecto)` es la forma prolija de manejar una clave opcional como `minimo`, sin tener que preguntarla con un `if` cada vez.
- Que separar la función que calcula de la que imprime hace mucho más fácil probar el programa.
- Que los valores por defecto de los parámetros se evalúan una sola vez, cuando se define la función, así que conviene pasar la configuración explícitamente cuando quiero probar otra.

**¿Qué me queda pendiente o sigo sin entender?**
- No estoy seguro de si, ante un rol inexistente, está mejor avisar y devolver una lista vacía (lo que hice) o cortar con un error. Todavía no vimos manejo de excepciones.
- Cuándo conviene `filter()` y cuándo una list comprehension. La clase 4 menciona que `filter` devuelve un iterador perezoso y que eso sirve con secuencias muy grandes, pero no me queda claro cuánto pesa eso en un caso chico como este.
- No usé `reduce()`. Me quedó la duda de si había alguna parte del ejercicio donde tuviera sentido.

**¿Esto se relaciona con otro ejercicio o concepto que ya vimos?**
- Sí, con casi todo lo de colecciones: diccionarios anidados (como el ejemplo de `music` de la clase 4), listas y `sorted()`.
- Con funciones: parámetros con valores por defecto, docstrings y retorno de varios valores. `validar_config` devuelve una tupla `(criterio, orden, minimo)` y la desempaqueto en tres variables, igual que el ejemplo `summarize_text` de la clase.
- Con el ejemplo de la clase de ordenar `dic_movies` por duración con `key=lambda elem: elem[1]`: es exactamente lo mismo que hago para ordenar las columnas por completitud.
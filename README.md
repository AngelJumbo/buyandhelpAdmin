# buyandhelpAdmin

## Levantar servicio

1. Crear `Virtual Enviroment`
```bash
$ python3 -m venv venv
```
2. Activar `Virtual Enviroment`
```bash
$ source venv/bin/activate
```
3. Instalar requerimientos
```bash
$ pip install -r requirements.txt
```
4. Crear migraciones
```bash
$ python manage.py makemigrations Buy
```
5. Ejecutar migraciones
```bash
$ python manage.py migrate
```
6. Correr servicio
```bash
$ python manage.py runserver
```

vistas:<br />
<ul>
<li>/ </li>
<li>/admin</li>
<li>/contact</li>
<li>/api/articulos</li>
</ul>

# suite-api

Para iniciar el proyecto primero hay que crear
un entorno virtual y luego instalar las dependencias
con pip:

```
virtualenv venv --no-site-packages
pip install -r requirements.txt
```

Luego, se puede lanzar el servidor usando gunicorn
o directamente python:

```
gunicorn app:app
```

```
python app.py
```

# Subtitles Translator
Permite traducir subtítulos **.srt** utilizando el traductor de Google.

## Comenzando
El proyecto utiliza Selenium para obtener la traducción, en lugar de la API de Google.<br/>
Lo que necesitaremos para que funcione es Python 3, Selenium (hemos utilizado la versión 3.141.0) y chromedriver (hemos utilizado la versión 92.0.4515.43).

Para instalar Python:
```
https://www.python.org/downloads/
```

Para instalar Selenium:
```
pip install selenium
```

Chromedriver lo puedes obtener [aquí](https://chromedriver.chromium.org/downloads)

## Funcionamiento
El programa busca todos los **.srt** que se encuentren en el directorio donde se ejecuta, y los comienza a traducir.<br/>

La sintaxis es la siguiente:
```
subtitlesTranslator.py -i <code> -o <code>
```

<code>-i</code> permitirá ingresar el código (idioma) del subtítulo de entrada<br/>
<code>-o</code> permitirá ingresar el código (idioma) del subtítulo de salida

Si no se ingresa ninguno de estos dos argumentos, entonces tomará por defecto el código <code>auto</code> (automático) para <code>-i</code> y el código <code>es</code> (español) para <code>-o</code>.<br/>

Es decir, ejecutar
```
subtitlesTranslator.py
```

hará que el código de ingreso sea el automático y el de salida sea el español. Por lo que traducirá los subtítulos de esa forma.

Para saber los códigos disponibles que soporte el traductor de Google, deben ejecutar
```
subtitlesTranslator.py -c
```
Esto mostrará una lista con los códigos y el idioma al que pertenece cada uno. La respuesta será del tipo
```
código -> idioma
```
Para realizar un backup del archivo que se quiere traducir, sólo tienen que ejecutar 
```
subtitlesTranslator.py -b
```
Toda esta información, la pueden obtener ejecutando
```
subtitlesTranslator.py -h
```
# Autores
Marco Weihmüller

# Licencia
Este proyecto está bajo la Licencia GNU General Public License v3.0

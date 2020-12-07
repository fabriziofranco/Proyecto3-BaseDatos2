from flask import Flask, render_template, request, redirect, url_for, Response, flash, send_from_directory
import json
import importlib
import sys
import os 
import glob
import time
import rtree_index
from werkzeug.utils import secure_filename

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


app = Flask(__name__,
            static_url_path='', 
            static_folder='frontEnd/static',
            template_folder='frontEnd/templates')
app.secret_key = b'heiderEsLoMaximo/'

@app.route('/')
def home():
   return render_template('buscador.html')


@app.route('/search', methods = ['POST'])
def search():
   type_of_search = request.form.get("type")

   if type_of_search == "knn":
      num_results = int(request.form.get("numElement"))
   elif type_of_search == "rango":
      range_results = float(request.form.get("numRange"))
   else:
      flash('Seleccionar el tipo de búsqueda.', 'alert-danger')
      return redirect(url_for('home'))


   if 'file' not in request.files:
      flash('No hay archivo, intente nuevamente.', 'alert-danger')
      return redirect(url_for('home'))
   
   file = request.files['file']

   if file.filename == '':
      flash('Archivo no seleccionado', 'alert-danger')
      return redirect(url_for('home'))
   
   if file:
      filename = secure_filename(file.filename)

   files = glob.glob('data/imageInput/*')
   for f in files:
      os.remove(f)
   
   start = time.time()
   archivo =  open("data/imageInput/"+str(file.filename), "wb")
   archivo.write(file.read())

   if type_of_search == "rango":
      list_of_path = rtree_index.range_search_rtree(str(file.filename), range_results, "12800", True)
      end = time.time()
      flash(u'Se han encontrado los resultados en ' + str(end - start) + ' segundos utilizando la búsqueda por rango.',  'alert-success')
   
   else:
      list_of_path = rtree_index.KNN_FaceRecognition(str(file.filename), num_results, "12800", True)
      end = time.time()
      flash(u'Se han encontrado ' + str(num_results) + ' resultados en ' + str(end - start) + ' segundos utilizando la búsqueda KNN.',  'alert-success')
   


   images_output = list()
   for f in list_of_path:
      images_output.append('data/12800/' + f)
      
   print(images_output)
   return render_template('buscador.html', images_output=images_output)



@app.route('/data/12800/<path:filename>')
def base_static(filename):
    return send_from_directory('data/12800/', filename)
   
if __name__ == '__main__':
   app.run()
from flask import Flask, render_template, request, redirect, url_for, Response, flash, send_from_directory
import json
import importlib
import sys
import os 
import glob
import time
import rtree_index

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
   uploaded_files = request.files.getlist("file")
   numero_bloques = request.form.get("numElement")
   
   files = glob.glob('data/imageInput/*')
   for f in files:
      os.remove(f)

   for file in uploaded_files:
      with open("data/imageInput/"+str(file.filename), "wb") as archivo:
         archivo.write(file.read())
         list_of_path = rtree_index.KNN_FaceRecognition(str(file.filename), 8, "12800")
      
   flash(u'Los datos se han cargado de manera correcta.',  'alert-success')

   images_output = list()
   for f in list_of_path:
      tempImage = dict()
      tempImage["url"] = 'data/12800/' + f
      images_output.append(tempImage)
      

   print(images_output)
   return render_template('buscador.html', images_output=images_output)



@app.route('/data/12800/<path:filename>')
def base_static(filename):
    return send_from_directory('data/12800/', filename)
   
if __name__ == '__main__':
   app.run()
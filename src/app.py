from flask import Flask, render_template, request, redirect, url_for, Response, flash, send_from_directory
import json
import importlib
import sys
import os 
import glob
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append("../merging_blocks/0.json")

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
   
   #index.Index("clean", "inverted_index", "merging_blocks", "sorted_blocks", int(numero_bloques))
   
   flash(u'Los datos se han cargado de manera correcta.',  'alert-success')

   images_output = list()
   for f in glob.glob('data/imageOutput/*'):
      tempImage = dict()
      tempImage["url"] = f
      tempImage["accuracy"] = 0.8
      images_output.append(tempImage)


   print(images_output)
   return render_template('buscador.html', images_output=images_output)



@app.route('/data/imageOutput/<path:filename>')
def base_static(filename):
    return send_from_directory('data/imageOutput/', filename)
   
if __name__ == '__main__':
   app.run()
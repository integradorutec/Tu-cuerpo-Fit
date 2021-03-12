import web
import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import json

urls = ('/upload', 'Upload')

class Upload():
    
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        return """
        <html>
            <head>              
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-BmbxuPwQa2lc/FVzBcNJ7UAyJxM6wuqIj61tLrc4wSX0szH/Ev+nYRRuWlolflfl" crossorigin="anonymous">
            <title>Distintor de ropa</title>
            </head>
                <body>
                  <body style="background-color:#FFAAAA;">
                    <form method="POST" enctype="multipart/form-data" action="">
                    <h1 align="center">Identificador de ropa</h1>
                    <br>
                    <div align="center" style="width:50px; height:50px;"><img src= "static/home.jpg"/> </div>
                    <div align="center">
                    <br>
                    <br>
                    <div class="input-group mb-3">
                    <label class="input-group-text" for="inputGroupFile01"></label>
                    <input type="file" class="form-control" id="inputGroupFile01" name="myfile">
                    </div>
                    <input type="submit" class="btn btn-primary" />
                    </div>
                    </form>
                    </body></html>"""
        

    def POST(self):
        x = web.input(myfile={})
        filedir = 'static' # change this to the directory you want to store the file in.
        if 'myfile' in x: # to check if the file-object is created
            filepath=x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
            filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
            fout = open(filedir +'/'+ filename,'wb') # creates the file where the uploaded file should be stored
            fout.write(x.myfile.file.read()) # writes the uploaded file to the newly created file.
            fout.close() # closes the file, upload complete.
       # print(str(filedir +'/'+ filename))
        return self.machine(str(filedir +'/'+ filename))

        #raise web.seeother('/upload')

    def machine(self,ruta):              
    # Disable scientific notation for clarity
        np.set_printoptions(suppress=True)

    # Load the model
        model = tensorflow.keras.models.load_model('static/keras_model.h5')

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1.
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
        image = Image.open(ruta)

    #resize the image to a 224x224 with the same strategy as in TM2:
    #resizing the image to be at least 224x224 and then cropping from the center
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)

    #turn the image into a numpy array
        image_array = np.asarray(image)

    # display the resized image
        image.show()

    # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    # Load the image into the array
        data[0] = normalized_image_array

    # run the inference
        prediction = model.predict(data)
        data={}
        for i in prediction:
            if i[0] > 0.7:
                resultado = "Es un vestido"
                data["Prenda"]=resultado
            if i[1] > 0.7:
                resultado = "Es una camisa"
                data["Prenda"]=resultado
            elif i[2] > 0.7:
                resultado = "Eres una pantalon"
                data["Prenda"]=resultado
            elif i[3] > 0.7:
                resultado = "Es una playera"
                data["Prenda"]=resultado
            elif i[4] > 0.7:
                resultado = "Es un sueter"               
                data["Prenda"]=resultado
            else:
                resultado = "No se encontraron coincidencias:"
                data["Prenda"]=resultado
        return json.dumps(data) 
        raise web.seeother('/upload')



if __name__ == "__main__":
    app = web.application(urls, globals()) 
    app.run()
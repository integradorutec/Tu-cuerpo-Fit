import web
import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np

urls = ('/upload', 'Upload')

class Upload():
    
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        return """
        <html>
            <head>
            </head>
                <body>
<form method="POST" enctype="multipart/form-data" action="">
<input type="file" name="myfile" />
<br/>
<input type="submit" />
</form>
</body></html>"""
    
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        return """
        <html>
            <head>
            </head>
            <body>
                <form method="POST" enctype="multipart/form-data" action="">
                    <input type="file" name="myfile" />
                    <br/>
                    <input type="submit" />
                </form>
            </body>
        </html>"""

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
        for i in prediction:
            if i[0] > 0.7:
                resultado = "Es un vestido: "
            if i[1] > 0.7:
                resultado = "Es una camisa: "
            elif i[2] > 0.7:
                resultado = "Eres una pantalon: "
            elif i[3] > 0.7:
                resultado = "Es una playera: "
            elif i[4] > 0.7:
                resultado = "Es un sueter: "
            else:
                resultado = "No se encontro coincidencias:"
        return resultado
        raise web.seeother('/upload')



if __name__ == "__main__":
    app = web.application(urls, globals()) 
    app.run()
<!DOCTYPE html>
<?php
echo shell_exec("python /var/www")
?>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width">
    <title>Bienvenido</title>
    <h1 class="display-1" align="center">Bienvenido</h1>

  </head>
  <body align="center" style="background-color:#F6DDCC">
    <h3> Suba la imagen a analizar </h3>
    <form enctype="multipart/form-data" action="uploader.php" method="POST" >
      <div>
      <input name="foto" type="file"/>
      </div>
      <div>
      <input name="Upload" type="submit"/>
      </div>
      
    </form>
  </body>
</html>
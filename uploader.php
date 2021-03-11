<?php
$carpeta = "files/imagenes/";
opendir($carpeta);
copy ($_FILES['foto']['tmp_name'], $_FILES['foto']['name']);
echo "Archivo subido";
$nombre= $_FILES['foto']['name'];
echo "<img src=\"$nombre\">";
echo $nombre
?>
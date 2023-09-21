<?php
$host = 'mysql';
$dbname = 'nombre_de_la_base_de_datos';
$user = 'usuario_de_la_base_de_datos';
$pass = 'contrasena_de_la_base_de_datos';

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname", $user, $pass);
    // Configura otras opciones de PDO según sea necesario
} catch (PDOException $e) {
    die("Error de conexión a la base de datos: " . $e->getMessage());
}

?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <?php echo '<p>Hello World!!!</p>'; ?>
</body>
</html>

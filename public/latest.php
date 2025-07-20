<?php
$baseDir = __DIR__; // directorio actual: /output
$dirs = glob($baseDir . '/*', GLOB_ONLYDIR);

// Buscar la carpeta más reciente (por nombre)
usort($dirs, function ($a, $b) {
    return strcmp($b, $a); // de mayor a menor
});

$latestDir = $dirs[0] ?? null;
if (!$latestDir) {
    echo "Error: No hay carpetas.";
    exit;
}

// Buscar la imagen más reciente dentro de esa carpeta
$images = glob($latestDir . '/*.png');
usort($images, function ($a, $b) {
    return filemtime($b) - filemtime($a); // más reciente primero
});

$latestImage = $images[0] ?? null;
if (!$latestImage) {
    echo "Error: No hay imágenes.";
    exit;
}

// Ruta pública relativa
$publicPath = str_replace($_SERVER['DOCUMENT_ROOT'], '', $latestImage);
$fullUrl = "http://" . $_SERVER['HTTP_HOST'] . $publicPath;
?>

<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Última Imagen del Sistema</title>
  <style>
    body { font-family: sans-serif; text-align: center; padding: 20px; background: #f6f6f6; }
    img { max-width: 90%; height: auto; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.2); }
  </style>
</head>
<body>
  <h2>🌀 Última Imagen Generada</h2>
  <p><?= basename($latestImage) ?></p>
  <img src="<?= htmlspecialchars($fullUrl) ?>" alt="Última Imagen">
</body>
</html>

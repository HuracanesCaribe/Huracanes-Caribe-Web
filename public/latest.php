<?php
function get_latest_image($basin_prefix, $local_base, $base_url) {
    // Buscar carpetas tipo fecha
    $folders = array_filter(glob($local_base . '/*'), function ($dir) {
        return is_dir($dir) && preg_match('/\d{4}-\d{2}-\d{2}/', basename($dir));
    });

    if (empty($folders)) {
        return ["error" => "No se encontraron carpetas."];
    }

    // Ordenar de más reciente a más antigua
    usort($folders, function ($a, $b) {
        return strcmp($b, $a);
    });

    foreach ($folders as $folder) {
        $basename = basename($folder);
        $pattern = $folder . '/' . $basin_prefix . '_*.png';
        $images = glob($pattern);

        if (!empty($images)) {
            // Ordenar por fecha de modificación
            usort($images, function ($a, $b) {
                return filemtime($b) - filemtime($a);
            });

            $latest_image = basename($images[0]);
            $url = $base_url . '/' . $basename . '/' . $latest_image;

            return [
                "url" => $url,
                "file" => $latest_image,
                "date" => $basename
            ];
        }
    }

    return ["error" => "No se encontraron imágenes para $basin_prefix."];
}

// Ruta local absoluta
$local_base = __DIR__ . '/../TWO_Script/output';
$base_url = 'http://150.230.24.24/output';

$atlantic = get_latest_image('atlantic', $local_base, $base_url);
$eastpac = get_latest_image('eastpac', $local_base, $base_url);

// Mostrar resultados
function render_image($title, $data) {
    if (isset($data['error'])) {
        echo "<h3>$title</h3><p style='color:red;'>{$data['error']}</p>";
    } else {
        echo "<h3 style='font-family:sans-serif;'>$title</h3>";
        echo "<img src='{$data['url']}' style='max-width:100%; border-radius:10px;' />";
        echo "<p style='font-family:sans-serif; font-size:14px;'>{$data['date']} / {$data['file']}</p>";
    }
}

render_image('🌊 Imagen más reciente del Atlántico', $atlantic);
render_image('🌋 Imagen más reciente del Pacífico Este', $eastpac);
?>

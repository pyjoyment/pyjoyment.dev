<?php
// The front controller, which gets every path that names no file of www/, as in Laravel or Symfony
$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

if ($path === '/') {
    echo '<link rel="stylesheet" href="/css/site.css"><h1>Hello from PHP ' . PHP_VERSION . '</h1>';
} elseif (preg_match('#^/hello/(\w+)$#', $path, $m)) {
    header('Content-Type: application/json');
    echo json_encode(['hello' => $m[1]]);
} else {
    http_response_code(404);
    echo 'Not found';
}

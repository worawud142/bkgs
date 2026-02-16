<?php
// api/news.php
require_once 'db.php';
session_start();

$method = $_SERVER['REQUEST_METHOD'];

// Helper to check auth for write operations
function checkAuth()
{
    if (!isset($_SESSION['user_id'])) {
        http_response_code(401);
        echo json_encode(["error" => "Unauthorized"]);
        exit();
    }
}

// GET: Fetch news
if ($method === 'GET') {
    $id = $_GET['id'] ?? null;
    $limit = $_GET['limit'] ?? null;
    $slug = $_GET['slug'] ?? null;

    if ($id) {
        $stmt = $conn->prepare("SELECT * FROM news WHERE id = :id");
        $stmt->execute(['id' => $id]);
        $row = $stmt->fetch(PDO::FETCH_ASSOC);
        echo json_encode($row ?: null);
    } elseif ($slug) {
        $stmt = $conn->prepare("SELECT * FROM news WHERE slug = :slug");
        $stmt->execute(['slug' => $slug]);
        $row = $stmt->fetch(PDO::FETCH_ASSOC);
        echo json_encode($row ?: null);
    } else {
        $sql = "SELECT * FROM news ORDER BY created_at DESC";
        if ($limit) {
            $sql .= " LIMIT " . intval($limit);
        }
        $stmt = $conn->query($sql);
        $rows = $stmt->fetchAll(PDO::FETCH_ASSOC);
        echo json_encode($rows);
    }
    exit();
}

// POST: Create or Update (Multipart Form Data)
if ($method === 'POST') {
    checkAuth();

    $id = $_POST['id'] ?? '';
    $title = $_POST['title'] ?? '';
    $slug = $_POST['slug'] ?? '';
    $desc = $_POST['desc'] ?? ''; // 'desc' is a reserved word in SQL, use prepared statement properly or rename column? Plan said 'description' but code might use 'desc' from frontend.
    // The schema says `description`, frontend sends `desc`. I will map it.
    $content = $_POST['content'] ?? '';
    $date = $_POST['date'] ?? '';
    $tag = $_POST['tag'] ?? 'ข่าว';

    // Handle File Upload
    $coverUrl = $_POST['existingCover'] ?? '';
    if (isset($_FILES['cover']) && $_FILES['cover']['error'] === UPLOAD_ERR_OK) {
        $uploadDir = '../uploads/';
        if (!is_dir($uploadDir))
            mkdir($uploadDir, 0777, true);

        $filename = time() . '_' . basename($_FILES['cover']['name']);
        $targetPath = $uploadDir . $filename;

        if (move_uploaded_file($_FILES['cover']['tmp_name'], $targetPath)) {
            // Return relative path for frontend to use
            $coverUrl = 'uploads/' . $filename;
        }
    }

    if ($id) {
        // Update
        $sql = "UPDATE news SET title=:title, slug=:slug, description=:desc, content=:content, event_date=:date, tag=:tag";
        $params = [
            'title' => $title,
            'slug' => $slug,
            'desc' => $desc,
            'content' => $content,
            'date' => $date,
            'tag' => $tag
        ];

        if ($coverUrl) {
            $sql .= ", cover_image=:cover";
            $params['cover'] = $coverUrl;
        }

        $sql .= " WHERE id=:id";
        $params['id'] = $id;

        $stmt = $conn->prepare($sql);
        $stmt->execute($params);
        echo json_encode(["success" => true, "id" => $id]);

    } else {
        // Create
        $stmt = $conn->prepare("INSERT INTO news (title, slug, description, content, event_date, tag, cover_image) VALUES (?, ?, ?, ?, ?, ?, ?)");
        $stmt->execute([$title, $slug, $desc, $content, $date, $tag, $coverUrl]);
        echo json_encode(["success" => true, "id" => $conn->lastInsertId()]);
    }
    exit();
}

// DELETE
if ($method === 'DELETE') {
    checkAuth();
    // DELETE method payload is tricky in PHP, usually via URL param for ID
    // Frontend should usually make DELETE request to api/news.php?id=...

    $id = $_GET['id'] ?? null;
    if (!$id) {
        http_response_code(400);
        echo json_encode(["error" => "ID required"]);
        exit();
    }

    $stmt = $conn->prepare("DELETE FROM news WHERE id = :id");
    $stmt->execute(['id' => $id]);
    echo json_encode(["success" => true]);
    exit();
}
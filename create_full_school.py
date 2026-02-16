import os

# ชื่อโฟลเดอร์โปรเจกต์
base_dir = "bankhuakai_school_full"

# โค้ดทั้งหมด
files = {
    # ---------------------------------------------------------
    # 1. DATABASE SQL
    # ---------------------------------------------------------
    "database.sql": """
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+07:00";

CREATE DATABASE IF NOT EXISTS school_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE school_db;

-- ตารางผู้ดูแลระบบ
CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- ตารางตั้งค่าเว็บไซต์ (แก้ไขข้อมูลโรงเรียน/ผอ. ได้เอง)
CREATE TABLE IF NOT EXISTS site_settings (
    id INT PRIMARY KEY,
    school_name_th VARCHAR(255) DEFAULT 'โรงเรียนบ้านขัวก่าย',
    school_name_en VARCHAR(255) DEFAULT 'Ban Khua Kai School',
    director_name VARCHAR(100) DEFAULT 'นายสมชาย ใจดี',
    director_position VARCHAR(100) DEFAULT 'ผู้อำนวยการโรงเรียน',
    director_msg TEXT,
    director_img VARCHAR(255) DEFAULT 'director_default.jpg',
    vision TEXT,
    phone VARCHAR(50),
    facebook_link VARCHAR(255)
);

-- ตารางข่าว
CREATE TABLE IF NOT EXISTS news (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    cover_img VARCHAR(255) DEFAULT 'news_placeholder.jpg',
    category VARCHAR(50) DEFAULT 'ประชาสัมพันธ์',
    view_count INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ตารางกิจกรรม
CREATE TABLE IF NOT EXISTS activities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    activity_date DATE,
    cover_img VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ข้อมูลเริ่มต้น (Seed Data)
INSERT INTO admins (username, password) VALUES ('admin', 'admin1234') ON DUPLICATE KEY UPDATE id=id;
INSERT INTO site_settings (id, director_msg, vision, phone, facebook_link) VALUES 
(1, 'มุ่งมั่นพัฒนาผู้เรียน ให้เป็นคนดี คนเก่ง และมีความสุข', 'เป็นเลิศทางวิชาการ สื่อสารสองภาษา ล้ำหน้าทางความคิด', '042-123-456', 'https://facebook.com/bankhuakai')
ON DUPLICATE KEY UPDATE id=id;

INSERT INTO news (title, content, category, created_at) VALUES 
('ประกาศเปิดภาคเรียนที่ 1/2568', 'โรงเรียนบ้านขัวก่ายขอแจ้งกำหนดการเปิดภาคเรียน...', 'วิชาการ', NOW()),
('รับสมัครนักเรียนใหม่ ประจำปีการศึกษา 2568', 'รายละเอียดการรับสมัครนักเรียนชั้นอนุบาล 1 และ ป.1...', 'รับสมัคร', NOW());
""",

    # ---------------------------------------------------------
    # 2. SYSTEM CONFIG & CSS
    # ---------------------------------------------------------
    "connect.php": """<?php
// ตั้งค่าสำหรับ MAMP (Mac)
$host = "localhost:8889"; 
$user = "root";
$pass = "root"; 
$db = "school_db";

try {
    $conn = new PDO("mysql:host=$host;dbname=$db;charset=utf8mb4", $user, $pass);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch(PDOException $e) {
    echo "Connection failed: " . $e->getMessage();
}

// ฟังก์ชันดึงค่า Setting
function getSetting($conn) {
    $stmt = $conn->query("SELECT * FROM site_settings WHERE id = 1");
    return $stmt->fetch(PDO::FETCH_ASSOC);
}
?>""",

    "assets/css/style.css": """
@import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600&family=Sarabun:wght@400;500&display=swap');

:root {
    --primary: #0d6efd;     /* Blue */
    --secondary: #0dcaf0;   /* Cyan */
    --accent: #ffc107;      /* Yellow */
    --dark: #343a40;
    --light: #f8f9fa;
    --font-head: 'Kanit', sans-serif;
    --font-body: 'Sarabun', sans-serif;
}

body { font-family: var(--font-body); background-color: #f4f6f9; }
h1, h2, h3, h4, h5, h6, .nav-link, .btn { font-family: var(--font-head); }

/* Navbar */
.navbar { box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
.nav-link { font-weight: 500; color: var(--dark) !important; }
.nav-link:hover, .nav-link.active { color: var(--primary) !important; }

/* Hero Section */
.hero {
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    color: white;
    padding: 80px 0;
    position: relative;
    overflow: hidden;
}
.hero::after {
    content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background: url('https://source.unsplash.com/1600x900/?school,building') center/cover;
    opacity: 0.1;
}
.director-card {
    background: white;
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    border-top: 5px solid var(--accent);
}

/* Cards */
.news-card { transition: 0.3s; border: none; border-radius: 10px; overflow: hidden; background: white; }
.news-card:hover { transform: translateY(-5px); box-shadow: 0 10px 15px rgba(0,0,0,0.05); }
.news-date { font-size: 0.85rem; color: #888; }
.badge-cat { position: absolute; top: 10px; right: 10px; }

/* Footer */
footer { background-color: var(--dark); color: #ccc; padding-top: 40px; }
footer h5 { color: white; }
""",

    "includes/navbar.php": """
<?php $settings = getSetting($conn); ?>
<nav class="navbar navbar-expand-lg navbar-light bg-white sticky-top">
  <div class="container">
    <a class="navbar-brand d-flex align-items-center" href="index.php">
        <img src="assets/img/logo.png" width="40" height="40" class="me-2" alt="Logo">
        <div>
            <div class="fw-bold text-primary" style="line-height:1;"><?php echo $settings['school_name_th']; ?></div>
            <small class="text-muted" style="font-size:0.7rem;"><?php echo $settings['school_name_en']; ?></small>
        </div>
    </a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navMain">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navMain">
      <ul class="navbar-nav ms-auto gap-2">
        <li class="nav-item"><a class="nav-link" href="index.php">หน้าแรก</a></li>
        <li class="nav-item"><a class="nav-link" href="about.php">ข้อมูลโรงเรียน</a></li>
        <li class="nav-item"><a class="nav-link" href="news.php">ข่าวประชาสัมพันธ์</a></li>
        <li class="nav-item"><a class="nav-link" href="activities.php">กิจกรรม</a></li>
        <li class="nav-item"><a class="nav-link" href="contact.php">ติดต่อเรา</a></li>
        <li class="nav-item"><a class="btn btn-outline-primary rounded-pill px-4" href="admin/login.php">เข้าระบบครู</a></li>
      </ul>
    </div>
  </div>
</nav>
""",
    "includes/footer.php": """
<?php $settings = getSetting($conn); ?>
<footer>
    <div class="container pb-4">
        <div class="row">
            <div class="col-md-4 mb-3">
                <h5><?php echo $settings['school_name_th']; ?></h5>
                <p class="small"><?php echo $settings['vision']; ?></p>
            </div>
            <div class="col-md-4 mb-3">
                <h5>เมนูลัด</h5>
                <ul class="list-unstyled small">
                    <li><a href="#" class="text-decoration-none text-muted">งานทะเบียนวัดผล</a></li>
                    <li><a href="#" class="text-decoration-none text-muted">ปฏิทินวิชาการ</a></li>
                </ul>
            </div>
            <div class="col-md-4 mb-3">
                <h5>ติดต่อเรา</h5>
                <p class="small">
                    📞 <?php echo $settings['phone']; ?><br>
                    Facebook: <a href="<?php echo $settings['facebook_link']; ?>" target="_blank" class="text-info">คลิกที่นี่</a>
                </p>
            </div>
        </div>
    </div>
    <div class="bg-black py-2 text-center small text-muted">
        © 2025 <?php echo $settings['school_name_en']; ?> | School Management System
    </div>
</footer>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
""",

    # ---------------------------------------------------------
    # 3. FRONTEND PAGES
    # ---------------------------------------------------------
    "index.php": """<?php require 'connect.php'; 
$settings = getSetting($conn);
?>
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php echo $settings['school_name_th']; ?></title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="assets/css/style.css" rel="stylesheet">
</head>
<body>
    <?php include 'includes/navbar.php'; ?>

    <section class="hero d-flex align-items-center">
        <div class="container text-center z-1">
            <h1 class="display-4 fw-bold mb-3"><?php echo $settings['school_name_th']; ?></h1>
            <p class="lead mb-4 opacity-75">"<?php echo $settings['vision']; ?>"</p>
            <a href="about.php" class="btn btn-light btn-lg rounded-pill fw-bold text-primary px-5">รู้จักโรงเรียน</a>
        </div>
    </section>

    <div class="container py-5">
        <div class="row g-5">
            <div class="col-lg-8">
                <div class="d-flex justify-content-between align-items-end mb-4">
                    <h3 class="fw-bold text-primary border-start border-4 border-primary ps-3">📰 ข่าวประชาสัมพันธ์ล่าสุด</h3>
                    <a href="news.php" class="btn btn-sm btn-outline-secondary rounded-pill">ดูทั้งหมด</a>
                </div>
                <div class="row g-4">
                    <?php
                    $stmt = $conn->query("SELECT * FROM news ORDER BY created_at DESC LIMIT 4");
                    while($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
                    ?>
                    <div class="col-md-6">
                        <div class="card news-card h-100">
                            <span class="badge bg-warning text-dark badge-cat shadow-sm"><?php echo $row['category']; ?></span>
                            <img src="uploads/<?php echo $row['cover_img']; ?>" class="card-img-top" style="height:200px; object-fit:cover;" onerror="this.src='https://via.placeholder.com/400x200'">
                            <div class="card-body">
                                <small class="text-muted">🗓 <?php echo date('d/m/Y', strtotime($row['created_at'])); ?></small>
                                <h5 class="card-title mt-2 fw-bold text-truncate"><?php echo $row['title']; ?></h5>
                                <p class="card-text text-muted small"><?php echo mb_substr($row['content'], 0, 80); ?>...</p>
                                <a href="news_detail.php?id=<?php echo $row['id']; ?>" class="stretched-link"></a>
                            </div>
                        </div>
                    </div>
                    <?php } ?>
                </div>
            </div>

            <div class="col-lg-4">
                <div class="director-card text-center p-4 mb-4">
                    <img src="uploads/<?php echo $settings['director_img']; ?>" class="rounded-circle mb-3 border border-4 border-white shadow" width="120" height="120" style="object-fit:cover;" onerror="this.src='https://via.placeholder.com/150'">
                    <h5 class="fw-bold"><?php echo $settings['director_name']; ?></h5>
                    <p class="text-muted small mb-2"><?php echo $settings['director_position']; ?></p>
                    <hr class="mx-auto" style="width: 50px;">
                    <p class="fst-italic small">"<?php echo $settings['director_msg']; ?>"</p>
                </div>

                <div class="list-group shadow-sm rounded-3 overflow-hidden">
                    <div class="list-group-item bg-primary text-white fw-bold">🔗 ลิงก์ที่น่าสนใจ</div>
                    <a href="#" class="list-group-item list-group-item-action">📝 ระบบงานทะเบียนวัดผล</a>
                    <a href="#" class="list-group-item list-group-item-action">🥗 เมนูอาหารกลางวัน</a>
                    <a href="#" class="list-group-item list-group-item-action">🚌 ข้อมูลรถรับ-ส่งนักเรียน</a>
                </div>
            </div>
        </div>
    </div>

    <?php include 'includes/footer.php'; ?>
</body>
</html>""",

    "news.php": """<?php require 'connect.php'; ?>
<!DOCTYPE html>
<html lang="th">
<head>
    <title>ข่าวประชาสัมพันธ์</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="assets/css/style.css" rel="stylesheet">
</head>
<body>
    <?php include 'includes/navbar.php'; ?>
    <div class="container py-5">
        <h2 class="fw-bold mb-4">ข่าวประชาสัมพันธ์ทั้งหมด</h2>
        <div class="row g-4">
            <?php
            $stmt = $conn->query("SELECT * FROM news ORDER BY created_at DESC");
            while($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
            ?>
            <div class="col-md-3">
                <div class="card news-card h-100">
                    <img src="uploads/<?php echo $row['cover_img']; ?>" class="card-img-top" style="height:180px; object-fit:cover;" onerror="this.src='https://via.placeholder.com/400x200'">
                    <div class="card-body">
                        <small class="text-muted"><?php echo date('d/m/Y', strtotime($row['created_at'])); ?></small>
                        <h6 class="card-title fw-bold mt-2"><?php echo $row['title']; ?></h6>
                        <a href="news_detail.php?id=<?php echo $row['id']; ?>" class="btn btn-sm btn-outline-primary mt-2 w-100">อ่านต่อ</a>
                    </div>
                </div>
            </div>
            <?php } ?>
        </div>
    </div>
    <?php include 'includes/footer.php'; ?>
</body>
</html>""",

    "contact.php": """<?php require 'connect.php'; $s = getSetting($conn); ?>
<!DOCTYPE html>
<html lang="th">
<head>
    <title>ติดต่อโรงเรียน</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="assets/css/style.css" rel="stylesheet">
</head>
<body>
    <?php include 'includes/navbar.php'; ?>
    <div class="container py-5">
        <div class="row">
            <div class="col-md-6">
                <h2 class="fw-bold text-primary">ติดต่อเรา</h2>
                <p><strong>ที่อยู่:</strong> <?php echo $s['school_name_th']; ?> อ.วานรนิวาส จ.สกลนคร</p>
                <p><strong>โทรศัพท์:</strong> <?php echo $s['phone']; ?></p>
                <div class="bg-light p-4 rounded mt-4">
                    <h5 class="fw-bold">ส่งข้อความถึงโรงเรียน</h5>
                    <form>
                        <input class="form-control mb-2" placeholder="ชื่อของคุณ">
                        <input class="form-control mb-2" placeholder="เบอร์โทรศัพท์">
                        <textarea class="form-control mb-2" rows="3" placeholder="ข้อความ"></textarea>
                        <button class="btn btn-primary w-100">ส่งข้อความ</button>
                    </form>
                </div>
            </div>
            <div class="col-md-6">
                <div class="ratio ratio-1x1 bg-secondary rounded overflow-hidden">
                    <div class="d-flex align-items-center justify-content-center text-white h-100">
                        <h4>แผนที่ Google Map</h4>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <?php include 'includes/footer.php'; ?>
</body>
</html>""",

    # ---------------------------------------------------------
    # 4. BACKEND (ADMIN) PAGES
    # ---------------------------------------------------------
    "admin/login.php": """
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <title>Admin Login</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="../assets/css/style.css" rel="stylesheet">
</head>
<body class="bg-light d-flex align-items-center justify-content-center vh-100">
    <div class="card border-0 shadow-lg p-4" style="width: 400px;">
        <div class="text-center mb-4">
            <h4 class="fw-bold text-primary">Admin Panel</h4>
            <p class="text-muted">เข้าสู่ระบบจัดการเว็บไซต์</p>
        </div>
        <form action="auth.php" method="POST">
            <div class="mb-3">
                <input type="text" name="username" class="form-control" placeholder="Username" required>
            </div>
            <div class="mb-3">
                <input type="password" name="password" class="form-control" placeholder="Password" required>
            </div>
            <button type="submit" class="btn btn-primary w-100 py-2">เข้าสู่ระบบ</button>
        </form>
        <div class="text-center mt-3"><a href="../index.php" class="text-muted small">กลับหน้าเว็บไซต์</a></div>
    </div>
</body>
</html>""",

    "admin/auth.php": """<?php
session_start();
require '../connect.php';
$u = $_POST['username'];
$p = $_POST['password'];

// ตรวจสอบ Login อย่างง่าย (ในงานจริงควรใช้ password_hash)
$stmt = $conn->prepare("SELECT * FROM admins WHERE username=:u AND password=:p");
$stmt->execute(['u'=>$u, 'p'=>$p]);

if($stmt->rowCount() > 0){
    $_SESSION['admin_id'] = $stmt->fetch()['id'];
    header("Location: dashboard.php");
} else {
    echo "<script>alert('รหัสผ่านไม่ถูกต้อง'); window.location='login.php';</script>";
}
?>""",

    "admin/nav_admin.php": """
<nav class="navbar navbar-expand navbar-dark bg-dark px-3 mb-4">
    <a class="navbar-brand" href="dashboard.php">⚙️ Admin Panel</a>
    <div class="navbar-nav ms-auto">
        <a class="nav-link text-white" href="../index.php" target="_blank">ดูหน้าเว็บ</a>
        <a class="nav-link text-danger ms-3" href="logout.php">ออกจากระบบ</a>
    </div>
</nav>""",

    "admin/dashboard.php": """<?php
session_start();
if(!isset($_SESSION['admin_id'])) { header("Location: login.php"); exit; }
require '../connect.php';
?>
<!DOCTYPE html>
<html lang="th">
<head>
    <title>Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="../assets/css/style.css" rel="stylesheet">
</head>
<body>
    <?php include 'nav_admin.php'; ?>
    <div class="container">
        <h2 class="mb-4">ยินดีต้อนรับคุณครู</h2>
        <div class="row g-4">
            <div class="col-md-4">
                <a href="manage_news.php" class="text-decoration-none">
                    <div class="card p-4 text-center text-white bg-primary h-100 hover-shadow">
                        <h1>📰</h1>
                        <h4>จัดการข่าวสาร</h4>
                        <p>เพิ่ม/ลบ/แก้ไข ข่าวประชาสัมพันธ์</p>
                    </div>
                </a>
            </div>
            <div class="col-md-4">
                <a href="manage_school.php" class="text-decoration-none">
                    <div class="card p-4 text-center text-white bg-success h-100 hover-shadow">
                        <h1>🏫</h1>
                        <h4>ข้อมูลโรงเรียน</h4>
                        <p>แก้ไขชื่อ ผอ. / วิสัยทัศน์ / ติดต่อ</p>
                    </div>
                </a>
            </div>
            <div class="col-md-4">
                <a href="#" class="text-decoration-none">
                    <div class="card p-4 text-center text-white bg-warning h-100 hover-shadow">
                        <h1>📸</h1>
                        <h4>กิจกรรม (เร็วๆนี้)</h4>
                        <p>อัปโหลดรูปภาพกิจกรรม</p>
                    </div>
                </a>
            </div>
        </div>
    </div>
</body>
</html>""",

    "admin/manage_news.php": """<?php
session_start();
if(!isset($_SESSION['admin_id'])) { header("Location: login.php"); exit; }
require '../connect.php';

// Handle Add News
if(isset($_POST['save_news'])){
    $title = $_POST['title'];
    $content = $_POST['content'];
    $cat = $_POST['category'];
    // Upload logic simplified
    $img = "news_placeholder.jpg"; // Default
    if(!empty($_FILES['img']['name'])){
        $img = time() . "_" . $_FILES['img']['name'];
        move_uploaded_file($_FILES['img']['tmp_name'], "../uploads/" . $img);
    }
    
    $stmt = $conn->prepare("INSERT INTO news (title, content, category, cover_img) VALUES (?,?,?,?)");
    $stmt->execute([$title, $content, $cat, $img]);
    echo "<script>alert('บันทึกสำเร็จ'); window.location='manage_news.php';</script>";
}

// Handle Delete
if(isset($_GET['del'])){
    $conn->prepare("DELETE FROM news WHERE id=?")->execute([$_GET['del']]);
    header("Location: manage_news.php");
}
?>
<!DOCTYPE html>
<html lang="th">
<head>
    <title>จัดการข่าว</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="../assets/css/style.css" rel="stylesheet">
</head>
<body>
    <?php include 'nav_admin.php'; ?>
    <div class="container">
        <div class="row">
            <div class="col-md-4">
                <div class="card p-3 mb-4">
                    <h5>เขียนข่าวใหม่</h5>
                    <form method="post" enctype="multipart/form-data">
                        <div class="mb-2">
                            <label>หัวข้อข่าว</label>
                            <input type="text" name="title" class="form-control" required>
                        </div>
                        <div class="mb-2">
                            <label>หมวดหมู่</label>
                            <select name="category" class="form-select">
                                <option>ประชาสัมพันธ์</option>
                                <option>วิชาการ</option>
                                <option>กิจกรรม</option>
                            </select>
                        </div>
                        <div class="mb-2">
                            <label>เนื้อหา</label>
                            <textarea name="content" class="form-control" rows="5" required></textarea>
                        </div>
                        <div class="mb-3">
                            <label>รูปปก</label>
                            <input type="file" name="img" class="form-control">
                        </div>
                        <button type="submit" name="save_news" class="btn btn-primary w-100">บันทึกข่าว</button>
                    </form>
                </div>
            </div>
            <div class="col-md-8">
                <div class="card p-3">
                    <h5>รายการข่าวทั้งหมด</h5>
                    <table class="table table-striped">
                        <thead><tr><th>ID</th><th>หัวข้อ</th><th>วันที่</th><th>จัดการ</th></tr></thead>
                        <tbody>
                            <?php
                            $news = $conn->query("SELECT * FROM news ORDER BY id DESC");
                            while($n = $news->fetch()){
                                echo "<tr>
                                    <td>{$n['id']}</td>
                                    <td>{$n['title']}</td>
                                    <td>".date('d/m/y',strtotime($n['created_at']))."</td>
                                    <td><a href='?del={$n['id']}' class='btn btn-sm btn-danger' onclick='return confirm(\"ลบ?\")'>ลบ</a></td>
                                </tr>";
                            }
                            ?>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</body>
</html>""",

    "admin/manage_school.php": """<?php
session_start();
if(!isset($_SESSION['admin_id'])) { header("Location: login.php"); exit; }
require '../connect.php';

if(isset($_POST['update_info'])){
    $name = $_POST['dir_name'];
    $pos = $_POST['dir_pos'];
    $msg = $_POST['dir_msg'];
    $vision = $_POST['vision'];
    
    // Update logic
    $sql = "UPDATE site_settings SET director_name=?, director_position=?, director_msg=?, vision=? WHERE id=1";
    $conn->prepare($sql)->execute([$name, $pos, $msg, $vision]);
    
    // Image upload check
    if(!empty($_FILES['dir_img']['name'])){
        $img = "director_" . time() . ".jpg";
        move_uploaded_file($_FILES['dir_img']['tmp_name'], "../uploads/" . $img);
        $conn->prepare("UPDATE site_settings SET director_img=? WHERE id=1")->execute([$img]);
    }
    
    echo "<script>alert('อัปเดตข้อมูลสำเร็จ'); window.location='manage_school.php';</script>";
}

$s = getSetting($conn);
?>
<!DOCTYPE html>
<html lang="th">
<head>
    <title>ตั้งค่าข้อมูลโรงเรียน</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="../assets/css/style.css" rel="stylesheet">
</head>
<body>
    <?php include 'nav_admin.php'; ?>
    <div class="container">
        <div class="card p-4 mx-auto" style="max-width:600px;">
            <h4 class="mb-3">แก้ไขข้อมูลพื้นฐาน / ผู้อำนวยการ</h4>
            <form method="post" enctype="multipart/form-data">
                <div class="mb-3">
                    <label>วิสัยทัศน์โรงเรียน</label>
                    <textarea name="vision" class="form-control" rows="3"><?php echo $s['vision']; ?></textarea>
                </div>
                <hr>
                <div class="mb-3">
                    <label>ชื่อผู้อำนวยการ</label>
                    <input type="text" name="dir_name" class="form-control" value="<?php echo $s['director_name']; ?>">
                </div>
                <div class="mb-3">
                    <label>ตำแหน่ง</label>
                    <input type="text" name="dir_pos" class="form-control" value="<?php echo $s['director_position']; ?>">
                </div>
                <div class="mb-3">
                    <label>คำขวัญ/สารจาก ผอ.</label>
                    <textarea name="dir_msg" class="form-control" rows="2"><?php echo $s['director_msg']; ?></textarea>
                </div>
                <div class="mb-3">
                    <label>เปลี่ยนรูป ผอ. (ปล่อยว่างถ้าไม่เปลี่ยน)</label>
                    <input type="file" name="dir_img" class="form-control">
                </div>
                <button type="submit" name="update_info" class="btn btn-success w-100">บันทึกการเปลี่ยนแปลง</button>
            </form>
        </div>
    </div>
</body>
</html>""",

    "admin/logout.php": "<?php session_start(); session_destroy(); header('Location: login.php'); ?>",
}

def create_project():
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
        # Create subfolders
        os.makedirs(os.path.join(base_dir, "admin"), exist_ok=True)
        os.makedirs(os.path.join(base_dir, "assets/css"), exist_ok=True)
        os.makedirs(os.path.join(base_dir, "assets/img"), exist_ok=True)
        os.makedirs(os.path.join(base_dir, "includes"), exist_ok=True)
        os.makedirs(os.path.join(base_dir, "uploads"), exist_ok=True)
        print(f"📂 สร้างโฟลเดอร์หลัก: {base_dir}")

    for filepath, content in files.items():
        full_path = os.path.join(base_dir, filepath)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print(f"✅ สร้างไฟล์: {filepath}")

    print("-" * 30)
    print(f"🎉 เสร็จสิ้น! ย้ายโฟลเดอร์ '{base_dir}' ไปที่ MAMP htdocs ได้เลย")

if __name__ == "__main__":
    create_project()
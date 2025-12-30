-- Script untuk menambahkan default app settings
-- Database: comparely
-- Tanggal: 2025-12-24

USE comparely;

-- Hapus data lama jika ada (untuk re-run script)
DELETE FROM app_settings WHERE `key` IN (
    'site_name',
    'site_description', 
    'maintenance_mode',
    'max_comparison',
    'items_per_page',
    'enable_ai',
    'enable_notifications',
    'session_timeout',
    'max_upload_size',
    'default_currency'
);

-- Insert default settings
INSERT INTO app_settings (`key`, `value`, `description`, created_at, updated_at) VALUES
('site_name', 'COMPARELY', 'Nama aplikasi', NOW(), NOW()),
('site_description', 'Platform Perbandingan Perangkat Terlengkap', 'Deskripsi aplikasi', NOW(), NOW()),
('maintenance_mode', 'false', 'Mode maintenance - set true untuk maintenance', NOW(), NOW()),
('max_comparison', '5', 'Maksimal jumlah device untuk compare sekaligus', NOW(), NOW()),
('items_per_page', '20', 'Jumlah item per halaman untuk pagination', NOW(), NOW()),
('enable_ai', 'true', 'Aktifkan fitur AI recommendation', NOW(), NOW()),
('enable_notifications', 'true', 'Aktifkan sistem notifikasi', NOW(), NOW()),
('session_timeout', '3600', 'Session timeout dalam detik (default: 1 jam)', NOW(), NOW()),
('max_upload_size', '5242880', 'Maksimal ukuran upload dalam bytes (default: 5MB)', NOW(), NOW()),
('default_currency', 'IDR', 'Mata uang default untuk harga', NOW(), NOW());

-- Tampilkan hasil
SELECT * FROM app_settings ORDER BY `key`;

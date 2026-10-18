# Thông tin bìa và phần mở đầu báo cáo

- **Trường / Khoa**: Học viện Kỹ thuật Mật mã — Khoa Công nghệ Thông tin (đã có sẵn trên bìa, giữ nguyên)
- **Tên môn học**: Lập trình Android nâng cao
- **Tên đề tài**: Xây dựng ứng dụng theo dõi sức khỏe và luyện tập Fitness Tracker trên nền tảng Android tích hợp trí tuệ nhân tạo Gemini
- **Nhóm**: L02 (đã có sẵn trên bìa, giữ nguyên)
  - Trần Mạnh Cường — CT070109
  - Trần Hoàng Dũng — CT070115
  - Đỗ Ngọc Huy — CT070132
- **Giảng viên hướng dẫn**: *để trống* — trên bìa giữ nguyên dòng "Giảng viên hướng dẫn:" và thêm dấu chấm `……………………` để điền tay sau. Trong Lời cảm ơn viết "thầy/cô giảng viên bộ môn Lập trình Android nâng cao", không ghi tên.
- **Địa điểm, năm**: Hà Nội, 2026 (chỉ một dòng)
- **Ảnh chụp màn hình**: chưa có, sẽ chụp sau. Trong báo cáo để khung giữ chỗ và ghi rõ cần chụp gì (xem `docs/antigravity-report-plan.md` mục E, quy tắc ảnh).

## Môi trường phát triển & kết quả thử nghiệm (dữ kiện đã xác minh — dùng cho mục 1.5 và 5.1–5.3)

Các số liệu dưới đây do nhóm chạy thực tế ngày 08/10/2026, **không có trong `docs/analysis`**; writer Chương 1 và Chương 5 lấy từ đây.

| Hạng mục | Giá trị |
|---|---|
| Hệ điều hành máy phát triển | Windows 11 (24H2) |
| Flutter SDK / Dart | Flutter 3.47.6 (stable) / Dart 3.13.5 |
| JDK dùng để build Android | Eclipse Temurin JDK 21 (Gradle 8.14 chưa tương thích JDK 25) |
| Gradle / Android Gradle Plugin / Kotlin | 8.14 / 8.11.1 / 2.2.20 |
| Android SDK | compileSdk theo Flutter, build-tools 36.0.0, `minSdk = 26` (Android 8.0) |
| Phân tích tĩnh | `flutter analyze`: No issues found |
| Kiểm thử tự động | `flutter test`: 123/123 test case đạt (17 file trong `test/`) |
| Bản build | APK debug (`flutter build apk --debug --dart-define-from-file=.env`), dung lượng ~204 MB |
| Thiết bị thật | Xiaomi, model 25053RT47C, HyperOS 3.0, Android 16 (API 36), có Google Play Services |
| Cách cài đặt | `adb install` qua gỡ lỗi không dây (Wireless debugging) |
| Kết quả chạy | Ứng dụng khởi chạy bình thường, logcat không có lỗi `FATAL`/`AndroidRuntime` của ứng dụng |
| Mô hình AI | `gemini-3.8-flash`, dự phòng `gemini-3.7-flash` (bản cũ dùng `gemini-2.0-flash` và `gemini-1.5-flash` đã bị Google ngừng, khiến AI lỗi — nhóm đã cập nhật) |

Vấn đề gặp khi triển khai (có thể nêu ở mục 5.3/5.4):
- Đăng nhập Google lỗi trên bản build ở máy này: SHA-1 khóa debug của máy (`5E:1E:10:40:…`) chưa được đăng ký trong Firebase (chỉ có `DA:A6:36:29:…`). Chế độ Khách hoạt động bình thường.
- HyperOS có thể dừng service chạy nền: cần bật Tự khởi động và đặt pin "Không hạn chế" cho ứng dụng.
- Chưa kiểm thử đầy đủ chức năng AI trên máy thật vì cần khóa Gemini API thật — ghi [CẦN BỔ SUNG] nếu nhóm chưa thử.

## Tên đề tài dự phòng (nếu muốn đổi)

1. Phát triển ứng dụng Android hỗ trợ luyện tập và dinh dưỡng thông minh ứng dụng trí tuệ nhân tạo
2. Ứng dụng di động theo dõi sức khỏe cá nhân Fitness Tracker kết hợp trợ lý AI trên hệ điều hành Android

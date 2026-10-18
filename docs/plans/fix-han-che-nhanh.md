# Kế hoạch sửa nhanh các hạn chế trong báo cáo v4 (mục 5.4)

Tiêu chí "sửa nhanh": sửa ít code (≤ ~40 dòng, không đổi kiến trúc, không cần tài khoản/khóa bên ngoài), kiểm được trên Xiaomi qua adb, và báo cáo chỉ cần bỏ dòng hạn chế + chỉnh 1–2 câu mô tả.

## Nhóm A — sửa ngay

| # | Hạn chế | Sửa ở đâu | Công sức | Kiểm trên máy | Báo cáo cần đổi |
|---|---|---|---|---|---|
| A1 | (10c) Chuỗi giao diện chưa dịch | `quick_favorites_food_bar.dart:391,410,439` ("Món Ăn Quen Thuộc", "Thêm món", gợi ý trống), `profile_health_connect_card.dart:326` (nút KẾT NỐI HEALTH CONNECT), `ai_chat_history_screen.dart:259` ("Cloud Firestore Sync" hiện cả ở chế độ Khách), `en.json` `streak_days` "{count} Days" → số ít/nhiều | ~10 dòng + key vào `vi.json`/`en.json` | Đổi EN/VI, chụp lại | Bỏ phần "chuỗi chưa qua LocaleService" ở hạn chế 10 |
| A2 | (10b) Chat AI hiện Markdown thô | `ai_nutritionist_chat_dialog.dart`, `ai_chat_history_screen.dart`: hiển thị in đậm `**…**`, gạch đầu dòng `*`/`-` bằng `Text.rich` tự viết (không thêm package; `flutter_markdown` đã ngừng phát triển) | ~25 dòng (1 hàm dùng chung) | Hỏi chat, chụp | Bỏ phần "Markdown thô" ở hạn chế 10 |
| A3 | (10a) Nội dung AI trả tiếng Anh | `gemini_service.dart`: thêm câu chỉ định ngôn ngữ theo `LocaleService.isVietnamese` vào các prompt (giữ nguyên khóa JSON tiếng Anh). Đã đo: hỏi bằng tiếng Việt thì model trả tên món tiếng Việt | ~10 dòng (1 hàm `_langHint()` + chèn vào 8 prompt) | Quét ảnh / nhập món / tạo bài tập | Bỏ hạn chế 10; sửa câu cuối 4.4.4 |
| A4 | (11) Nhật ký bài tập lưu reps mục tiêu | `active_workout_screen.dart`: cộng dồn `_currentReps` mỗi khi xong hiệp (dòng ~313) và khi kết thúc; truyền số hiệp đã tập + reps trung bình/tổng vào `logCompletedWorkout` (dòng 409) | ~10 dòng | Tập 1 hiệp đếm 3 reps → kiểm `workout_logs` | Bỏ hạn chế 11; sửa câu "lưu theo giá trị mục tiêu" ở 4.2.3 |
| A5 | (5, một phần) Gửi Firestore 2 lần | Xóa `FirestoreService().saveWorkoutLog` (`storage_service.dart:1087`) và `saveFoodLog` (`:1396`) vì Repository đã gửi | 2 dòng | Không kiểm được trên máy (cần đăng nhập Google); chạy `flutter test` | Hạn chế 5 chỉ còn "StorageService quá tải" |
| A6 | (12) Mã vạch chỉ quét trực tiếp | `barcode_scanner_sheet.dart`: nút "Chọn ảnh" → `image_picker` (đã có) → `_scannerController.analyzeImage(path)` (có trong mobile_scanner 7) → `_handleBarcodeDetected` | ~35 dòng | Đẩy ảnh EAN-13 Nutella vào thư viện, quét → 539 kcal | Bỏ hạn chế 12; thêm 1 câu ở 3.9.1 |
| A7 | (7) BiometricGate không khóa lại | `biometric_gate.dart`: ghi thời điểm `paused`; khi `resumed` sau > 30 s thì đặt `_isLocked = true` và hỏi lại. Khoảng ân hạn để chọn ảnh/camera/Health Connect không bị hỏi vân tay | ~15 dòng | Cần bạn quét vân tay (rời app > 30 s rồi quay lại) | Bỏ hạn chế 7; sửa đoạn hạn chế ở 3.8.2 |

Thứ tự gợi ý: A1 → A2 → A3 → A4 → A5 → A6 → A7 (từ dễ đến cần thao tác tay). Sau mỗi mục: `flutter analyze` + `flutter test`; gom build/cài 1–2 lần, kiểm trên máy, rồi cập nhật `md/` và dựng lại v4 một lần ở cuối.

## Nhóm B — để nguyên là hạn chế (không sửa nhanh được)

| # | Hạn chế | Lý do |
|---|---|---|
| 1 | Race condition SharedPreferences | Phải đổi kiến trúc (Room/ContentProvider) và gộp 3 bản logic đếm bước |
| 2 | Phụ thuộc cảm biến, chính sách pin OEM | Do phần cứng/hệ điều hành, không sửa bằng code |
| 3 | Release ký bằng debug key | Code ~15 dòng nhưng cần tạo keystore thật, giữ bí mật, và đổi SHA-1 trên Firebase — cần quyết định của nhóm |
| 4 | AI phụ thuộc đám mây | Cần mô hình on-device (Gemini Nano/AICore) |
| 5 | `StorageService` > 2.200 dòng | Tái cấu trúc lớn (phần gửi trùng đã tách ra A5) |
| 6 | Đồng bộ chưa xử lý xung đột, chưa có GPS, chưa dọn ảnh | Tính năng mới |
| 8 | Chưa có test Kotlin | Cần dựng JUnit/Robolectric trong Gradle — làm được nhưng không phải "sửa nhanh" |
| 9 | Nước/chat chưa lưu SQLite | Nhóm đã quyết định giữ nguyên |

Sau nhóm A, mục 5.4 còn 8 hạn chế (1, 2, 3, 4, 5-rút gọn, 6, 8, 9).

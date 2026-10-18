# Kế hoạch viết lại báo cáo — bản v4

Mục tiêu: báo cáo mô tả **đúng trạng thái hiện tại** của mã nguồn (nhánh `report`, commit `99c3d3d`) và kết quả chạy thật trên Xiaomi 25053RT47C ngày 18/10/2026. Báo cáo **không** nhắc tới việc đã sửa lỗi gì — chỉ trình bày ứng dụng như nó đang là.

Nguồn chi tiết: [kiem-chung-v3.md](kiem-chung-v3.md) (bằng chứng, số liệu, đường dẫn code).

## 0. Cách làm

- **Sửa nguồn Markdown, không sửa tay file Word.** `ADRnangcaobaocao_v3.docx` được dựng từ `md/*.md` bằng `build_report.py` (chỉ khác v2 ở trang bìa/danh sách tác giả và danh mục hình đã cập nhật F9). Sửa trong Word sẽ mất khi dựng lại.
- Dựng bản mới thành `ADRnangcaobaocao_v4.docx` (đổi `OUTPUT_PATH` trong `build_report.py`, dòng 38).
- **Trang bìa + tác giả**: đưa phần đã sửa tay ở v3 (Nguyễn Huy Hoàng CT070221, Trần Hoàng Dũng CT070115, Đỗ Ngọc Huy CT070132, Trần Mạnh Cường CT070109) vào file mẫu `goc/ADRnangcaobaocao.docx` và danh sách tên ở `md/00-loi-cam-on.md` (đang thiếu mã SV, thiếu Nguyễn Huy Hoàng), để không phải sửa tay lại mỗi lần dựng.
- Ảnh: chép ảnh từ `img/demo/` sang `img/` đúng tên mà Markdown đang chờ (mục 3) — script tự thay khung giữ chỗ.
- Sau khi dựng: mở Word → F9 cập nhật mục lục/danh mục hình → chạy `verify_report.py`.

## 1. Thay đổi nội dung theo từng file

### `md/01-loi-mo-dau.md` — Lời mở đầu

- AI: "gemini-3.8-flash, dự phòng gemini-3.7-flash" → **chuỗi 3 tầng `gemini-3.8-flash` → `gemini-3.7-flash` → `gemini-2.5-flash`**.
- "mô phỏng động học 18 khớp xương của 22 bài tập" → **18 khớp, 21 động tác có hoạt cảnh** (enum `AnatomyExerciseType` có 22 giá trị gồm `general`); danh mục bài tập trên app có **17 bài** (9 tự do + 8 tạ đơn).
- "SQLite gồm 7 bảng" → giữ, nhưng nói rõ dữ liệu cục bộ nằm ở **SQLite + SharedPreferences** (xem 2.3 bên dưới).

### `md/10-chuong-1.md` — Chương 1

- 1.2.2 (Activity): "MainActivity kế thừa FlutterActivity" → **`FlutterFragmentActivity`**; thêm 1 câu lý do: plugin `health` cần `ActivityResultLauncher` để mở hộp thoại quyền Health Connect, `local_auth` cần `FragmentActivity` cho BiometricPrompt.
- Bảng 1.1: dòng `google_generative_ai` ghi chuỗi 3 model.
- 1.5: giữ nguyên (Flutter 3.47.6, Dart 3.13.5, JDK 21, Gradle 8.14, AGP 8.11.1, Kotlin 2.2.20, APK ~204 MB, analyze 0 issue, 123/123 test — **đã xác minh lại, vẫn đúng**).

### `md/20-chuong-2.md` — Chương 2

- 2.1.1 / Bảng 2.1 (F-09): Gemini chuỗi 3 tầng.
- **2.3 lớp 4 (Local Storage)** — viết đúng phân chia hiện tại:
  - SQLite: `food_entries`, `workout_logs`, `body_measurements`, `favorite_foods`, `progress_photos` là nơi lưu chính (đã kiểm có bản ghi thật).
  - Lịch sử nước uống và lịch sử chat AI: luồng giao diện lưu qua `StorageService` vào **SharedPreferences** (`daily_water_history`, `ai_chat_history`, danh sách JSON); bảng SQLite `daily_water_history`, `chat_messages` được `WaterRepository`/`ChatRepository` dùng khi hợp nhất dữ liệu từ Firestore.
  - ⚠ Quyết định cần chốt trước khi viết: giữ mô tả trung thực như trên, **hoặc** sửa code cho nước/chat ghi vào SQLite rồi giữ câu "SQLite 7 bảng" (xem mục 4).
- 2.3 lớp 6: thêm `gemini-2.5-flash`.
- 2.5.1: `workout_logs.duration` lưu **phút** (không phải giây).
- Bảng 2.5 — sửa tên khóa cho khớp code: `flutter.isGuestMode` → **`flutter.is_guest_mode`**; `flutter.biometric_enabled` → **`flutter.biometric_app_lock_enabled`**; thêm `flutter.app_language`.
- 2.5.2: khối code debounce ghi "(rút gọn)" hoặc dán nguyên văn `step_repository.dart:119-131` (tên biến thật `_lastPersistedSteps`, `_lastPersistTime`).
- 2.5.3: `/users/{uid}/chat_history` → **`ai_chat_history`**; bổ sung `daily_summaries`, `settings`. Thêm 1 câu: tính năng đồng bộ chỉ chạy khi đã đăng nhập Google (xem 5.3.3).
- 2.6 bước 3 (BiometricGate): giữ nguyên.

### `md/30-chuong-3.md` — Chương 3

- 3.1.2: giữ (thuật toán khớp code, dịch vụ chạy thật `types=0x100`).
- Hình 3.2 (mô tả ảnh): thông báo đếm bước hiển thị "Hôm nay: N / 10000 bước (x%)", **không có thanh tiến độ** (thanh tiến độ chỉ có ở thông báo nghỉ hiệp).
- 3.3.1: khối XML widget → `minWidth="180dp"`, `minHeight="90dp"`, thêm `targetCellWidth="4"`, `targetCellHeight="2"`. Thêm ý kỹ thuật: RemoteViews chỉ cho phép một số lớp (LinearLayout, FrameLayout, TextView, ImageView, ProgressBar…) — layout widget dùng `FrameLayout` có nền màu làm đường kẻ thay cho `View` (lớp `View` bị launcher từ chối: "Class not allowed to be inflated").
- 3.4.2: nhắc nước từ 08:00, chu kỳ 1/2/3 giờ (mặc định 2 giờ → 7 mốc 08:00–20:00; 1 giờ → 14 mốc 08:00–21:00). Có thể thêm kết quả `dumpsys alarm`: `RTC_WAKEUP`, `window=0`, `flags=0x5` (cho phép khi Doze).
- 3.4.3: giữ (đã kiểm: thông báo "Đang nghỉ giữa hiệp: 55s" có thanh tiến độ).
- 3.5.2: thêm 1 câu thực tế: trên HyperOS, intent `ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` mở trang **Battery details của MIUI** thay cho hộp thoại chuẩn Android (ảnh `chup-hyperos-battery.png`).
- **3.7 Health Connect**:
  - Quyền: thêm **`health.READ_ACTIVE_CALORIES_BURNED`** (code đọc `ACTIVE_ENERGY_BURNED`); 3.7.2 bước 3 sửa "TOTAL_CALORIES_BURNED" → "ACTIVE_ENERGY_BURNED (calo hoạt động)".
  - 3.7.1 thêm: khai báo `activity-alias ViewPermissionUsageActivity` với `VIEW_PERMISSION_USAGE` + `HEALTH_PERMISSIONS` (bắt buộc trên Android 14+ để Health Connect hiện hộp thoại cấp quyền) — trích `AndroidManifest.xml`.
  - Thêm ảnh hộp thoại cấp quyền Health Connect (`chup-health-connect-permission.png`).
- 3.8.2: giữ hạn chế không khóa lại khi `paused`; thêm: hộp thoại vân tay là cửa sổ hệ thống nên khi đóng app nhận `resumed` trước khi `authenticate()` trả kết quả — BiometricGate dùng cờ `_isAuthenticating` để không mở hộp thoại lần hai. Hộp thoại được bảo vệ chụp màn hình (FLAG_SECURE).
- 3.9.1 bước 4: bỏ "rung HapticFeedback, tạm dừng luồng quét" → "khi nhận được mã, ứng dụng khóa xử lý (`_isProcessing`) để không gọi API trùng, rồi truy vấn Open Food Facts". Tên lớp `BarcodeScannerSheet`. Ghi rõ: quét bằng camera trực tiếp (chưa hỗ trợ chọn ảnh mã vạch từ thư viện).
- 3.9.2: quyền micro được xin **khi khởi tạo dịch vụ giọng nói lúc mở Dashboard** (`_initSpeech` trong `initState`), không phải lúc bấm micro.
- Bảng 3.1: thêm `health.READ_ACTIVE_CALORIES_BURNED`; ghi chú `USE_BIOMETRIC` do plugin `local_auth` khai báo (gộp vào manifest khi build).
- 3.10.2:
  - Câu "just-in-time": đúng cho ACTIVITY_RECOGNITION (khi dựng widget bước) và CAMERA (khi mở trình quét); POST_NOTIFICATIONS xin ngay khi khởi động; RECORD_AUDIO xin khi mở Dashboard.
  - Kết quả `dumpsys`: `isForeground=true`, **`types=0x00000100`** (= `FOREGROUND_SERVICE_TYPE_HEALTH`), kênh `StepCounterChannel` — dùng đúng chuỗi in ra thay vì `foregroundServiceType=health`.
  - Lệnh giả lập `am broadcast BOOT_COMPLETED`: **bị hệ thống từ chối** trên Android 16 không root (`SecurityException: Permission Denial`) → thay bằng kiểm tra thật: `adb reboot` rồi `dumpsys activity services`.
  - Kiểm quyền: dùng `adb shell dumpsys package com.nhh031.fitness_tracker | findstr granted` (ACTIVITY_RECOGNITION không hiện trong `cmd appops`).

### `md/40-chuong-4.md` — Chương 4

- 4.1.1: thêm thẻ "AI ghi nhận món ăn" (mục tiêu kcal lấy từ hồ sơ — hiện 2152 kcal).
- 4.1.3: bỏ "bảng `water_logs`" và "`setWaterCupsByDate()`" → `StorageService.addWaterCup()` / `addWaterCupForDate()` / `getWaterCupsByDate()`, lưu SharedPreferences (`water_cups_today`, `daily_water_history`) để App Widget đọc trực tiếp; `checkAndResetWaterDaily()` chốt sổ ngày cũ.
- 4.1.4: biểu đồ mặc định là **"24h Hôm nay"** (đường nạp/tiêu theo giờ, chấm tròn thời điểm hiện tại), có tab "7 Ngày (Tuần)" và "Cân nặng".
- Bảng 4.2: Hít đất mặc định **3 × 15**; các dòng tạ đơn khớp app (Đẩy ngực 3×12 10 kg, 115 kcal). Thêm câu: danh mục 17 bài, lọc Tự do (9) / Tạ đơn (8).
- 4.2.3: giữ Progressive Overload (đã thấy chạy: "Buổi trước: 10.0kg × 10 reps → Hôm nay: +1 rep hoặc +1–2.5kg" — ảnh `chup-progressive-overload.png`). Bổ sung hộp thoại hoàn thành (kcal, thời gian, sets×reps, mức tạ — `chup-workout-complete.png`). Thêm mục **AI Huấn luyện viên tạo bài tập** (chọn thời gian + mục tiêu + dụng cụ → Gemini sinh danh sách động tác — `chup-ai-workout-generator.png`).
- **4.3.2 Gemini Vision** — viết lại đoạn "Model Fallback" và thay khối code `_generateWithFallback` bằng bản hiện tại (`gemini_service.dart`: `_modelChain` + vòng lặp, timeout riêng từng tầng). Số liệu đo thực tế (18/10): `gemini-2.5-flash` 6/6 thành công, 3,3–7,5 s; 3.8/3.7 lúc tải cao trả 503/429 hoặc treo — chuỗi tự chuyển tầng; kết quả trên máy: "Phở Bò Tái Nạm" 570 kcal sau ~17 s (`chup-ai-food-scanner.png`). Thêm nhập bằng văn bản ("2 quả trứng ốp la và 1 bánh mì" → 410 kcal, lưu `food_entries`).
- Bảng 4.3: cột Gemini → "chuỗi 3.8 → 3.7 → 2.5-flash; thường 3–7 s".
- 4.4.1: hồ sơ lưu **SharedPreferences (`user_profile`, JSON)**, không phải "bảng `user_profile` SQLite". Ví dụ số liệu thật: 175 cm/70 kg/24 tuổi → BMI 22,9; BMR 1679; TDEE 2602; mục tiêu 2152 kcal. US Navy: eo 82/cổ 38 → 14,5 % (`chup-body-measurements.png`).
- 4.4.2: nói rõ **hai lớp huy hiệu**: 9 huy hiệu của `AchievementService` (Bảng 4.4, hộp thoại mở khóa) và thẻ "Huy hiệu thành tích" ở tab Hoạt động (`badges_achievement_widget.dart`: 10k bước, Cardio, Bình minh, Ngọn lửa). `fat_burner` chỉ tính khi trong ngày đã ghi món ăn.
- 4.4.4: giữ; thêm ảnh giao diện tiếng Anh (`chup-profile-english.png`).
- Thêm (tùy chọn) 4.3.x **Chuyên gia dinh dưỡng AI + lịch sử tư vấn** (`chup-ai-chat.png`, `chup-ai-chat-history.png`).

### `md/50-chuong-5.md` — Chương 5

- 5.1: giữ (123/123, 17 tệp, analyze 0 issue — vẫn đúng).
- 5.2: giữ; ảnh GitHub Actions chỉ có sau khi push nhánh.
- Bảng 5.2: giữ (đúng thiết bị, đúng APK ~204 MB, logcat không FATAL).
- 5.3.2: thay bằng kết quả thật — dịch vụ `isForeground=true types=0x100`; `dumpsys appwidget` thấy provider đăng ký (`updatePeriodMillis=1800000`); quyền đã cấp (ACTIVITY_RECOGNITION, POST_NOTIFICATIONS, CAMERA, RECORD_AUDIO) qua `dumpsys package`; lịch nhắc nước trong `dumpsys alarm`.
- **5.3.3** viết lại:
  1. Đăng nhập Google: dùng đoạn ngắn đã thống nhất (SHA-1 máy build chưa đăng ký → chưa hoàn tất; chức năng chạy đủ ở chế độ Khách; **đồng bộ Firestore chưa kiểm chứng trên thiết bị**).
  2. HyperOS: dịch vụ không tự chạy lại sau khi cập nhật/khởi động nếu chưa bật Autostart (đã quan sát thực tế).
  3. Bỏ ý "AI chưa kiểm thử trên máy thật" — thay bằng kết quả đo ở 4.3.2.
- **5.4 hạn chế** — cập nhật theo hiện trạng:
  - Giữ: race condition SharedPreferences, phụ thuộc cảm biến/OEM, release dùng debug key, `StorageService` quá lớn, BiometricGate không khóa lại khi `paused`, thiếu test Kotlin, hợp nhất LWW + chưa có GPS.
  - Sửa ý "Gemini 1,5–3 s": độ trễ phụ thuộc tải máy chủ (3–7 s bình thường, có thể > 20 s khi model preview quá tải; app tự chuyển model).
  - Thêm: nước uống & chat lưu SharedPreferences (nếu không sửa code); nội dung AI trả về tiếng Anh khi app đang tiếng Việt; chat hiển thị Markdown thô; quét mã vạch chỉ qua camera trực tiếp; nhật ký bài tập lưu số rep mục tiêu thay vì số rep đã đếm; vài chuỗi giao diện chưa qua `LocaleService` (bản EN); nhận dạng giọng nói và quét mã vạch chưa kiểm trên thiết bị.
- Bảng 5.3: đồng bộ với danh sách trên.

### `md/95-phu-luc.md` — Phụ lục

- Bảng A.1: thêm `health.READ_ACTIVE_CALORIES_BURNED`; ghi chú `USE_BIOMETRIC` từ plugin.
- Bảng C.1: thay 2 dòng `am broadcast BOOT_COMPLETED / MY_PACKAGE_REPLACED` bằng `adb reboot` + `dumpsys activity services`; dòng kiểm quyền dùng `dumpsys package … | findstr granted`; thêm `adb shell dumpsys alarm | findstr fitness_tracker` (lịch nhắc nước) và `adb logcat -b crash`; kết quả `dumpsys` ghi `types=0x00000100`.

## 2. Bảng ánh xạ ảnh

| Tên Markdown đang chờ (`img/`) | Lấy từ `img/demo/` | Trạng thái |
|---|---|---|
| `chup-step-notification.png` | — | **Đã đặt vào `img/`** ("Hôm nay: 20 / 10000 bước", chỉ cắt dòng của app) |
| `chup-dashboard.png` | — | **Đã đặt vào `img/`** (cân bằng calo, Điểm sức khỏe 36/100, vòng 20 bước) |
| `chup-workout-anatomy.png` | `chup-workout-anatomy.png` | Có |
| `chup-workout-detail.png` | `chup-workout-detail.png` | Có |
| `chup-nutrition-tab.png` | `chup-nutrition-tab.png` hoặc `chup-nutrition-meal-logged.png` | Có |
| `chup-ai-food-scanner.png` | `chup-ai-food-scanner.png` | Có (Phở Bò Tái Nạm 570 kcal) |
| `chup-profile-settings.png` | `chup-profile-settings.png` | Có |
| `chup-adb-dumpsys.png`, `chup-adb-dumpsys-service.png` | — | **Đã đặt vào `img/`** (dựng từ output thật của lệnh adb) |
| `chup-test-analyze.png` | — | **Đã đặt vào `img/`** (output thật: No issues found, +123 All tests passed) |
| `chup-app-widget.png` | — | **Đã đặt vào `img/`** (20 / 10.000 bước, 8 / 8 cốc) |
| `chup-barcode-scanner.png` | — | **Đã đặt vào `img/`** (Nutella 3017620422003, 539 kcal) |
| `chup-biometric-prompt.png` | — | **Không chụp được** (cửa sổ bảo mật FLAG_SECURE, adb ra màn hình đen) → bỏ khung Hình 4.8, mô tả bằng chữ |
| `chup-github-actions.png` | — | Cần push nhánh để CI chạy |

Ảnh mới nên thêm vào Markdown (đã có trong `img/demo/`): `chup-rest-timer-notification.png` (3.4.3), `chup-hyperos-battery.png` (3.5.2), `chup-health-connect-permission.png` (3.7), `chup-calories-chart-24h.png` (4.1.4), `chup-progressive-overload.png`, `chup-workout-complete.png`, `chup-ai-workout-generator.png` (4.2.3), `chup-nutrition-meal-logged.png`, `chup-ai-chat.png`, `chup-ai-chat-history.png` (4.3), `chup-body-measurements.png` (4.4.1), `chup-profile-english.png` (4.4.4).

## 3. Thứ tự thực hiện

1. **Chốt quyết định** (mục 4).
2. Sửa trang bìa trong `goc/` + `md/00-loi-cam-on.md`.
3. Sửa `md/` theo mục 1 (gợi ý chia: Ch1–2 · Ch3 + Phụ lục · Ch4 · Ch5).
4. Chụp các ảnh còn thiếu (widget, mã vạch, vân tay, dashboard có bước chân, terminal).
5. Chép ảnh vào `img/` theo mục 2, thêm cú pháp `![Hình x.y: …](img/…)` cho ảnh mới.
6. Đổi `OUTPUT_PATH` → v4, chạy `python build_report.py`, mở Word nhấn F9, chạy `verify_report.py`.
7. Đọc soát lần cuối các con số: 123 test / 17 tệp, 2152 kcal, 14,5 %, `types=0x100`, chuỗi model.

## 4. Quyết định cần chốt trước khi viết

| Vấn đề | Phương án A (chỉ sửa báo cáo) | Phương án B (sửa code cho khớp báo cáo) |
|---|---|---|
| Nước uống & chat lưu SharedPreferences | Mô tả đúng như hiện tại ở 2.3 / 4.1.3, nêu là hạn chế ở 5.4 | Cho `StorageService` ghi qua `WaterRepository`/`ChatRepository` vào SQLite → giữ "Local-First SQLite 7 bảng" |
| Nội dung AI trả tiếng Anh | Nêu hạn chế | Thêm ngôn ngữ hiện tại vào prompt Gemini |
| Chat hiển thị Markdown thô | Nêu hạn chế | Render Markdown (`flutter_markdown`) |
| Log bài tập lưu rep mục tiêu | Nêu hạn chế | Lưu số rep đã đếm |
| Chuỗi chưa dịch ở bản EN | Nêu hạn chế | Đưa qua `LocaleService.tr` + thêm key vào `en.json`/`vi.json` |

Khuyến nghị: B cho dòng đầu (ảnh hưởng tính đúng của kiến trúc được trình bày ở Chương 2), A cho các dòng còn lại.

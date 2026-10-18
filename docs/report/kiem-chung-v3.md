# Kiểm chứng ADRnangcaobaocao_v3.docx với mã nguồn

Ngày kiểm: 2026-10-18 · Nhánh `report` · Phương pháp: trích toàn bộ văn bản/bảng của docx, đối chiếu từng khẳng định kỹ thuật với code, chạy lại `flutter analyze` và `flutter test`.

## 1. Đã xác minh — khớp với code

| Khẳng định trong báo cáo | Bằng chứng |
|---|---|
| Flutter 3.47.6 / Dart 3.13.5, AGP 8.11.1, Kotlin 2.2.20, Gradle 8.14, minSdk 26, desugar 2.1.4 | `flutter --version`, `android/settings.gradle.kts:22-23`, `gradle-wrapper.properties:5`, `android/app/build.gradle.kts` |
| `flutter analyze` → No issues found | Chạy lại hôm nay: **No issues found** |
| 123/123 test, 17 tệp; số test theo từng nhóm ở Bảng 5.1 (15/35/18/27/17/11) | Chạy lại hôm nay: **All tests passed! (+123)**; đếm theo tệp khớp từng dòng |
| Foreground Service `health`, `START_STICKY`, batching 10 s, thuật toán baseline/reboot-offset | `StepCounterService.kt:34-134` (trích dẫn dòng chính xác) |
| BootReceiver 4 action, `startForegroundService` | `BootReceiver.kt`, `AndroidManifest.xml:71-81` |
| MethodChannel 4 phương thức, EventChannel + `RECEIVER_NOT_EXPORTED` | `MainActivity.kt:33-102` |
| Widget: `updatePeriodMillis=1800000`, `FLAG_IMMUTABLE`, hard-code "10.000" / "8 cốc" | `FitnessAppWidgetProvider.kt:30-50` |
| 16 quyền trong Manifest, `<queries>` Health Connect + RecognitionService | `AndroidManifest.xml:3-19, 99-111` |
| SQLite 7 bảng + đúng tên các index, cờ `sqlite_migrated_v1`, FFI in-memory khi `FLUTTER_TEST` | `app_database.dart:18-29, 81-295` |
| Logout xóa 7 bảng trong 1 transaction; đổi `UniqueKey` để dựng lại tab | `app_database.dart:299-310`, `main_screen.dart:37,62` |
| IndexedStack, `extendBody`, BackdropFilter blur 24 | `main_screen.dart:93-135` |
| Firestore WriteBatch ngắt ở 400 thao tác | `firestore_service.dart:499-505` |
| Gemini `gemini-3.8-flash` → fallback `gemini-3.7-flash`, nhận MIME từ byte đầu, bộ đệm **23** món | `gemini_service.dart:41-42, 76-94, 456, 158-184` |
| Open Food Facts: API v2, User-Agent, timeout 8 s, `product_name_vi` → `_en`, kJ/4.184 | `open_food_facts_service.dart:50-101` |
| Công thức: sải chân 0.415·h, 0.04 kcal/bước, BMR/1440, TDEE −450/+350/+150, US Navy | `user_metrics_service.dart` |
| Health Score 20/35/35/10, 5 bậc 90/75/60/40 | `health_score_widget.dart:76-124, 202-216` |
| 9 huy hiệu, khóa `unlocked_achievement_badges_v1`, `StreamController.broadcast` | `achievement_service.dart` |
| 18 khớp xương | `anatomy_kinematic_painter.dart:37-55` |
| BiometricGate không khóa lại khi `paused` (hạn chế tự nhận) | `biometric_gate.dart:33-37` — đúng là chỉ xử lý `resumed` |
| 3 kênh thông báo, `exactAllowWhileIdle`, `onlyAlertOnce`, `showProgress` | `notification_service.dart`, `StepCounterService.kt:180-193` |

## 2. Sai lệch cần sửa trong báo cáo

| # | Vị trí trong báo cáo | Báo cáo ghi | Thực tế trong code | Đề xuất |
|---|---|---|---|---|
| 1 | 3.7.2 bước 3, Bảng 3.1, Phụ lục A | Đọc `TOTAL_CALORIES_BURNED` | `health_sync_service.dart:84` dùng `HealthDataType.ACTIVE_ENERGY_BURNED`. Manifest chỉ khai `READ_TOTAL_CALORIES_BURNED`, **thiếu `READ_ACTIVE_CALORIES_BURNED`** | **Lỗi code thật** (xem mục 3). Sửa code cho khớp báo cáo |
| 2 | 3.3.1 (khối XML widget) | `minWidth="250dp"`, `minHeight="110dp"` | `180dp` / `90dp`, có thêm `targetCellWidth=4`, `targetCellHeight=2` (`fitness_app_widget_info.xml:3-6`) | Cập nhật khối code |
| 3 | 2.5.3 | `/users/{uid}/chat_history` | `ai_chat_history`; còn có `daily_summaries`, `settings` mà báo cáo chưa liệt kê | Sửa tên, bổ sung 2 collection |
| 4 | 4.4.1 | Hồ sơ "lưu vào bảng `user_profile` trong SQLite" | Không có bảng này; hồ sơ là JSON trong SharedPreferences khóa `user_profile` (đúng như Bảng 2.5 — báo cáo đang tự mâu thuẫn) | Sửa thành SharedPreferences |
| 5 | 4.1.3 | Ghi vào "bảng `water_logs`" qua `StorageService.setWaterCupsByDate()` | Bảng SQLite là `daily_water_history`; hàm `setWaterCupsByDate` **không tồn tại** — dùng `addWaterCup`, `addWaterCupForDate`, `getWaterCupsByDate`, `checkAndResetWaterDaily`. `water_logs` chỉ là collection Firestore | Sửa tên bảng và tên hàm |
| 6 | 3.9.1 bước 4 | Khi nhận mã: rung `HapticFeedback`, tạm dừng luồng quét | `barcode_scanner_sheet.dart:76-90, 271-280` không rung, không dừng camera, chỉ chặn bằng cờ `_isProcessing` | Bỏ câu này, hoặc thêm haptic + `controller.stop()` vào code |
| 7 | Hình 4.6 / khung ảnh | `BarcodeScannerScreen` | Lớp tên `BarcodeScannerSheet` (bottom sheet) | Sửa tên |
| 8 | Phụ lục A | `USE_BIOMETRIC` khai trong AndroidManifest.xml | Không có trong manifest của app; quyền này do plugin `local_auth` merge vào lúc build | Ghi chú "(merge từ plugin local_auth)" |
| 9 | 2.5.2 (code debounce) | Ghi "Nguồn: step_repository.dart:121-132" như trích nguyên văn | Code thật dùng `_lastPersistedSteps`/`_lastPersistTime`, có thêm `saveDailySteps`; nằm ở dòng 119-131 | Thêm "(rút gọn)" hoặc dán nguyên văn |
| 10 | 2.1.1 / F-01 | "Lọc nhiễu tối đa 5 bước/giây" như tính năng chung | Bộ lọc chỉ có trong Dart (`step_repository.dart:101-115`). Luồng Kotlin — luồng chạy khi app đóng — không lọc | Nói rõ phạm vi bộ lọc |
| 11 | Mở đầu, mục 3 | "22 bài tập" | Enum `AnatomyExerciseType` có 22 giá trị, nhưng gồm `general` (mặc định) → 21 bài cụ thể | Ghi "21 bài tập + 1 tư thế mặc định" hoặc giữ nguyên nếu chấp nhận |

## 3. Lỗi code phát hiện khi kiểm chứng

1. **Health Connect thiếu quyền** — `_dataTypes` yêu cầu `ACTIVE_ENERGY_BURNED`, nhưng Manifest không khai `android.permission.health.READ_ACTIVE_CALORIES_BURNED`. Khi bấm "Kết nối Health Connect", `requestAuthorization` có thể trả `false` hoặc bỏ qua loại dữ liệu này. Hai cách sửa: đổi sang `HealthDataType.TOTAL_CALORIES_BURNED` (khớp Manifest và báo cáo), hoặc thêm quyền vào Manifest.
2. **Rủi ro crash sau reboot (Android 14+)** — dịch vụ FGS loại `health` yêu cầu đã được cấp `ACTIVITY_RECOGNITION` lúc khởi chạy. `BootReceiver` gọi `startForegroundService` mà không kiểm tra quyền. Nếu người dùng thu hồi quyền (đúng kịch bản `pm revoke` ở Phụ lục C), lần boot sau sẽ ném `SecurityException` ở nền. Cần kiểm tra trên máy thật.

## 4. Chưa thể xác minh (cần demo trên thiết bị)

Các khẳng định sau mô tả kết quả **đã chạy trên máy thật**. Hiện chưa có bằng chứng, và báo cáo còn **13 khung giữ chỗ ảnh**:

- 1.5 / Bảng 5.2: Xiaomi 25053RT47C, HyperOS 3.0, APK ~204 MB, logcat không có FATAL.
- 3.10.2 / 5.3.2: `dumpsys` cho thấy `isForeground=true`, `foregroundServiceType=health`; `dumpsys appwidget` ra widget 4x2; appops đã cấp quyền.
- Phụ lục C: kết quả mong đợi của từng lệnh ADB (BOOT_COMPLETED, revoke quyền, run-as đọc prefs...).
- Các ảnh: notification đếm bước, App Widget, Dashboard, Workout/giải phẫu, chi tiết bài tập, Nutrition, AI food scan, barcode, Profile, BiometricPrompt, terminal analyze/test, GitHub Actions, adb dumpsys.

## 5. Kết quả demo trên Xiaomi 25053RT47C (2026-10-18)

Máy: Android 16 (API 36), HyperOS 3.0, có cảm biến `step_counter` phần cứng. Cài APK debug build từ code hiện tại (`flutter build apk --debug --dart-define-from-file=.env`, ~204 MB, phải dùng JDK 21 vì Flutter mặc định đang trỏ Java 25). Ảnh và log lưu ở `docs/report/img/demo/`.

### 5.1. Đã xác minh trên máy thật

| Khẳng định | Kết quả |
|---|---|
| Foreground Service loại health | `isForeground=true`, `types=0x00000100` (= `FOREGROUND_SERVICE_TYPE_HEALTH`), kênh `StepCounterChannel` — `adb-dumpsys-services.txt` |
| Thông báo thường trực đếm bước | Có ("Fitness Tracker • Đếm bước nền") — `chup-step-notification.png` |
| Thông báo nghỉ hiệp có thanh tiến độ | Có ("Đang nghỉ giữa hiệp: 55s" + progress) — `chup-rest-timer-notification.png` |
| AuthGate → Login → Guest → Onboarding → MainScreen | Đúng luồng mục 2.6 |
| Xin quyền đúng lúc: ACTIVITY_RECOGNITION khi dựng widget bước, CAMERA khi mở quét mã vạch | Đúng |
| SharedPreferences dùng chung (`run-as … cat FlutterSharedPreferences.xml`) | Có `today_steps`, `water_cups_today`, `step_baseline_*`, `step_reboot_offset` kiểu `long` |
| Công thức BMR/TDEE/BMI/mục tiêu | BMR 1679, TDEE 2602 (×1,55), mục tiêu 2152 (−450), BMI 22,9 — khớp công thức |
| Mô hình giải phẫu 2D, hoạt cảnh động học, đếm set/rep | Hoạt động — `chup-workout-*.png` |
| Không crash | `logcat -b crash` không có FATAL của app |
| `USE_BIOMETRIC` | Có trong `dumpsys package` (merge từ plugin) |

### 5.2. Lỗi phát hiện khi chạy thật

| # | Lỗi | Bằng chứng / nguyên nhân |
|---|---|---|
| D1 | **Health Connect không bao giờ hiện hộp thoại xin quyền**, app báo luôn "Người dùng từ chối quyền" | Log `FLUTTER_HEALTH: Permission launcher not found`. Plugin `health` (và `local_auth`) yêu cầu `MainActivity : FlutterFragmentActivity`, code đang là `FlutterActivity` (`MainActivity.kt:16`) |
| D2 | **Fallback Gemini không chạy khi model chính treo/chậm** | `analyzeFoodImage` bọc `_generateWithFallback` bằng một `.timeout(30s)` chung (`gemini_service.dart:508`). Đo bằng curl: `gemini-3.8-flash` 34–76 s (có lúc 503), `gemini-3.7-flash` ~22 s → hết 30 s trước khi kịp gọi dự phòng → "Gemini AI chưa nhận diện được món" |
| D3 | **Lần cài đầu: cấp ACTIVITY_RECOGNITION xong dịch vụ đếm bước không chạy**, phải mở lại app mới chạy | Tái hiện 2/2 lần sau khi gỡ–cài. Không có log lỗi; nghi `StepCounterWidget` bị dựng lại (đổi `_tabSessionKey` sau onboarding / dialog huy hiệu) trong lúc chờ quyền |
| D4 | **Tràn layout (RenderFlex overflow)** ở 4 chỗ | Thẻ nước (8,2–16 px khi ml ≥ 4 chữ số, `water_reminder_widget.dart:662`), chú thích biểu đồ 24h (5,2 px), tiêu đề "Phân bổ Macro" (9,4 px), tiêu đề "Hồ sơ sinh trắc học" (15 px). Ở bản release không có sọc vàng–đen nhưng nội dung bị cắt |
| D5 | Huy hiệu **"Siết mỡ siêu đẳng" mở khóa ngay lần đầu mở app** | Chưa ăn gì → thâm hụt (BMR tích lũy − 0) > 500 kcal. Tái hiện 2/2 |
| D6 | Thẻ "AI ghi nhận món ăn" dùng mục tiêu 2.000 kcal, tab Dinh dưỡng dùng 2.152 kcal | Hai nơi không dùng chung mục tiêu |
| D7 | Dịch vụ không tự chạy lại sau `adb install -r` (MY_PACKAGE_REPLACED) | HyperOS chặn Autostart — đúng như báo cáo đã cảnh báo ở 5.3.3 |

### 5.3. Điểm báo cáo cần sửa thêm sau demo

- **Phụ lục C / 3.10.2**: `am broadcast -a BOOT_COMPLETED` và `MY_PACKAGE_REPLACED` **bị từ chối** (`SecurityException: Permission Denial … uid=2000`) trên Android 16 không root. Thay bằng: khởi động lại máy thật (`adb reboot`) rồi `dumpsys activity services`.
- **5.3.2**: `cmd appops get` **không hiển thị ACTIVITY_RECOGNITION** (đó là runtime permission). Dùng `adb shell dumpsys package com.nhh031.fitness_tracker | findstr granted`.
- **5.3.2 / Hình 3.3**: `dumpsys appwidget` chỉ cho thấy provider đã đăng ký, **chưa có widget nào được đặt trên màn hình chính** → cần tự thêm widget rồi mới chụp.
- `dumpsys` in `types=0x00000100`, không in chữ `foregroundServiceType=health` → sửa câu mô tả kết quả.
- Hình 3.2 mô tả "thanh tiến độ" trong thông báo đếm bước — thông báo này **không có** progress bar (chỉ thông báo nghỉ hiệp có).
- Bảng 4.2: Hít đất mặc định **3 × 15**, không phải 3 × 12. Danh sách bài tập trên app có **17 bài** (9 tự do + 8 tạ đơn).
- 4.4.2: thẻ "Huy hiệu thành tích" ở tab Hoạt động hiển thị bộ **4 huy hiệu khác** (10k bước, Cardio, Bình minh, Ngọn lửa) ngoài bộ 9 huy hiệu ở Bảng 4.4.
- 3.5.2: trên HyperOS, `ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` mở trang **Battery details của MIUI** chứ không phải hộp thoại chuẩn — `chup-hyperos-battery.png`.

### 5.4. Chưa kiểm được (cần thao tác tay của người dùng)

- Đếm bước thật (cần đi bộ) và ảnh Dashboard/notification có số bước > 0.
- App Widget trên màn hình chính (cần tự kéo widget ra Home).
- BiometricPrompt (cần vân tay; nghi bị ảnh hưởng bởi D1).
- Quét mã vạch: trình quét chỉ dùng camera trực tiếp, không chọn ảnh từ thư viện → cần đưa camera điện thoại vào ảnh mã vạch (đã tạo sẵn EAN-13 Nutella `3017620422003`).
- BootReceiver sau khi khởi động lại máy thật.

## 6. Đã sửa D1–D6 và kiểm lại trên máy (2026-10-18)

`flutter analyze`: No issues found · `flutter test`: 123/123 pass · cài sạch (gỡ–cài) lên Xiaomi rồi kiểm lại.

| # | Sửa | Kết quả kiểm lại |
|---|---|---|
| D1 | `MainActivity : FlutterFragmentActivity`; thêm `health.READ_ACTIVE_CALORIES_BURNED` (code đọc `ACTIVE_ENERGY_BURNED`); thêm `activity-alias ViewPermissionUsageActivity` (Health Connect bắt buộc trên Android 14+) | Bấm "Kết nối Health Connect" → mở màn hình xin quyền của Health Connect (Active calories, Heart rate, Sleep, Steps) — `chup-health-connect-permission.png`. **Báo cáo cần thêm quyền READ_ACTIVE_CALORIES_BURNED vào Bảng 3.1/A.1 và sửa 3.7.2 thành ACTIVE_ENERGY_BURNED** |
| D2 | `_generateWithFallback` có timeout riêng cho model chính (20 s; 8 s cho tra cứu văn bản), timeout tổng nới lên 60 s/25 s; bản stream chuyển dự phòng khi không có chunk trong 20 s và không lặp nội dung đã trả | Log: `Model chính (gemini-3.8-flash) lỗi: TimeoutException after 0:00:20 … chuyển sang dự phòng (gemini-3.7-flash)` → cơ chế dự phòng **đã chạy**. Nhưng ảnh vẫn chưa nhận diện được vì 3.7 cũng treo (xem 6.1) |
| D3 | `StepCounterWidget`: bọc `request()` trong try/catch, tách `_startTracking()`, khởi chạy bù khi app `resumed` mà quyền đã cấp | Cài sạch → cấp quyền → `isForeground=true types=0x100` sau ~2 s (trước đây không chạy) |
| D4 | `Expanded`/`FittedBox`/ellipsis ở thẻ nước, chú thích biểu đồ 24h, tiêu đề Phân bổ Macro, tiêu đề Hồ sơ | Không còn sọc tràn ở cả 4 chỗ (kể cả 2000 ml). Nút **"Sửa"** hồ sơ trước đây bị đẩy ra khỏi màn hình nay đã hiện |
| D5 | `fat_burner` chỉ tính thâm hụt khi hôm nay đã ghi ít nhất 1 món | Cài sạch, thâm hụt 789 kcal, không còn tự mở huy hiệu. Huy hiệu "Thủy thần 8 cốc" vẫn mở đúng khi đủ 8 cốc |
| D6 | Thẻ AI ghi món dùng `profile.targetCalories`, lắng nghe `profileUpdateNotifier` | Hiện "0 / 2152 kcal", khớp tab Dinh dưỡng |

Ảnh trong `docs/report/img/demo/` đã chụp lại bằng bản đã sửa: `chup-nutrition-tab.png`, `chup-profile-settings.png`, `chup-calories-chart-24h.png`, `chup-health-connect-permission.png`, `chup-ai-chat.png`. Không có ảnh nào chứa trình chọn ảnh, danh sách tài khoản hay cuộc gọi.

### 6.1. Gemini: chat chạy, quét ảnh chưa chạy

Đo trực tiếp bằng curl, cùng API key, ảnh phở 800×600:

| Model | Văn bản | Ảnh |
|---|---|---|
| gemini-3.8-flash | 34–76 s, có lúc 503 "high demand" | Không phản hồi sau 90 s |
| gemini-3.7-flash | ~22 s | Không phản hồi sau 90 s |
| gemini-3.5-flash | — | 200 OK, ~13 s, nhận đúng phở |
| gemini-2.5-flash | — | 200 OK, ~5,6 s, nhận đúng phở |

- Chat "Chuyên gia AI": 3.8 trả 503 ngay → dự phòng 3.7 trả lời, có cá nhân hoá (nhắc 2.000 ml nước, mục tiêu 65 kg). Câu trả lời hiển thị **Markdown thô** (`**`, `*`).
- Quét ảnh: 3.8 treo 20 s → 3.7 treo nốt → rơi về nhập tay. Key không lỗi; nguyên nhân là phía Google đang quá tải xử lý ảnh trên hai model 3.8/3.7.

### 6.2. Đăng nhập Google

Chọn tài khoản xong app vẫn ở chế độ Khách, log `Google Sign-In canceled by user.` Nguyên nhân: APK ký bằng debug keystore SHA‑1 `5E:1E:10:40:83:FF:98:FA:F0:2A:AF:96:F3:A3:DC:FB:4C:76:BD:BB`, còn `google-services.json` chỉ có `DA:A6:36:29:…`. Đúng như 5.3.3 của báo cáo; cần thêm SHA‑1 trên Firebase Console rồi tải lại `google-services.json` (không sửa bằng code).

### 6.3. Thêm tầng dự phòng gemini-2.5-flash — quét ảnh đã chạy

`GeminiService` dùng chuỗi `_modelChain = [gemini-3.8-flash, gemini-3.7-flash, gemini-2.5-flash]` cho cả `_generateWithFallback` và bản stream. Hai tầng đầu có timeout riêng (20 s; 8 s cho tra cứu văn bản), tầng cuối dùng phần thời gian còn lại của timeout tổng.

Kiểm lại trên Xiaomi (analyze sạch, 123/123 test pass): chọn ảnh phở → log `gemini-3.8-flash lỗi: Server Error [503]` → `gemini-3.7-flash lỗi: Server Error [503]` → `gemini-2.5-flash` trả kết quả **"Phở Bò Tái Nạm" — 570 kcal, đạm 36 g, tinh bột 48 g, béo 23 g** sau ~17 s — `chup-ai-food-scanner.png`.

**Báo cáo cần sửa theo**: Mở đầu (mục 1, 2), Bảng 1.1, 2.1.1, 2.3 (lớp 6), 4.3.2 (đoạn "Model Fallback" và code `_generateWithFallback`), Bảng 4.3 — đổi "dự phòng hai tầng 3.8 → 3.7" thành chuỗi ba tầng 3.8 → 3.7 → 2.5-flash có timeout từng tầng.

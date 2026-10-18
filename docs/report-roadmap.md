# Lộ trình phân tích mã nguồn để viết báo cáo

Mục tiêu: trả lời "app làm được gì" và "dùng kỹ thuật Android nào, ở file nào" cho môn *Android nâng cao*. Tổng ~46.600 dòng Dart/Kotlin; **không cần đọc hết**. Lớp native Android chỉ ~600 dòng nhưng chứa phần lớn kỹ thuật Android thuần → đọc kỹ trước, phần Dart đọc theo mục đích.

## 1. Bản đồ tính năng → kỹ thuật Android → file bằng chứng

| Tính năng | Kỹ thuật Android / nền tảng | File chính |
|---|---|---|
| Đếm bước chạy nền | Foreground Service (`foregroundServiceType=health`), `SensorManager` + `TYPE_STEP_COUNTER` (batching 10 s), `START_STICKY`, Notification Channel, `PendingIntent` | `android/.../StepCounterService.kt`, `AndroidManifest.xml` |
| Tự chạy lại sau khởi động máy | `BroadcastReceiver` nghe `BOOT_COMPLETED`, `MY_PACKAGE_REPLACED`, `QUICKBOOT_POWERON` | `BootReceiver.kt` |
| Đẩy số bước lên UI Flutter | `LocalBroadcast`-kiểu `sendBroadcast` (`setPackage`) → `BroadcastReceiver` → `EventChannel` | `MainActivity.kt`, `step_counter_widget.dart` |
| Widget màn hình chính | `AppWidgetProvider`, `RemoteViews`, `appwidget-provider` XML, `updatePeriodMillis`, `PendingIntent.FLAG_IMMUTABLE` | `FitnessAppWidgetProvider.kt`, `res/layout/fitness_app_widget.xml`, `res/xml/fitness_app_widget_info.xml`, `widget_sync_service.dart` |
| Chia sẻ dữ liệu native ↔ Dart | `SharedPreferences` (`FlutterSharedPreferences`, key `flutter.*`) | `StepCounterService.kt`, `step_repository.dart` |
| Bỏ tối ưu pin | `PowerManager.isIgnoringBatteryOptimizations`, `ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` | `MainActivity.kt`, `background_service.dart`, `profile_battery_card.dart` |
| Nhắc uống nước | `flutter_local_notifications`, `zonedSchedule` + `exactAllowWhileIdle`, quyền `SCHEDULE_EXACT_ALARM`/`POST_NOTIFICATIONS`, receiver boot của plugin | `notification_service.dart`, `water_reminder_widget.dart` |
| Health Connect | Quyền `android.permission.health.*`, `<queries>`, intent `ACTION_SHOW_PERMISSIONS_RATIONALE`, plugin `health` | `health_sync_service.dart`, `profile_health_connect_card.dart` |
| Khóa app bằng sinh trắc | `BiometricPrompt` qua `local_auth`, `WidgetsBindingObserver` để khóa lại khi quay về từ nền | `biometric_service.dart`, `biometric_gate.dart` |
| Quét mã vạch / chụp ảnh món ăn | Camera (`CAMERA`), `mobile_scanner`, `image_picker` | `barcode_scanner_sheet.dart`, `ai_food_logging_widget.dart`, `meal_category_card_widget.dart` |
| Nhập liệu giọng nói | `RECORD_AUDIO`, `RecognitionService` (`<queries>`), `speech_to_text` | `speech_service.dart` |
| Đăng nhập Google + đồng bộ cloud | Firebase Auth, Google Sign-In (Credential/`serverClientId`), Cloud Firestore, `google-services` Gradle plugin | `auth_service.dart`, `firestore_service.dart`, `android/app/google-services.json` |
| AI Coach / phân tích món ăn | Gemini (`google_generative_ai`), model chính + fallback, streaming | `gemini_service.dart`, `ai_coach_card_widget.dart`, `ai_nutritionist_chat_dialog.dart` |
| Lưu trữ cục bộ | SQLite (`sqflite`), index theo ngày, migrate từ SharedPreferences | `app_database.dart`, `repositories/*`, `storage_service.dart` |
| Mô hình giải phẫu chuyển động | `CustomPainter`, `AnimationController`, động học khớp | `anatomy_kinematic_painter.dart`, `exercise_pose_widget.dart`, `muscle_anatomy_map_widget.dart` |
| Xuất báo cáo 30 ngày | `path_provider` + `share_plus` (Intent chia sẻ) | `report_export_service.dart` |
| Đa ngôn ngữ | JSON asset + `ValueNotifier` rebuild `MaterialApp` | `locale_service.dart`, `assets/i18n/*.json` |

## 2. Lộ trình đọc code (theo thứ tự)

Mỗi chặng ghi: **đọc gì → câu hỏi cần trả lời → chứng cứ nên thu thập → mục báo cáo tương ứng**.

### Chặng 0 — Chuẩn bị (≈0,5 giờ)
- Chạy app theo `README.md` (Phần A/B), ghi lại phiên bản Flutter (`flutter --version`) và thiết bị thử.
- `flutter pub deps --no-dev --style=compact` để có danh sách thư viện cho chương "Công nghệ sử dụng".
- Chụp màn hình từng tab + widget + notification foreground service.
- *Mục báo cáo*: Giới thiệu, môi trường, công cụ.

### Chặng 1 — Cấu trúc dự án & cấu hình build (≈1 giờ)
- Đọc: `pubspec.yaml`, `android/app/build.gradle.kts`, `android/build.gradle.kts`, `settings.gradle.kts`, `gradle.properties`, `.github/workflows/flutter_ci.yml`, `analysis_options.yaml`.
- Hỏi: Flutter chia thư mục nền tảng thế nào, thư mục nào do tool sinh ra (`ios/`, `macos/`, `linux/`, `windows/`, `web/`) và thư mục nào tự viết (`lib/`, `android/app/src/main`)? `minSdk 26` / `compileSdk` lấy từ đâu (`flutter.compileSdkVersion`)? Vì sao bật `coreLibraryDesugaring`? Plugin `google-services` làm gì?
- Chứng cứ: sơ đồ cây thư mục (mục "Cây thư mục" trong `CLAUDE.md`), bảng dependency chia nhóm (UI, dữ liệu, Firebase, AI, thiết bị).
- *Mục báo cáo*: Cấu trúc dự án, cấu hình & build, CI.

### Chặng 2 — Lớp native Android (≈3–4 giờ) ★ trọng tâm
Đọc theo thứ tự:
1. `AndroidManifest.xml` — liệt kê từng `<uses-permission>` và phân loại: runtime (`ACTIVITY_RECOGNITION`, `POST_NOTIFICATIONS`, `CAMERA`, `RECORD_AUDIO`), đặc biệt (`SCHEDULE_EXACT_ALARM`, `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS`), Health Connect, foreground-service. Xem `<service>`, 3 `<receiver>`, `<queries>`, `launchMode="singleTop"`, `configChanges`.
2. `MainActivity.kt` — `FlutterActivity`, `configureFlutterEngine`, `MethodChannel` (4 method), `EventChannel` + `StreamHandler`, đăng ký/huỷ `BroadcastReceiver` theo vòng đời, `RECEIVER_NOT_EXPORTED` (API 33).
3. `StepCounterService.kt` — vòng đời `onCreate → startForeground → registerListener`, batching `maxReportLatency`, `onSensorChanged`, thuật toán baseline/reboot-offset, `NotificationCompat`, `NotificationChannel` (API 26+).
4. `BootReceiver.kt` — action boot, `startForegroundService`.
5. `FitnessAppWidgetProvider.kt` + `res/layout/fitness_app_widget.xml` + `res/xml/fitness_app_widget_info.xml` + `drawable/widget_background.xml` — `RemoteViews`, `updateAppWidget`, kích thước widget (`targetCellWidth/Height`, `resizeMode`).
6. `res/values*/styles.xml`, `launch_background.xml` — Launch theme/Splash.
- Hỏi (nên trả lời bằng sơ đồ tuần tự):
  - Từ lúc cảm biến phát sự kiện đến lúc số bước hiện trên UI/Widget/Notification đi qua những thành phần nào?
  - Khi Activity bị huỷ mà Service còn chạy, dữ liệu được giữ ở đâu? (→ `SharedPreferences`)
  - Hệ quả của `START_STICKY`, của foreground service type `health` trên Android 14+, của việc bỏ tối ưu pin?
  - Rủi ro: ghi prefs bằng `apply()` từ cả Kotlin lẫn Dart (race), `catch` rỗng trong `updateAllWidgets`, widget hard-code chuỗi.
- Chứng cứ trên thiết bị:
  ```bash
  adb shell dumpsys activity services com.nhh031.fitness_tracker   # service đang chạy
  adb shell dumpsys appwidget | findstr fitness                    # widget đã đăng ký
  adb logcat -s flutter                                            # log phía Dart
  adb shell dumpsys deviceidle whitelist | findstr fitness         # trạng thái bỏ tối ưu pin
  adb shell cmd appops get com.nhh031.fitness_tracker              # quyền & appops
  ```
- *Mục báo cáo*: Thành phần Android (Activity, Service, BroadcastReceiver, AppWidget), quyền, cảm biến, thông báo, chạy nền.

### Chặng 3 — Cầu nối Flutter ↔ Android (≈2 giờ)
- Đọc: `services/background_service.dart`, `widget_sync_service.dart`, `widgets/step_counter_widget.dart` (phần `_initStepCounter`), `screens/profile/profile_battery_card.dart`, `services/notification_service.dart`, `services/health_sync_service.dart`, `services/biometric_service.dart`, `widgets/biometric_gate.dart`.
- Hỏi: Hai phía thống nhất tên kênh/method ra sao? Dữ liệu nào đi bằng channel, dữ liệu nào đi bằng prefs? Quyền runtime được xin lúc nào, bị từ chối thì sao? Plugin nào bọc API Android nào (xem bảng mục 1)?
- Chứng cứ: bảng đối chiếu `invokeMethod("x")` ↔ `case "x"` trong `MainActivity.kt`; sơ đồ kiến trúc Platform Channel.
- *Mục báo cáo*: Giao tiếp Flutter–Native, sử dụng plugin hệ thống.

### Chặng 4 — Dữ liệu & kiến trúc ứng dụng (≈3 giờ)
- Đọc: `main.dart`, `widgets/auth_gate.dart`, `screens/main_screen.dart`, `database/app_database.dart`, `repositories/step_repository.dart` + `water_repository.dart` (mẫu), `services/storage_service.dart` (chỉ đầu file: notifier, cache, rồi dò theo nhóm hàm), `services/firestore_service.dart`, `services/auth_service.dart`.
- Hỏi: Thứ tự khởi tạo trong `main()` và vì sao? Schema SQLite gồm những bảng nào (`workout_logs`, `food_entries`, `daily_water_history`, `chat_messages`, + bảng V2), index nào? Chiến lược local-first, cache in-memory, migrate SharedPreferences → SQLite? `ValueNotifier` thay cho state management ra sao? Sync Firestore xảy ra khi nào?
- Chứng cứ: ERD các bảng SQLite (có thể xem bằng Android Studio *App Inspection*), sơ đồ lớp UI → StorageService → Repository → DB/Cloud.
- Điểm phê bình: `StorageService` ~2.270 dòng đóng vai "God facade" và trùng logic với `StepRepository`.
- *Mục báo cáo*: Kiến trúc, lưu trữ dữ liệu, xác thực & đồng bộ.

### Chặng 5 — Nghiệp vụ & AI (≈2 giờ)
- Đọc: `services/gemini_service.dart` (prompt, parse JSON, fallback model, streaming), `open_food_facts_service.dart`, `user_metrics_service.dart` (BMR/TDEE, quãng đường/calo từ bước), `achievement_service.dart`, `speech_service.dart`, `report_export_service.dart`, `widgets/barcode_scanner_sheet.dart`, `widgets/ai_food_logging_widget.dart`.
- Hỏi: Công thức tính toán nào được dùng, có trích nguồn không? Xử lý lỗi/mạng/API key thế nào? Dữ liệu nào rời khỏi máy (Gemini, Open Food Facts, Firestore) — liên quan quyền riêng tư.
- *Mục báo cáo*: Chức năng chính theo module, tích hợp dịch vụ ngoài.

### Chặng 6 — Giao diện (≈2–3 giờ)
- Đọc: `theme.dart`, `widgets/app_ui_components.dart`, `screens/dashboard_screen.dart`, `workout_screen.dart` → `active_workout_screen.dart`, `food_screen.dart`, `profile_screen.dart` (+ `screens/profile/*`), một chart mẫu (`weekly_calorie_bar_chart.dart`), `hydration_wave_widget.dart`.
- Nâng cao (chỉ lướt cấu trúc): `anatomy_kinematic_painter.dart` (`AnatomyKinematicJoints`, `AnatomyKinematicPainter`), `exercise_pose_widget.dart` (`ExercisePoseAnimator`), `muscle_anatomy_map_widget.dart`.
- Hỏi: Điều hướng 4 tab và `AuthGate`/`BiometricGate` bọc nhau thế nào? Vòng đời widget (`initState/dispose`, huỷ subscription), `WidgetsBindingObserver`? Hiệu năng: `CustomPainter`, `shouldRepaint`, `KeyedSubtree` khi đổi phiên?
- *Mục báo cáo*: Thiết kế giao diện & trải nghiệm, đa ngôn ngữ (`locale_service.dart`, `assets/i18n`).

### Chặng 7 — Chất lượng, bảo mật, hạn chế (≈1,5 giờ)
- Đọc: `test/storage_service_test.dart` (mẫu chuẩn), `test/activity_features_test.dart`, `test/anatomy_kinematic_painter_test.dart`, `.github/workflows/flutter_ci.yml`, `.gitignore`.
- Chạy: `flutter analyze`, `flutter test --coverage` (lấy số liệu cho báo cáo).
- Tổng hợp rủi ro/hạn chế (đã phát hiện, nên kiểm chứng lại khi viết):
  1. Logic đếm bước lặp ở 3 nơi, có thể race trên prefs; Kotlin thiếu anti-jitter.
  2. `google-services.json` được commit; `serverClientId` hard-code.
  3. Release ký bằng debug key; `applicationId` khác `namespace`.
  4. `main()` nuốt lỗi khởi tạo DB/Health; `catch` rỗng trong vài chỗ native.
  5. Không có test cho code Kotlin; widget Android hard-code chuỗi/mục tiêu.
  6. Tên model Gemini viết cứng trong `GeminiService` (hiện `gemini-3.8-flash`, dự phòng `gemini-3.7-flash`). Trước đây là `gemini-2.0-flash` + `gemini-1.5-flash` — cả hai đã bị Google tắt nên mọi lời gọi AI đều lỗi; cần nêu trong báo cáo như một rủi ro phụ thuộc dịch vụ ngoài.
  7. Thư viện `lottie` khai báo nhưng không dùng.
- *Mục báo cáo*: Kiểm thử, bảo mật & quyền riêng tư, hạn chế & hướng phát triển.

## 3. Dàn ý báo cáo gợi ý

1. Giới thiệu đề tài, mục tiêu, phạm vi, môi trường (Chặng 0)
2. Công nghệ & thư viện sử dụng (Chặng 1)
3. Kiến trúc tổng thể + sơ đồ thư mục (Chặng 1, 4)
4. **Các thành phần Android sử dụng** — Service, Receiver, App Widget, Notification, Sensor, quyền (Chặng 2)
5. Giao tiếp Flutter ↔ Native (Platform Channel, SharedPreferences) (Chặng 3)
6. Lưu trữ dữ liệu & đồng bộ (SQLite, Firestore, Auth) (Chặng 4)
7. Chức năng chi tiết theo module: Dashboard, Workout, Food/AI, Profile/Health (Chặng 5, 6)
8. Giao diện & đa ngôn ngữ (Chặng 6)
9. Kiểm thử, CI/CD (Chặng 7)
10. Đánh giá: ưu điểm, hạn chế, hướng phát triển (Chặng 7)
11. Phụ lục: bảng quyền, bảng channel, schema DB, danh sách file

## 4. Sơ đồ nên vẽ (mỗi sơ đồ ứng với một chặng)

- Cây thư mục rút gọn (Chặng 1)
- Component diagram: Flutter UI ↔ Platform Channel ↔ Service/Receiver/Widget ↔ SharedPreferences (Chặng 2–3)
- Sequence diagram "một bước chân": Sensor → `StepCounterService` → prefs/notification/broadcast → `MainActivity` → `EventChannel` → `StepCounterWidget` → `WidgetSyncService` → `FitnessAppWidgetProvider` (Chặng 2–3)
- Luồng khởi động & cổng truy cập: `main` → `AuthGate` → Onboarding → `BiometricGate` → `MainScreen` (Chặng 4)
- ERD SQLite (Chặng 4)
- Luồng Gemini: input (text/ảnh/giọng nói/barcode) → service → parse → lưu `food_entries` (Chặng 5)

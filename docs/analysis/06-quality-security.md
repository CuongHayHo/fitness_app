# Phân tích Kiểm thử, CI & Bảo mật (W6)

## 1. Tóm tắt
Dự án Fitness Tracker thiết lập hệ thống đảm bảo chất lượng phần mềm (QA) và bảo mật đa tầng với bộ kiểm thử tự động gồm 17 file (123 tests) đạt độ phủ toàn diện từ giải thuật sinh trắc, giao diện động học CustomPainter đến tầng Repository. Chiến lược SQLite FFI in-memory cách ly hoàn toàn môi trường test, giải phóng ứng dụng khỏi sự phụ thuộc vào thiết bị thật. Pipeline CI/CD trên GitHub Actions tự động hóa quy trình kiểm tra mã nguồn (chính sách 0 lint issue), chạy toàn bộ test suite và build APK xác minh. Về bảo mật, dự án tách biệt secret qua compile-time define, ẩn cấu hình nhạy cảm qua `.gitignore`, dù vẫn còn một số rủi ro như dùng debug keystore cho release và lưu API key người dùng dưới dạng văn bản thuần.

## 2. Chức năng

| Chức năng | Mô tả ngắn | file:line |
|---|---|---|
| **CI/CD Pipeline Tự động hóa** | Workflow GitHub Actions kích hoạt khi push/PR vào nhánh `main`/`master`, tự động cài đặt Zulu Java 17, Flutter stable, chạy phân tích tĩnh, chạy bộ test và biên dịch kiểm tra APK debug. | `.github/workflows/flutter_ci.yml:3-44` |
| **Quy chuẩn Static Analysis (Lint)** | Cấu hình bộ phân tích tĩnh tuân thủ chuẩn `flutter_lints`, áp dụng chính sách 0 lỗi/cảnh báo (Zero-issue policy) làm chốt chặn chất lượng trước khi hợp nhất mã nguồn. | `analysis_options.yaml:10-26`, `pubspec.yaml:75` |
| **Quản lý Bí mật & Khóa API Đa tầng** | Cơ chế nạp Gemini API Key với thứ tự ưu tiên: Compile-time define (`--dart-define`) -> Runtime SharedPreferences -> Fallback ngoại tuyến, không hardcode khóa trong mã nguồn. | `lib/services/gemini_service.dart:48-61`, `.env.example:1-7` |
| **Kiểm soát Tệp tin Nhạy cảm (VCS Exclusion)** | Cấu hình `.gitignore` loại trừ các tệp chứa thông tin nhạy cảm như biến môi trường (`.env*`), tệp thuộc tính cục bộ (`local.properties`, `key.properties`), và chứng chỉ ký số (`*.keystore`, `*.jks`). | `.gitignore:18-20,38-42` |
| **Kiểm thử SQLite In-Memory Tốc độ cao** | Khởi tạo SQLite độc lập qua `sqflite_common_ffi` và `inMemoryDatabasePath` khi phát hiện cờ môi trường `FLUTTER_TEST`, đảm bảo test chạy tức thì, không ghi đĩa và cô lập hoàn toàn giữa các ca kiểm thử. | `lib/database/app_database.dart:20-28,46-55`, `pubspec.yaml:58` |
| **Kiểm thử Giả lập SharedPreferences** | Thiết lập trạng thái ban đầu của kho lưu trữ Key-Value thông qua `SharedPreferences.setMockInitialValues({})` trước mỗi ca kiểm thử, cho phép kiểm tra logic lưu trữ mà không cần engine nền tảng. | `test/storage_service_test.dart:11`, `test/activity_features_test.dart:15` |
| **Kiểm thử Logic Chuỗi Ngày (Streak) & Reboot** | Kiểm tra thuật toán duy trì streak đăng nhập, xử lý ngắt quãng >1 ngày, giới hạn streak người dùng mới, và thuật toán bảo toàn số bước phần cứng khi thiết bị khởi động lại. | `test/storage_service_test.dart:16-125` |
| **Kiểm thử Lượng nước & Cấu hình Nhắc nhở** | Kiểm thử tăng giảm ly nước hôm nay, cơ chế tự động chuyển dữ liệu cũ vào nhật ký lịch sử khi sang ngày mới, và lưu trữ chu kỳ hẹn giờ uống nước. | `test/storage_service_test.dart:133-204`, `test/widget_test.dart:8-41` |
| **Kiểm thử Tuần tự hóa Tóm tắt Ngày** | Kiểm tra tính toàn vẹn của mô hình `DailyActivitySummary` khi chuyển đổi sang/từ JSON, xác thực truy vấn dữ liệu hoạt động theo ngày cụ thể và lọc theo ngày tham gia. | `test/storage_service_test.dart:212-306` |
| **Kiểm thử Ghi nhận Tập luyện & Mở khóa Huy hiệu** | Kiểm tra tích lũy thời lượng tập tuần, nhận diện bài tập rạng sáng (< 7:00 AM), và điều kiện mở khóa các huy hiệu thành tích (10k Steps, Eternal Flame, Cardio Master, Dawn Warrior). | `test/activity_features_test.dart:19-132` |
| **Kiểm thử Xử lý Phản hồi AI & Fallback Ngoại tuyến** | Kiểm định parser bóc tách JSON món ăn/bài tập từ Gemini (kể cả khi bị bọc trong Markdown block hoặc văn bản đối thoại), và cơ chế tự sinh bài tập cục bộ khi mất kết nối mạng. | `test/activity_features_test.dart:136-168,360-383`, `test/gemini_service_test.dart:8-90` |
| **Kiểm thử Tính Calo & Macro Dinh dưỡng** | Kiểm định ghi nhận nhật ký dinh dưỡng theo ngày, tính tổng macro (protein/carbs/fat), và công thức tính calo tiêu thụ thời gian thực kết hợp BMR theo thời gian trong ngày. | `test/activity_features_test.dart:176-255` |
| **Kiểm thử Phân loại Thiết bị & Tăng tải Tạ** | Kiểm tra phân loại bài tập tay không (bodyweight) vs tạ đơn (dumbbell), và công thức điều chỉnh calo theo khối lượng tạ (`WorkoutCalorieHelper`). | `test/activity_features_test.dart:259-358` |
| **Kiểm thử Vẽ Động học Giải phẫu (Kinematic Painter)** | Kiểm tra thuật toán phân loại bài tập đa ngôn ngữ (Việt - Anh), chọn góc nhìn (front/side), tính hệ số kích hoạt cơ động, nhịp động học 5 pha rep tempo, và render Widget CustomPaint không phát sinh ngoại lệ. | `test/anatomy_kinematic_painter_test.dart:7-276` |
| **Kiểm thử Kiến trúc Repository & Quản lý Cache** | Kiểm tra khởi tạo bảng SQLite, xóa trắng dữ liệu (`clearAllUserData`), và tính nhất quán của cơ chế xóa cache bộ nhớ (`invalidateCache`) trên các Repository. | `test/phase_3_architecture_test.dart:20-35`, `test/evolution_plan_v2_test.dart:14-24` |
| **Kiểm thử Công thức Sinh trắc & Điểm Sức khỏe** | Kiểm tra thuật toán tính % mỡ cơ thể theo chuẩn US Navy, chỉ số BMI, BMR theo phương trình Mifflin-St Jeor, và thuật toán tính Health Score dựa trên 4 trụ cột (Vận động, Dinh dưỡng, Giấc ngủ, Thói quen). | `test/profile_features_test.dart:10-60`, `test/health_score_test.dart:15-40`, `test/evolution_plan_v2_test.dart:126-150` |
| **Kiểm thử Quét Mã Vạch & Đồng bộ Thiết bị Đeo** | Kiểm tra mô hình sản phẩm quét mã vạch `ScannedFoodProduct` (tỷ lệ khẩu phần), xử lý mã vạch rỗng, và vòng đời kết nối dữ liệu sức khỏe `HealthSnapshot`. | `test/phase_4_features_test.dart:18-111` |
| **Cấu hình Xây dựng Nền tảng Android** | Thiết lập thông số ứng dụng Android: `namespace`, `applicationId`, `minSdk = 26`, biên dịch Java 17, desugaring thư viện cốt lõi, và cấu hình ký số ứng dụng. | `android/app/build.gradle.kts:10,14-39,44` |
| **Tích hợp Cấu hình Dịch vụ Firebase Client** | Tệp cấu hình client `google-services.json` định nghĩa tham số kết nối cho cả 2 định danh gói (`com.example.fitness_tracker` và `com.nhh031.fitness_tracker`). | `android/app/google-services.json:1-84`, `android/app/build.gradle.kts:6` |

## 3. Kỹ thuật Android/Flutter

| Kỹ thuật / API | Cách dùng trong dự án | file:line | API level / Quyền liên quan |
|---|---|---|---|
| **SQLite FFI (`sqflite_common_ffi`)** | Cấu hình `databaseFactory = databaseFactoryFfi` và nạp database ảo `inMemoryDatabasePath` khi chạy trong môi trường `FLUTTER_TEST`, cho phép chạy test SQLite native trên CPU host mà không cần Android Emulator. | `lib/database/app_database.dart:20-28,46-55`, `pubspec.yaml:58` | Độc lập nền tảng, không cần quyền hệ thống |
| **Mocking SharedPreferences** | Gọi `SharedPreferences.setMockInitialValues({...})` trong khối `setUp()` để cô lập hoàn toàn trạng thái giữa các test, giả lập bộ nhớ KV của Android. | `test/storage_service_test.dart:11`, `test/activity_features_test.dart:15` | Android SharedPreferences API |
| **Widget Testing (`WidgetTester`)** | Sử dụng `testWidgets`, `tester.pumpWidget()`, `tester.pumpAndSettle()`, và `tester.takeException()` để kiểm định kết xuất widget CustomPaint, kiểm tra lỗi giao diện và chuyển đổi giới tính mô hình giải phẫu. | `test/anatomy_kinematic_painter_test.dart:195-276`, `test/phase_4_features_test.dart:113-131`, `test/muscle_anatomy_map_test.dart:6-40` | Flutter Test Framework |
| **GitHub Actions Pipeline** | Tự động hóa CI/CD với 3 chốt chặn: Kiểm tra tĩnh (`flutter analyze`), kiểm tra hồi quy (`flutter test`), và kiểm tra đóng gói (`flutter build apk --debug`) trên runner `ubuntu-latest`. | `.github/workflows/flutter_ci.yml:10-44` | Môi trường CI Linux, Docker/Runner |
| **Flutter Lints Static Analyzer** | Kích hoạt bộ quy tắc phân tích mã nguồn chuẩn `package:flutter_lints/flutter.yaml` trong `analysis_options.yaml`, phát hiện sớm lỗi cú pháp, rò rỉ bộ nhớ và vi phạm quy chuẩn Flutter. | `analysis_options.yaml:10`, `pubspec.yaml:75` | Dart Analyzer Engine |
| **Compile-time Define (`String.fromEnvironment`)** | Đọc biến môi trường lúc biên dịch `const envKey = String.fromEnvironment('GEMINI_API_KEY')` để nạp khóa bảo mật từ cờ build hoặc tệp `.env`, ngăn ngừa việc nhúng cứng khóa vào mã nguồn. | `lib/services/gemini_service.dart:48-52` | Dart Runtime / Build flags |
| **Kiểm soát Tệp Bảo mật (.gitignore)** | Khai báo loại trừ các định dạng khóa Android Keystore (`*.jks`, `*.keystore`), cấu hình riêng máy dev (`local.properties`, `key.properties`), và tệp môi trường thực (`.env*`). | `.gitignore:18-20,38-42` | Git Version Control |
| **Signing Configs trong Gradle** | Cấu hình khối `signingConfigs` và gán chữ ký số trong `buildTypes.release` cho ứng dụng Android. | `android/app/build.gradle.kts:35-39` | Android Gradle Plugin (AGP) |
| **Java Core Library Desugaring** | Bật `isCoreLibraryDesugaringEnabled = true` đi kèm phụ thuộc `desugar_jdk_libs:2.1.4` để hỗ trợ các API Java 8+ (như java.time) trên các thiết bị Android chạy `minSdk 26`. | `android/app/build.gradle.kts:15,44` | Android API 26+ |
| **Google Services Gradle Plugin** | Áp dụng plugin `com.google.gms.google-services` để đọc tệp `google-services.json` và tự động sinh tài nguyên XML cho Firebase Core / Auth / Firestore. | `android/app/build.gradle.kts:6`, `android/app/google-services.json:1-84` | Google Play Services |

## 4. Luồng xử lý chính

Sơ đồ khối sau đây mô tả toàn bộ quy trình Đảm bảo Chất lượng Phần mềm (QA), Cơ chế Cách ly Kiểm thử (Test Isolation) và Pipeline CI/CD tự động của dự án:

```mermaid
flowchart TD
    subgraph DevEnvironment["1. Môi trường Phát triển (Developer Workstation)"]
        A[Lập trình viên sửa mã nguồn] --> B[Chạy Kiểm tra Phân tích Tĩnh: flutter analyze]
        B --> C[Chạy Kiểm thử Tự động Cục bộ: flutter test]
    end

    subgraph TestIsolation["2. Cơ chế Cách ly Kiểm thử (Test Isolation Strategy)"]
        C --> D{Môi trường phát hiện cờ FLUTTER_TEST?}
        D -- Đúng --> E[AppDatabase.ensureFfiInitialized]
        E --> F[sqfliteFfiInit + databaseFactory = databaseFactoryFfi]
        F --> G[Mở Database inMemoryDatabasePath: Không ghi đĩa, chạy trên RAM]
        D -- Đúng --> H[SharedPreferences.setMockInitialValues: Giả lập sạch Key-Value]
        G & H --> I[Thực thi 123 tests: Unit, Widget, Anatomy Painter, Biometrics]
    end

    subgraph SecretMgmt["3. Quản lý Secret & Cấu hình"]
        K[.env thực tế / Biến môi trường] -. Bị chặn bởi .gitignore .-> L[Không commit lên Git]
        M[.env.example] -- Cung cấp template mẫu --> N[Repository Git]
        O[Khóa Gemini: String.fromEnvironment] -- Ưu tiên 1: Compile-time define --> P[GeminiService.apiKey]
    end

    subgraph CICDPipeline["4. GitHub Actions CI/CD Pipeline (Ubuntu Runner)"]
        N --> Q[Sự kiện Push / Pull Request vào main, master]
        Q --> R[actions/checkout@v4]
        R --> S[actions/setup-java@v4: Zulu JDK 17]
        S --> T[subosito/flutter-action@v2: Channel Stable, Cache enabled]
        T --> U[flutter pub get]
        U --> V[flutter analyze: Chặn build nếu có bất kỳ lỗi/cảnh báo nào]
        V --> W[flutter test: 123/123 tests bắt buộc PASS]
        W --> X[flutter build apk --debug: Xác minh biên dịch Android APK thành công]
    end

    I -->|Tất cả test PASS & 0 Lint issue| N
    X --> Y[Hoàn tất Xác thực CI - Mã nguồn Sẵn sàng Triển khai]
```

## 5. Hạn chế & rủi ro

- **Bản phát hành Release ký bằng Debug Keystore (`android/app/build.gradle.kts:35-39`):** Trong khối `buildTypes.release`, cấu hình hiện tại đang trỏ `signingConfig = signingConfigs.getByName("debug")` đi kèm ghi chú TODO. Nếu build APK/AAB release để phát hành thực tế, ứng dụng sẽ mang chữ ký debug mặc định, dẫn đến nguy cơ bị giả mạo ứng dụng và vi phạm chính sách bảo mật của Google Play Store.
- **Tệp `google-services.json` được commit trực tiếp vào mã nguồn (`android/app/google-services.json:1-84`, `.gitignore:1-56`):** Tệp cấu hình Firebase chứa `project_id`, `mobilesdk_app_id`, client id và api key đang nằm trong chỉ mục của Git và không được loại trừ trong `.gitignore`. Mặc dù Firebase API keys là public identifiers theo thiết kế của Google, việc công khai file này đòi hỏi toàn bộ Cloud Firestore và Firebase Storage phải được bảo vệ nghiêm ngặt bằng Security Rules và API restriction trên Google Cloud Console để tránh bị lạm dụng quota hoặc truy cập dữ liệu trái phép.
- **Không đồng nhất Package Name giữa Gradle và cấu hình dịch vụ (`android/app/build.gradle.kts:10,25`, `android/app/google-services.json:12,49`):** Trong Gradle, `namespace` được đặt là `com.example.fitness_tracker` trong khi `applicationId` là `com.nhh031.fitness_tracker`. Mặc dù `google-services.json` đã khai báo client thứ 2 cho `com.nhh031.fitness_tracker`, sự phân mảnh này dễ gây lỗi cấu hình sai package khi tích hợp thêm các dịch vụ của bên thứ ba (như OAuth 2.0, Health Connect API, hoặc Push Notification).
- **Quy tắc Phân tích Tĩnh (Linter) ở mức tối thiểu (`analysis_options.yaml:23-26`):** Dự án chỉ kế thừa bộ luật cơ bản từ `flutter_lints`, các luật nghiêm ngặt nhằm nâng cao chất lượng code như `avoid_print`, `unawaited_futures`, `always_declare_return_types`, `prefer_final_locals` đều chưa được bật hoặc đang bị chú thích (commented out).
- **Lưu trữ Gemini API Key người dùng dưới dạng văn bản thuần (`lib/services/gemini_service.dart:55-57`, `lib/services/storage_service.dart:138`):** Khi người dùng nhập API key tùy chỉnh trong ứng dụng, giá trị này được lưu trực tiếp vào `SharedPreferences` thông thường mà không sử dụng cơ chế mã hóa cấp hệ điều hành (như `flutter_secure_storage` kết hợp Android Keystore / EncryptedSharedPreferences), dẫn đến nguy cơ rò rỉ khóa nếu thiết bị bị root hoặc bị sao lưu dữ liệu (`adb backup`).
- **Thiếu kiểm thử tích hợp (Integration Test) trên thiết bị thật (`test/*.dart`):** Toàn bộ 123 ca kiểm thử hiện tại là Unit Test và Widget Test chạy trên môi trường giả lập (host CPU + FFI SQLite + Mock SharedPreferences). Dự án hoàn toàn chưa có bộ `integration_test` để xác thực hành vi phần cứng thực tế trên Android như: cảm biến đếm bước chạy nền khi tắt màn hình, quyền runtime của Android 13/14, hoặc giao tiếp camera quét mã vạch qua `mobile_scanner`.
- **Quy trình CI chưa có bước phân tích bảo mật tĩnh và kiểm tra độ phủ mã (Code Coverage) (`.github/workflows/flutter_ci.yml:37-44`):** Pipeline CI mới chỉ dừng lại ở `flutter analyze`, `flutter test` và `flutter build apk --debug`. Chưa tích hợp công cụ quét lỗ hổng phụ thuộc (Dependency Vulnerability Scanner như Trivy hoặc Snyk), chưa đo lường tỷ lệ bao phủ mã nguồn (`--coverage`) và chưa có bước kiểm thử build release (`flutter build appbundle`).

## 6. Gợi ý cho báo cáo

### Các mục báo cáo đề xuất đưa vào Đồ án
1. **Chương "Kiểm thử & Đảm bảo Chất lượng Phần mềm (Software Quality Assurance & Testing Strategy)":**
   - Phân tích chiến lược kiểm thử đa tầng: Kiểm thử đơn vị (Unit Test) cho các thuật toán lõi (Mifflin-St Jeor, US Navy Body Fat, 4-Pillar Health Score, Kinematic Rep Tempo); Kiểm thử giao diện (Widget Test) cho đồ họa `CustomPainter` và tương tác người dùng.
   - Kiến trúc kiểm thử SQLite không phụ thuộc thiết bị: Trình bày cơ chế kích hoạt `sqflite_common_ffi` và `inMemoryDatabasePath` khi phát hiện biến môi trường kiểm thử, cho phép chạy 123 tests tự động trong vài giây mà không cần khởi động máy ảo Android nặng nề.
   - Tự động hóa kiểm soát hồi quy với CI/CD Pipeline (GitHub Actions): Quy trình kiểm duyệt tự động từ phân tích tĩnh (0 lint issue) đến xác minh build APK.
2. **Chương "An toàn Thông tin & Cấu hình Ứng dụng Android (Application Security & DevOps)":**
   - Quản lý khóa API và cấu hình nhạy cảm: Trình bày mô hình 3 cấp (Compile-time define qua `--dart-define`, Runtime SharedPreferences, và Fallback offline), quy tắc kiểm soát tệp nhạy cảm với `.gitignore`.
   - Phân tích rủi ro an toàn trên nền tảng Android: Thực trạng chữ ký số Keystore cho môi trường phát triển vs môi trường thương mại; Khuyến nghị mã hóa dữ liệu cục bộ bằng Android Keystore.

### Lệnh adb và công cụ kiểm thử đề xuất thực hiện để lấy minh chứng
- **Chạy phân tích tĩnh mã nguồn cục bộ:**
  ```bash
  flutter analyze
  ```
- **Chạy toàn bộ 123 bài kiểm thử với định dạng chi tiết:**
  ```bash
  flutter test --reporter expanded
  ```
- **Xác thực chữ ký số của gói cài đặt APK:**
  ```bash
  apksigner verify --verbose --print-certs build/app/outputs/flutter-apk/app-debug.apk
  ```
- **Kiểm tra danh sách quyền hệ thống thực tế được cấp cho ứng dụng qua adb:**
  ```bash
  adb shell dumpsys package com.nhh031.fitness_tracker | findstr /i "permission"
  ```
- **Kiểm tra dữ liệu SharedPreferences trong bộ nhớ cục bộ để đánh giá an toàn dữ liệu:**
  ```bash
  adb shell run-as com.nhh031.fitness_tracker cat shared_prefs/FlutterSharedPreferences.xml
  ```

### Ảnh chụp màn hình cần thu thập minh chứng
1. Ảnh chụp terminal thực thi lệnh `flutter analyze` hiển thị thông báo thành công tuyệt đối: `"No issues found!"`.
2. Ảnh chụp terminal thực thi lệnh `flutter test` hiển thị kết quả toàn bộ 123 ca kiểm thử vượt qua thành công: `"All tests passed!"`.
3. Ảnh chụp giao diện GitHub Actions hiển thị luồng chạy hoàn tất (tất cả các bước đều tick xanh: Checkout, Setup Java 17, Setup Flutter, Code Quality Analysis, Execute Test Suite, Build Android APK).
4. Ảnh chụp cấu trúc in-memory database configuration trong mã nguồn minh họa sự tách biệt giữa môi trường kiểm thử và môi trường chạy thực tế.

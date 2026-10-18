# CHƯƠNG 5. KIỂM THỬ, ĐÁNH GIÁ VÀ KẾT LUẬN

## 5.1. Kiểm thử phần mềm tự động

Nhằm đảm bảo tính ổn định và hạn chế lỗi hồi quy trong quá trình phát triển, nhóm đã xây dựng chiến lược kiểm thử đa tầng gồm phân tích mã nguồn tĩnh, kiểm thử đơn vị (*Unit Test*), kiểm thử giao diện (*Widget Test*) và cô lập dữ liệu.

### 5.1.1. Kiểm thử tĩnh và chuẩn hóa mã nguồn

Kiểm thử tĩnh được thực hiện qua bộ công cụ `flutter analyze` kết hợp quy chuẩn `package:flutter_lints/flutter.yaml`. 

```yaml
include: package:flutter_lints/flutter.yaml

linter:
  rules:
    prefer_const_constructors: true
    prefer_const_declarations: true
    avoid_empty_else: true
    unnecessary_null_aware_assignments: true
```
(Nguồn: analysis_options.yaml:10-18)

Quy chuẩn này quét cây cú pháp Dart nhằm phát hiện biến không sử dụng, rủi ro bất đồng bộ và khởi tạo đối tượng dư thừa. Kết quả phân tích đạt 0 lỗi và 0 cảnh báo:

```text
Analyzing fitness_app...
No issues found! (ran in 4.2s)
```

Chính sách không chấp nhận lỗi tĩnh giúp mã nguồn duy trì tính đồng nhất và giảm thiểu rủi ro ngoại lệ trong quá trình chạy.

### 5.1.2. Chiến lược cô lập kiểm thử tầng dữ liệu với SQLite FFI

Cơ sở dữ liệu SQLite trong Flutter phụ thuộc thư viện native của Android. Để kiểm thử trên máy trạm hoặc máy chủ CI mà không cần mở máy ảo Android, nhóm sử dụng thư viện `sqflite_common_ffi`. Khi phát hiện cờ môi trường `FLUTTER_TEST`, ứng dụng khởi tạo cơ sở dữ liệu trên bộ nhớ RAM qua hằng số `inMemoryDatabasePath`:

```dart
static void ensureFfiInitialized() {
  if (_ffiInitialized) return;
  if (!kIsWeb &&
      (Platform.isWindows ||
          Platform.isMacOS ||
          Platform.environment.containsKey('FLUTTER_TEST'))) {
    sqfliteFfiInit();
    databaseFactory = databaseFactoryFfi;
    _ffiInitialized = true;
  }
}
```
(Nguồn: lib/database/app_database.dart:18-29)

Giải pháp này mang lại ba ưu điểm kỹ thuật:
1. **Tính độc lập:** Mỗi ca kiểm thử chạy trên một cơ sở dữ liệu RAM riêng biệt, tự hủy sau khi bài kiểm thử kết thúc.
2. **Tốc độ thực thi:** Thao tác đọc ghi trên bộ nhớ RAM diễn ra nhanh, không phát sinh độ trễ I/O đĩa vật lý.
3. **Độc lập nền tảng:** Bộ kiểm thử chạy được trên máy trạm và máy chủ CI tự động mà không cần thiết bị Android vật lý.

Song song đó, nhóm gọi `SharedPreferences.setMockInitialValues({})` trước mỗi bài test để giả lập kho lưu trữ khóa - giá trị rỗng, phục vụ kiểm thử chuỗi ngày đăng nhập (*streak*) và lượng nước uống.

### 5.1.3. Kết quả thực thi bộ kiểm thử tự động đa tầng

Hệ thống kiểm thử gồm 17 tệp trong thư mục `test/` với 123 bài kiểm thử unit test và widget test. Toàn bộ 123 bài kiểm thử đều vượt qua thành công, đạt tỷ lệ 100% (123/123 tests passed).

Bảng 5.1: Bảng tổng hợp kết quả kiểm thử phần mềm theo module chức năng

| Phân hệ chức năng | Tệp kiểm thử cụ thể | Số bài test | Trạng thái | Nội dung kiểm thử trọng tâm |
|---|---|:---:|:---:|---|
| **Xác thực & Thể trạng** | `profile_features_test.dart`, `health_score_test.dart` | 15 | 15/15 Pass | Công thức US Navy tính tỷ lệ mỡ; BMR Mifflin-St Jeor; BMI; Điểm Sức khỏe 4 trụ cột. |
| **Cơ sở dữ liệu & Storage** | `storage_service_test.dart`, `phase_3_architecture_test.dart`, `evolution_plan_v2_test.dart` | 35 | 35/35 Pass | Duy trì streak; nhật ký nước; khởi tạo 7 bảng SQLite; xóa dữ liệu và bộ đệm bộ nhớ. |
| **Cảm biến & Dịch vụ nền** | `activity_features_test.dart`, `phase_4_features_test.dart` | 18 | 18/18 Pass | Xử lý bù số bước khi máy khởi động lại; nhận diện bài tập rạng sáng; mở khóa huy hiệu. |
| **Dinh dưỡng & Xử lý AI** | `food_tab_features_test.dart`, `gemini_service_test.dart`, `daily_ai_briefing_test.dart`, `ai_chat_history_test.dart` | 27 | 27/27 Pass | Bóc tách JSON từ Gemini; chuyển đổi model dự phòng; bộ đệm 23 món ăn định sẵn; tính macro. |
| **Luyện tập & Động học** | `anatomy_kinematic_painter_test.dart`, `exercise_pose_widget_test.dart`, `muscle_anatomy_map_test.dart`, `achievements_and_analytics_test.dart` | 17 | 17/17 Pass | Lượng giác 18 khớp xương; nhịp động học 5 pha rep tempo; góc nhìn trước/cạnh; bản đồ cơ bắp. |
| **Giao diện & Đa ngôn ngữ** | `locale_service_test.dart`, `widget_test.dart` | 11 | 11/11 Pass | Nạp gói ngôn ngữ tiếng Việt/tiếng Anh; làm mới màn hình khi đổi ngôn ngữ; widget nước. |
| **Tổng cộng** | **17 tệp kiểm thử** | **123** | **123/123** | **Tỷ lệ vượt qua đạt 100%** |

![Hình 5.1: Minh chứng kết quả phân tích tĩnh và kiểm thử tự động](img/chup-test-analyze.png)
> CHỤP: Cửa sổ dòng lệnh Terminal máy tính / thấy thông báo "No issues found!" và kết quả "All 123 tests passed!" / chạy lần lượt lệnh flutter analyze và flutter test tại thư mục gốc dự án.

---

## 5.2. Quy trình tích hợp liên tục (CI/CD)

Nhóm thiết lập quy trình tích hợp liên tục (*CI*) trên GitHub Actions để tự động hóa khâu kiểm tra chất lượng mỗi khi có thay đổi mã nguồn.

### 5.2.1. Cấu hình quy trình tự động trên GitHub Actions

Workflow được định nghĩa trong `.github/workflows/flutter_ci.yml`, tự động kích hoạt khi có sự kiện đẩy mã (*push*) hoặc tạo yêu cầu hợp nhất (*pull request*) vào nhánh `main` và `master`.

```yaml
name: Flutter CI/CD Pipeline
on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  analyze_and_test:
    name: Analyze, Test & Build Verification
    runs-on: ubuntu-latest
    timeout-minutes: 25
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { distribution: 'zulu', java-version: '17' }
      - uses: subosito/flutter-action@v2
        with: { channel: 'stable', cache: true }
      - run: flutter pub get
```
(Nguồn: .github/workflows/flutter_ci.yml:1-35)

Pipeline chạy trên máy ảo `ubuntu-latest`, cài đặt Java 17 (Zulu JDK) tương thích với Android Gradle Plugin 8.11.1 và Flutter SDK kênh `stable` có lưu bộ nhớ đệm phụ thuộc.

### 5.2.2. Ba chốt chặn đảm bảo chất lượng phần mềm

Quy trình CI gồm 3 chốt chặn kiểm duyệt liên tiếp:
1. **Chốt chặn 1 - Phân tích tĩnh (`flutter analyze`):** Quét toàn bộ mã nguồn theo bộ luật linter. Nếu có cảnh báo hoặc lỗi cú pháp, pipeline dừng lại ngay lập tức.
2. **Chốt chặn 2 - Kiểm thử tự động (`flutter test`):** Thực thi 123 bài kiểm thử unit và widget test trên môi trường máy ảo runner headless nhờ cơ chế SQLite FFI in-memory.
3. **Chốt chặn 3 - Xác minh biên dịch gói cài đặt (`flutter build apk --debug`):** Biên dịch tệp APK debug để xác nhận tính tương thích của cấu hình Gradle, tệp `AndroidManifest.xml` và các plugin native.

![Hình 5.2: Quy trình kiểm thử và CI/CD tự động trên GitHub Actions](img/ci-cd-pipeline.png)

![Hình 5.3: Quy trình tích hợp liên tục trên giao diện GitHub Actions](img/chup-github-actions.png)
> CHỤP: Giao diện web GitHub Actions của kho lưu trữ / workflow Flutter CI/CD Pipeline hiển thị dấu tích xanh thành công cho toàn bộ các bước / truy cập vào tab Actions sau khi đẩy mã nguồn lên nhánh chính.

---

## 5.3. Thử nghiệm trên thiết bị Android thực tế và kết quả đo lường

Nhóm đã cài đặt ứng dụng lên thiết bị Android vật lý để kiểm tra dịch vụ chạy nền, cảm biến phần cứng và tiện ích màn hình chính.

### 5.3.1. Thiết bị thử nghiệm và môi trường triển khai

Bảng 5.2 ghi nhận thông số môi trường thử nghiệm thực tế do nhóm đo lường:

Bảng 5.2: Thông số môi trường và kết quả thử nghiệm trên thiết bị Android thực tế

| Hạng mục | Thông số kỹ thuật ghi nhận thực tế |
|---|---|
| **Dòng máy thử nghiệm** | Xiaomi, model: `25053RT47C` |
| **Giao diện & Hệ điều hành** | Xiaomi HyperOS 3.0 trên nền tảng Android 16 (API Level 36) |
| **Dịch vụ hệ thống** | Tích hợp sẵn Google Play Services chính thức |
| **Phương thức cài đặt** | Gỡ lỗi không dây (*Wireless Debugging*) qua `adb connect` và `adb install` |
| **Gói nhị phân thử nghiệm** | APK Debug (`flutter build apk --debug --dart-define-from-file=.env`) |
| **Dung lượng tệp APK** | Xấp xỉ 204 MB (gói debug chứa biểu tượng gỡ lỗi Dart VM) |
| **Trạng thái khởi chạy** | Ứng dụng mở bình thường, giao diện hiển thị ổn định |
| **Kiểm tra nhật ký Logcat** | Không phát sinh lỗi `FATAL EXCEPTION` hay `AndroidRuntime` của ứng dụng |

### 5.3.2. Đánh giá vận hành và xác thực qua công cụ adb

Nhóm sử dụng công cụ `adb` để xác thực trạng thái tiến trình và dịch vụ nền:
1. **Dịch vụ đếm bước chân chạy nền:** Lệnh `adb shell dumpsys activity services com.nhh031.fitness_tracker` xác nhận `StepCounterService` đang chạy ở tiền cảnh với `isForeground=true`, thuộc tính `foregroundServiceType="health"`. Thông báo thường trực (*Ongoing Notification*) cập nhật số bước trên thanh trạng thái.
2. **Tiện ích màn hình chính (App Widget):** Lệnh `adb shell dumpsys appwidget` ghi nhận `FitnessAppWidgetProvider` hoạt động đúng kích thước 4x2 và cập nhật số bước chân cùng số cốc nước khi có sự kiện làm mới.
3. **Quyền hạn hệ thống:** Lệnh `adb shell cmd appops get com.nhh031.fitness_tracker` xác nhận ứng dụng đã được cấp quyền `ACTIVITY_RECOGNITION` và `POST_NOTIFICATIONS`.

![Hình 5.4: Trạng thái Foreground Service của ứng dụng qua công cụ adb dumpsys](img/chup-adb-dumpsys-service.png)
> CHỤP: Cửa sổ dòng lệnh Terminal máy tính / hiển thị StepCounterService với foregroundServiceType="health" và isForeground=true / kết nối thiết bị thật qua adb và chạy lệnh adb shell dumpsys activity services com.nhh031.fitness_tracker.

### 5.3.3. Đánh giá khách quan các hạn chế trong quá trình thử nghiệm thực tế

Thử nghiệm trên phần cứng thật ghi nhận 3 vấn đề kỹ thuật phát sinh:
1. **Lỗi đăng nhập Google trên bản build máy thử:** Đăng nhập Google không hoàn tất do mã băm chứng chỉ debug SHA-1 của máy thử (`5E:1E:10:40:...`) chưa được đăng ký trong cấu hình Firebase (bảng điều khiển mới lưu mã `DA:A6:36:29:...` của máy lập trình ban đầu). Tuy nhiên, chế độ Khách (*Guest Mode*) hoạt động ổn định, cho phép lưu trữ đầy đủ dữ liệu cục bộ vào SQLite.
2. **Quản lý pin nghiêm ngặt trên HyperOS:** Giao diện HyperOS có xu hướng tạm dừng dịch vụ chạy nền khi màn hình tắt nếu người dùng chưa cấp quyền "Tự khởi động" (*Autostart*) và chưa đặt chế độ pin sang "Không hạn chế".
3. **Kiểm thử AI trên máy thật còn hạn chế:** Chức năng nhận diện món ăn từ ảnh chưa được kiểm thử toàn bộ trên máy thật do cần cấu hình khóa API Gemini hợp lệ tại thời điểm chạy. Khi thiếu khóa, ứng dụng tự kích hoạt cơ chế dự phòng ngoại tuyến từ bộ đệm món ăn có sẵn.

---

## 5.4. Đánh giá và các hạn chế kỹ thuật hiện tại

Qua phân tích mã nguồn và thử nghiệm thực tế, nhóm ghi nhận 8 hạn chế kỹ thuật cốt lõi:

1. **Tranh chấp dữ liệu trên SharedPreferences đa tiến trình:** `StepCounterService.kt` (native) và `StepRepository` (Flutter) đều ghi không đồng bộ bằng `apply()` vào cùng tệp XML `"FlutterSharedPreferences"`. Thiếu cơ chế khóa tệp giữa hai tiến trình độc lập dễ gây sai lệch số bước cơ sở (*baseline offset*).
2. **Phụ thuộc cảm biến phần cứng và chính sách pin OEM:** Thuật toán đếm bước phụ thuộc vào cảm biến `TYPE_STEP_COUNTER`. Trên các thiết bị thiếu cảm biến này hoặc bị hệ điều hành OEM can thiệp khi ngủ sâu, dịch vụ nền có thể bị gián đoạn.
3. **Rủi ro chữ ký số bản phát hành:** Trong `android/app/build.gradle.kts`, khối `buildTypes.release` đang dùng chứng chỉ debug mặc định (`signingConfig = signingConfigs.getByName("debug")`), tiềm ẩn nguy cơ bảo mật nếu phát hành thực tế.
4. **Độ trễ và phụ thuộc API AI đám mây:** Phân tích ảnh món ăn qua Gemini API tạo độ trễ mạng 1,5 đến 3 giây và đòi hỏi Internet liên tục. Ứng dụng chưa tích hợp mô hình thị giác máy tính chạy trực tiếp trên thiết bị (*on-device*).
5. **Lớp StorageService quá tải và trùng lặp gửi dữ liệu mạng:** Lớp `StorageService` dài hơn 2.200 dòng mã kiêm nhiệm quá nhiều nghiệp vụ. Ngoài ra, nhật ký bài tập và món ăn bị gửi lên Cloud Firestore hai lần (*Dual Network Push*) do gọi đồng thời từ Service và Repository.
6. **Hợp nhất dữ liệu cơ bản và thiếu GPS ngoài trời:** Thuật toán đồng bộ giữa SQLite và Firestore áp dụng cơ chế ghi đè theo bản ghi mới nhất (*Last-Write-Wins*). Ứng dụng chưa có GPS để vẽ lộ trình chạy bộ trên bản đồ và thư mục ảnh cục bộ chưa có cơ chế dọn dẹp tự động.
7. **Lỗ hổng không tự động khóa lại trong BiometricGate:** `BiometricGate` chỉ gọi xác thực vân tay khi vòng đời chuyển sang `resumed` mà chưa đặt lại cờ khóa khi ứng dụng chuyển sang `paused`, dẫn đến việc không yêu cầu quét lại vân tay sau khi rời ứng dụng.
8. **Thiếu kiểm thử tự động cho tầng Native Kotlin:** Dự án chưa có bài kiểm thử JUnit nào cho các tệp Kotlin (`StepCounterService.kt`, `BootReceiver.kt`) trong thư mục `src/test` hoặc `src/androidTest`.

Bảng 5.3: Phân tích các hạn chế kỹ thuật cốt lõi và hướng khắc phục

| STT | Vấn đề kỹ thuật | Nguyên nhân cụ thể | Hướng khắc phục kỹ thuật |
|:---:|---|---|---|
| 1 | Race condition trên SharedPreferences | Tiến trình Kotlin và luồng Flutter ghi đồng thời vào tệp XML | Chuyển sang dùng Room Database native (chế độ WAL) hoặc ContentProvider |
| 2 | Service nền bị dừng trên máy OEM | Quản lý pin nghiêm ngặt trên HyperOS/OneUI khi tắt màn hình | Hướng dẫn người dùng bật Autostart và chọn chế độ pin Không hạn chế |
| 3 | Bản release dùng debug keystore | `build.gradle.kts` gán debug signing cho cấu hình release | Tạo tệp `key.properties`, nạp chứng chỉ ký số chính thức từ biến môi trường bí mật |
| 4 | Phụ thuộc dịch vụ AI đám mây | Gọi API Gemini Cloud Vision qua kết nối mạng | Nghiên cứu tích hợp mô hình Gemini Nano chạy cục bộ trên thiết bị qua Android AICore |
| 5 | Lớp `StorageService` quá tải | Gom toàn bộ nghiệp vụ lưu trữ vào một lớp duy nhất | Phân chia thành các service nghiệp vụ chuyên biệt; loại bỏ lệnh gọi Firestore trùng lặp |
| 6 | Thiếu theo dõi lộ trình GPS | Chưa tích hợp API vị trí và thư viện bản đồ | Bổ sung module GPS kết hợp thư viện OpenStreetMap hoặc Google Maps |
| 7 | Chưa tự động khóa lại sinh trắc | Thiếu lệnh đặt lại cờ khóa khi vòng đời app chuyển sang `paused` | Đặt cờ khóa ngay khi ứng dụng rời màn hình chính trong `didChangeAppLifecycleState` |
| 8 | Thiếu kiểm thử tự động lớp Native | Chưa viết JUnit test cho các tệp Kotlin | Bổ sung bộ kiểm thử JUnit 4/Robolectric cho `StepCounterService` và `BootReceiver` |

---

## 5.5. Hướng phát triển trong tương lai

Dựa trên các hạn chế kỹ thuật đã phân tích, nhóm đề xuất 5 hướng phát triển tiếp theo:

1. **Đồng bộ hai chiều với Android Health Connect và Wear OS:** Nâng cấp `HealthSyncService` để trao đổi nhịp tim, giấc ngủ và bước chân với nền tảng Health Connect của Google; phát triển ứng dụng đồng hành cho đồng hồ Wear OS.
2. **Bổ sung module định vị GPS và vẽ bản đồ lộ trình:** Sử dụng `FusedLocationProviderClient` của Android để ghi nhận tọa độ GPS khi chạy bộ ngoài trời, tính vận tốc và vẽ lộ trình di chuyển trên nền bản đồ số OpenStreetMap hoặc Google Maps SDK.
3. **Tích hợp mô hình AI chạy trực tiếp trên thiết bị (On-Device AI):** Nghiên cứu tích hợp mô hình Gemini Nano qua Android AICore để nhận diện thực phẩm khi mất kết nối mạng, giảm độ trễ và bảo vệ quyền riêng tư dữ liệu ảnh.
4. **Tái cấu trúc kiến trúc phần mềm và tầng lưu trữ:** Chuyển đổi quản lý trạng thái sang BLoC hoặc Riverpod; thay thế việc chia sẻ SharedPreferences đa tiến trình bằng Room Database hoặc ContentProvider ở tầng Native.
5. **Nâng cao an toàn thông tin và hoàn thiện kiểm thử native:** Mã hóa dữ liệu lưu trữ cục bộ bằng Android Keystore qua `flutter_secure_storage`; bổ sung bộ kiểm thử JUnit và Robolectric cho mã nguồn Kotlin trên pipeline CI/CD.

---

## 5.6. Kết luận

Đề tài **"Xây dựng ứng dụng theo dõi sức khỏe và luyện tập Fitness Tracker trên nền tảng Android tích hợp trí tuệ nhân tạo Gemini"** đã hoàn thành các mục tiêu kỹ thuật đề ra, đáp ứng yêu cầu của môn học Lập trình Android nâng cao.

### Tổng kết các kết quả đạt được
Ứng dụng kết hợp hiệu quả giữa nền tảng Flutter và các kỹ thuật native của hệ điều hành Android:
- **Tầng Native Android:** Khai thác Foreground Service loại `health` kết hợp cảm biến phần cứng `TYPE_STEP_COUNTER` gộp mẫu 10 giây; tự phục hồi dịch vụ sau khởi động máy qua `BootReceiver`; xây dựng tiện ích màn hình chính (*App Widget*) với `RemoteViews`; quản lý kênh thông báo hẹn giờ chính xác.
- **Cầu nối nền tảng:** Thiết lập liên lạc hai chiều giữa Dart và Kotlin qua `MethodChannel` và `EventChannel` để truyền nhận sự kiện bước chân và cập nhật widget.
- **Lưu trữ dữ liệu:** Áp dụng mô hình ưu tiên cục bộ (*Local-First*) với cơ sở dữ liệu SQLite 7 bảng, kết hợp đồng bộ hóa đám mây Cloud Firestore.
- **Tích hợp Trí tuệ nhân tạo:** Tích hợp mô hình Gemini AI vào bài toán phân tích dinh dưỡng và gợi ý bài tập, đi kèm bộ đệm ngoại tuyến dự phòng khi mất mạng.
- **Đảm bảo chất lượng:** Đạt 123/123 bài kiểm thử tự động, 0 lỗi phân tích tĩnh và thiết lập quy trình CI/CD trên GitHub Actions. Thử nghiệm trên thiết bị Xiaomi HyperOS 3.0 (Android 16) đã xác nhận tính ổn định và chỉ ra các bài học thực tế về quản lý tiến trình nền của hệ điều hành.

### Giá trị học thuật và thực tiễn thu hoạch được
Thông qua đề tài, nhóm đã tích lũy được những kiến thức giá trị:
- Nắm vững vòng đời tiến trình, cơ chế quản lý năng lượng Doze mode và giới hạn chạy nền trên các phiên bản Android hiện đại.
- Thành thạo kỹ thuật tương tác với phần cứng thiết bị, xử lý cảm biến và giao tiếp qua Platform Channel.
- Hiểu rõ sự khác biệt giữa môi trường kiểm thử lý thuyết và hành vi thực tế của các dòng máy OEM, từ đó rèn luyện phương pháp tiếp cận kỹ thuật cẩn trọng, thực chứng và khách quan.

Kết quả của đồ án tạo tiền đề vững chắc để các thành viên trong nhóm tiếp tục nghiên cứu và phát triển các giải pháp phần mềm di động trong thực tế.

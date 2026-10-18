# PHỤ LỤC

## Phụ lục A: Bảng tổng hợp quyền Android Manifest

Ứng dụng khai báo các quyền hệ thống trong tệp tin `AndroidManifest.xml` nhằm phục vụ việc thu thập dữ liệu cảm biến bước chân nền, thông báo tiến độ, quét mã vạch và đồng bộ các chỉ số sức khỏe.

Bảng A.1: Danh mục quyền hệ thống khai báo trong AndroidManifest.xml

| Tên quyền | Mức độ bảo vệ | API Level | Mục đích trong ứng dụng |
|---|---|---|---|
| `android.permission.ACTIVITY_RECOGNITION` | Nguy hiểm (Runtime) | API 29+ | Nhận diện vận động và đọc số bước từ cảm biến phần cứng `TYPE_STEP_COUNTER` |
| `android.permission.FOREGROUND_SERVICE` | Thông thường (Normal) | API 28+ | Cho phép khởi chạy `StepCounterService` chạy nền dưới dạng dịch vụ tiền cảnh |
| `android.permission.FOREGROUND_SERVICE_HEALTH` | Thông thường (Normal) | API 34+ | Phân loại mục đích dịch vụ tiền cảnh chuyên biệt cho theo dõi sức khỏe theo chuẩn Android 14+ |
| `android.permission.POST_NOTIFICATIONS` | Nguy hiểm (Runtime) | API 33+ | Hiển thị thông báo tiến độ bước chân, thông báo nhắc uống nước và đồng hồ đếm ngược nghỉ hiệp |
| `android.permission.RECEIVE_BOOT_COMPLETED` | Thông thường (Normal) | API 1+ | Cho phép `BootReceiver` nhận tín hiệu khởi động máy để tự động kích hoạt lại dịch vụ đếm bước |
| `android.permission.SCHEDULE_EXACT_ALARM` | Đặc biệt (Special) | API 31+ | Lên lịch thông báo nhắc uống nước chính xác theo từng khung giờ cố định |
| `android.permission.USE_EXACT_ALARM` | Thông thường (Normal) | API 33+ | Cho phép sử dụng cơ chế báo thức chính xác cho các tác vụ nhắc nhở định kỳ |
| `android.permission.VIBRATE` | Thông thường (Normal) | API 1+ | Kích hoạt rung phản hồi xúc giác (`AppHaptics`) và rung báo hiệu khi kết thúc hiệp nghỉ |
| `android.permission.RECORD_AUDIO` | Nguy hiểm (Runtime) | API 1+ | Thu âm giọng nói phục vụ chuyển đổi âm thanh thành văn bản khi ghi chép dinh dưỡng |
| `android.permission.INTERNET` | Thông thường (Normal) | API 1+ | Kết nối mạng truy vấn mô hình Gemini AI, cơ sở dữ liệu Open Food Facts và Firebase |
| `android.permission.CAMERA` | Nguy hiểm (Runtime) | API 1+ | Chụp ảnh món ăn để AI nhận diện và quét mã vạch bao bì thực phẩm qua `mobile_scanner` |
| `android.permission.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` | Thông thường (Normal) | API 23+ | Mở màn hình hệ thống yêu cầu người dùng loại trừ ứng dụng khỏi danh sách tối ưu hóa pin Doze Mode |
| `android.permission.USE_BIOMETRIC` | Thông thường (Normal) | API 28+ | Sử dụng cảm biến vân tay hoặc khuôn mặt qua `BiometricPrompt` để bảo vệ ứng dụng |
| `android.permission.health.READ_STEPS` | Quyền Health Connect | API 34+ / App | Đọc dữ liệu bước chân lưu trữ trong kho dữ liệu Google Health Connect |
| `android.permission.health.READ_HEART_RATE` | Quyền Health Connect | API 34+ / App | Đọc dữ liệu nhịp tim từ Google Health Connect để phân tích thể trạng |
| `android.permission.health.READ_TOTAL_CALORIES_BURNED` | Quyền Health Connect | API 34+ / App | Đọc tổng lượng calo tiêu hao tổng hợp từ Google Health Connect |
| `android.permission.health.READ_SLEEP` | Quyền Health Connect | API 34+ / App | Đọc dữ liệu các phiên giấc ngủ từ Google Health Connect |

---

## Phụ lục B: Bảng danh mục Platform Channels

Tầng cầu nối nền tảng (*Platform Bridge*) kết nối mã nguồn Dart của Flutter Engine với lớp native Android Kotlin (`MainActivity`, `StepCounterService`, `FitnessAppWidgetProvider`) thông qua hai kênh truyền thông điệp và cơ chế tệp cấu hình dùng chung.

Bảng B.1: Danh mục Platform Channels giao tiếp Flutter và Android Native

| Loại kênh | Tên định danh kênh | Tên phương thức / Sự kiện | Chiều gọi | Kiểu tham số & Trả về | Chức năng chi tiết |
|---|---|---|---|---|---|
| `MethodChannel` | `com.example.fitness_tracker/service` | `startService` | Dart $\to$ Kotlin | Tham số: `null`<br>Trả về: `void` | Khởi chạy dịch vụ tiền cảnh `StepCounterService` thông qua `startForegroundService` |
| `MethodChannel` | `com.example.fitness_tracker/service` | `isIgnoringBatteryOptimizations` | Dart $\to$ Kotlin | Tham số: `null`<br>Trả về: `Boolean` | Kiểm tra ứng dụng đã được đưa vào danh sách trắng miễn trừ Doze Mode hay chưa |
| `MethodChannel` | `com.example.fitness_tracker/service` | `requestIgnoreBatteryOptimizations` | Dart $\to$ Kotlin | Tham số: `null`<br>Trả về: `Boolean` | Mở Intent hệ thống yêu cầu người dùng xác nhận bỏ qua tối ưu hóa pin |
| `MethodChannel` | `com.example.fitness_tracker/service` | `updateWidget` | Dart $\to$ Kotlin | Tham số: `null`<br>Trả về: `Boolean` | Yêu cầu `FitnessAppWidgetProvider` cập nhật lại giao diện `RemoteViews` cho mọi widget |
| `EventChannel` | `com.example.fitness_tracker/steps` | `onListen` / Luồng sự kiện | Kotlin $\to$ Dart | Phát ra: `Int` (số bước phần cứng) | Truyền luồng dữ liệu bước chân từ cảm biến phần cứng qua `stepReceiver` tới Flutter UI |
| `EventChannel` | `com.example.fitness_tracker/steps` | `onCancel` | Dart $\to$ Kotlin | Tham số: `null`<br>Trả về: `void` | Hủy đăng ký `BroadcastReceiver` nội bộ khi Flutter UI ngừng lắng nghe sự kiện |

Bảng B.2: Danh mục khóa trạng thái chia sẻ qua FlutterSharedPreferences

| Tên khóa (Key XML) | Kiểu dữ liệu | Thành phần đọc/ghi Native | Thành phần đọc/ghi Dart | Ý nghĩa và mục đích |
|---|---|---|---|---|
| `flutter.today_steps` | `Long` (Kotlin) / `int` (Dart) | `StepCounterService` (ghi)<br>`FitnessAppWidgetProvider` (đọc) | `StepRepository` (đọc/ghi)<br>`StorageService` (đọc/ghi) | Số bước chân tích lũy trong ngày hiện tại |
| `flutter.water_cups_today` | `Long` (Kotlin) / `int` (Dart) | `FitnessAppWidgetProvider` (đọc) | `WaterRepository` (đọc/ghi)<br>`StorageService` (đọc/ghi) | Số cốc nước đã uống trong ngày hiện tại |
| `flutter.step_baseline_hardware` | `Long` (Kotlin) / `int` (Dart) | `StepCounterService` (đọc/ghi) | `StepRepository` (đọc/ghi) | Giá trị cảm biến phần cứng ghi nhận tại thời điểm bắt đầu tính mốc |
| `flutter.step_baseline_date` | `String` | `StepCounterService` (đọc/ghi) | `StepRepository` (đọc/ghi) | Chuỗi ngày xác định mốc tính toán hiện tại (định dạng `yyyy-MM-dd`) |
| `flutter.step_reboot_offset` | `Long` (Kotlin) / `int` (Dart) | `StepCounterService` (đọc/ghi) | `StepRepository` (đọc/ghi) | Số bước chân bù trừ tích lũy trước khi thiết bị khởi động lại |

---

## Phụ lục C: Danh mục lệnh ADB kiểm tra ứng dụng trên thiết bị

Công cụ dòng lệnh ADB (*Android Debug Bridge*) được sử dụng trong quá trình kiểm thử để kiểm tra trạng thái hoạt động của tiến trình nền, giả lập các sự kiện hệ thống, kiểm soát quyền và thu thập thông tin gỡ lỗi trên thiết bị thật (`com.nhh031.fitness_tracker`).

Bảng C.1: Danh mục lệnh ADB kiểm thử và giám sát ứng dụng trên thiết bị

| Nhóm tác vụ | Lệnh ADB thực thi | Mục đích và ý nghĩa kỹ thuật | Kết quả quan sát mong đợi |
|---|---|---|---|
| **Dịch vụ nền** | `adb shell dumpsys activity services com.nhh031.fitness_tracker` | Kiểm tra trạng thái của `StepCounterService` | Xuất hiện `isForeground=true`, `foregroundServiceType=health` và thông tin Notification ID |
| **Dịch vụ nền** | `adb shell ps -A \| grep com.nhh031.fitness_tracker` | Kiểm tra tiến trình ứng dụng đang chạy trong hệ điều hành | Hiển thị PID của tiến trình chính tương ứng với gói ứng dụng |
| **Tiết kiệm pin** | `adb shell dumpsys deviceidle whitelist` | Kiểm tra xem ứng dụng đã nằm trong danh sách trắng Doze Mode hay chưa | Danh sách hiển thị tên gói `com.nhh031.fitness_tracker` nếu người dùng đã cấp quyền |
| **Tiết kiệm pin** | `adb shell cmd deviceidle step deep` | Ép thiết bị vào trạng thái Doze Mode sâu để kiểm tra tính bền bỉ của service | `StepCounterService` vẫn tiếp tục đếm bước khi CPU chuyển sang trạng thái ngủ |
| **Broadcast** | `adb shell am broadcast -a android.intent.action.BOOT_COMPLETED -p com.nhh031.fitness_tracker` | Giả lập sự kiện hoàn tất khởi động máy để kiểm tra `BootReceiver` | `BootReceiver` tiếp nhận Intent và gọi `startForegroundService` kích hoạt lại bộ đếm bước |
| **Broadcast** | `adb shell am broadcast -a android.intent.action.MY_PACKAGE_REPLACED -p com.nhh031.fitness_tracker` | Giả lập sự kiện cập nhật ứng dụng thành công | Dịch vụ đếm bước tự động khởi chạy lại mà không cần người dùng mở app |
| **App Widget** | `adb shell dumpsys appwidget com.nhh031.fitness_tracker` | Kiểm tra thông tin các thực thể App Widget đang được gắn trên màn hình chính | Xuất hiện thông tin kích thước và component `FitnessAppWidgetProvider` |
| **Phân quyền** | `adb shell pm grant com.nhh031.fitness_tracker android.permission.ACTIVITY_RECOGNITION` | Cấp quyền nhận diện vận động qua dòng lệnh | Quyền chuyển sang trạng thái `granted` mà không cần hiển thị hộp thoại giao diện |
| **Phân quyền** | `adb shell pm grant com.nhh031.fitness_tracker android.permission.POST_NOTIFICATIONS` | Cấp quyền hiển thị thông báo trên Android 13+ | Thông báo tiến độ bước chân xuất hiện ngay trên thanh trạng thái |
| **Phân quyền** | `adb shell pm revoke com.nhh031.fitness_tracker android.permission.ACTIVITY_RECOGNITION` | Thu hồi quyền nhận diện vận động để kiểm tra cơ chế xử lý lỗi | Giao diện Flutter hiển thị thông báo hướng dẫn người dùng cấp lại quyền |
| **Dữ liệu chia sẻ** | `adb shell run-as com.nhh031.fitness_tracker cat /data/data/com.nhh031.fitness_tracker/shared_prefs/FlutterSharedPreferences.xml` | Đọc nội dung tệp SharedPreferences native dùng chung | Hiển thị các trường `flutter.today_steps`, `flutter.water_cups_today` với giá trị đồng bộ |
| **Nhật ký Logcat** | `adb logcat -s StepCounterService:V FitnessAppWidget:V flutter:V MainActivity:V` | Lọc thông tin nhật ký hệ thống của các thành phần native và Flutter | Hiển thị chi tiết từng sự kiện cảm biến phần cứng và lệnh cập nhật widget |
| **Kiểm tra crash** | `adb logcat *:E \| grep -E "FATAL\|AndroidRuntime"` | Bắt nhanh các ngoại lệ nghiêm trọng gây dừng ứng dụng đột ngột | Không có lỗi ngoại lệ `FATAL EXCEPTION` xuất phát từ gói ứng dụng |
| **Chụp ảnh bằng chứng** | `adb exec-out screencap -p > docs/report/img/chup-adb-dumpsys.png` | Xuất trực tiếp ảnh chụp màn hình thiết bị vào thư mục báo cáo | Tệp ảnh PNG chứa kết quả kiểm thử được tạo lập thành công |

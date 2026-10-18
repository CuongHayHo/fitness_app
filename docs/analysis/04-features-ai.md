# Phân tích Nghiệp vụ & AI (W4)

## 1. Tóm tắt
Phân hệ Nghiệp vụ & Trí tuệ Nhân tạo (W4) của Fitness Tracker tích hợp mô hình Gemini AI thế hệ mới (`gemini-3.8-flash`, dự phòng `gemini-3.7-flash`) cùng Open Food Facts REST API v2, biến ứng dụng thành trợ lý sức khỏe cá nhân thông minh. Hệ thống hỗ trợ nhập liệu dinh dưỡng đa phương thức (giọng nói qua STT, camera chụp món ăn qua Multimodal Vision, quét mã vạch và nhập văn bản), trò chuyện tư vấn dinh dưỡng thời gian thực dạng Streaming (SSE), tự động tạo giáo án tập luyện cá nhân hóa theo thiết bị và sinh trắc học, cùng cơ chế dự phòng ngoại tuyến hoàn chỉnh (Offline Clinical Engine & Nutrition Cache) đảm bảo tính sẵn sàng cao ngay cả khi mất mạng.

## 2. Chức năng

| Chức năng | Mô tả ngắn | file:line |
|---|---|---|
| **Cấu hình & Quản lý API Key kép** | Hỗ trợ nạp API Key an toàn qua compile-time `--dart-define=GEMINI_API_KEY` (hoặc `.env`) và cho phép người dùng nhập khóa động lúc runtime lưu trong bộ nhớ. | `lib/services/gemini_service.dart:43-62` |
| **Cơ chế chuyển đổi dự phòng mô hình AI (Model Fallback)** | Tự động chuyển tiếp yêu cầu từ model chính `gemini-3.8-flash` sang `gemini-3.7-flash` khi gặp sự cố mạng, quá tải quota hoặc lỗi kết nối. | `lib/services/gemini_service.dart:41-42,76-94` |
| **Phản hồi luồng thời gian thực (Streaming AI Response)** | Hỗ trợ phát sinh nội dung dạng stream (`Stream<String>`) cho phép giao diện hiển thị câu trả lời dạng gõ chữ mượt mà với cơ chế fallback tự động. | `lib/services/gemini_service.dart:97-130,600-668` |
| **Trích xuất & Làm sạch JSON thông minh** | Tự động loại bỏ thẻ định dạng markdown (```json), cắt lọc chuỗi bao quanh và phân tích cú pháp chuỗi JSON trả về từ mô hình AI thành thực thể Dart. | `lib/services/gemini_service.dart:133-155` |
| **Bộ nhớ đệm dinh dưỡng không độ trễ (Offline Cache)** | Lưu trữ sẵn 23 món ăn Việt Nam & thể hình phổ biến cùng cơ chế tìm kiếm gần đúng (fuzzy search), tự động lưu kết quả mới tra cứu vào RAM. | `lib/services/gemini_service.dart:158-208` |
| **Phân tích dinh dưỡng qua văn bản / giọng nói** | Phân tích mô tả món ăn tự do từ chuỗi văn bản hoặc giọng nói chuyển đổi để ước tính calo, đạm (protein), tinh bột (carbs) và chất béo (fat). | `lib/services/gemini_service.dart:192-245` |
| **Tính toán khẩu phần ăn lâm sàng (Portion Engine)** | Công thức tính dinh dưỡng chuẩn y khoa theo trọng lượng gam (cơm, thịt, rau) kèm gọi AI phân tích món phức hợp và tự động fallback về engine ngoại tuyến. | `lib/services/gemini_service.dart:248-386,390-452` |
| **Nhận diện món ăn qua hình ảnh (Multimodal Vision)** | Tự động nhận diện định dạng ảnh (JPEG, PNG, WebP) từ byte header và gửi kèm prompt tới Gemini Vision để bóc tách dinh dưỡng đĩa ăn. | `lib/services/gemini_service.dart:454-521` |
| **Chuyên gia dinh dưỡng AI (AI Nutritionist Chat)** | Hộp thoại tư vấn dinh dưỡng thông minh liên kết trực tiếp với hồ sơ sinh trắc học người dùng (BMI, BMR, TDEE) và nhật ký ăn uống thực tế trong ngày. | `lib/services/gemini_service.dart:524-668`, `lib/widgets/ai_nutritionist_chat_dialog.dart:83-150` |
| **Khởi tạo bài tập tùy biến (AI Workout Routine)** | Sinh giáo án tập luyện theo thời lượng (10–180 phút), mục tiêu thể hình, trang bị sẵn có (bodyweight, tạ đơn, kết hợp) kèm bộ tạo bài tập ngoại tuyến 100%. | `lib/services/gemini_service.dart:671-1004`, `lib/widgets/ai_coach_card_widget.dart:24-73,181-220` |
| **Bản tin AI huấn luyện viên buổi sáng (Daily AI Briefing)** | Đánh giá tổng quan năng lượng nạp/tiêu hao, số bước chân, lượng nước ngày hôm trước để đưa ra thông điệp truyền cảm hứng và mẹo hành động cho ngày mới. | `lib/services/gemini_service.dart:1007-1235`, `lib/widgets/daily_ai_briefing_widget.dart:55-89` |
| **Tra cứu mã vạch qua Open Food Facts API** | Quét mã vạch sản phẩm bánh kẹo, đồ hộp, gửi REST request v2 để lấy tên sản phẩm tiếng Việt/Anh, năng lượng (kcal/kJ) và macro, hỗ trợ nhân khẩu phần. | `lib/services/open_food_facts_service.dart:6-43,53-141` |
| **Tính toán sinh trắc học chuẩn y khoa (User Metrics)** | Cung cấp thuật toán BMR Mifflin-St Jeor, TDEE, calo thâm hụt/dư thừa, calo bước chân (0.04 kcal/bước), chiều dài sải chân và % mỡ cơ thể US Navy. | `lib/services/user_metrics_service.dart:10-218` |
| **Game hóa & Hệ thống huy hiệu thành tích** | Theo dõi 9 danh hiệu (chuỗi rèn luyện, hydration, đi bộ 10k bước, 3 bữa ăn) kèm bus sự kiện phát sóng mở khóa huy hiệu và rung phản hồi xúc giác. | `lib/services/achievement_service.dart:8-109,151-238` |
| **Xuất & Chia sẻ báo cáo 30 ngày qua Share Sheet** | Tổng hợp hồ sơ hội viên, số đo US Navy, nhật ký 30 ngày tập luyện & dinh dưỡng thành tệp văn bản đính kèm chia sẻ qua ứng dụng ngoài (Zalo, Gmail). | `lib/services/report_export_service.dart:14-176` |
| **Hệ thống đa ngôn ngữ động (i18n Localization)** | Tải tệp ngôn ngữ JSON qua AssetBundle, chuyển đổi linh hoạt qua ValueNotifier và hỗ trợ nội suy tham số chuỗi `{key}` tức thời. | `lib/services/locale_service.dart:10-74` |
| **Giao diện ghi nhận món ăn đa phương thức** | Giao diện hợp nhất nhận diện văn bản, ghi âm giọng nói qua `SpeechService`, chụp ảnh qua `ImagePicker`, và kích hoạt sheet quét mã vạch. | `lib/widgets/ai_food_logging_widget.dart:30-46,121-220,344-436` |

## 3. Kỹ thuật Android/Flutter

| Kỹ thuật / API | Cách dùng trong dự án | file:line | API level / Quyền liên quan |
|---|---|---|---|
| **Google Generative AI SDK (`google_generative_ai`)** | Tích hợp gói SDK chính thức của Google, tạo `GenerativeModel` truyền `systemInstruction`, điều phối lệnh gọi `generateContent` và `generateContentStream`. | `lib/services/gemini_service.dart:3,64-94,102-124` | Android API 1+, quyền `android.permission.INTERNET` |
| **Phân tích Byte Header & MIME Detection** | Kiểm tra byte signature ma trận đầu vào (`0x89 0x50 0x4E 0x47` cho PNG, `RIFF...WEBP` cho WebP) để gán đúng MIME type cho `DataPart` của Gemini Multimodal. | `lib/services/gemini_service.dart:454-474,502-506` | Dart Typed Data (`Uint8List`), không yêu cầu quyền native |
| **Open Food Facts REST Client (`http`)** | Gửi yêu cầu HTTP GET với User-Agent tùy chỉnh (`FitnessTrackerApp - Android - Version 1.0.0`) theo đúng chính sách Open Food Facts, cài đặt timeout 8 giây. | `lib/services/open_food_facts_service.dart:3,58-65` | Android API 1+, quyền `android.permission.INTERNET` |
| **Ghi âm & Nhận dạng giọng nói (`speech_to_text`)** | Tích hợp Android `RecognitionService` lắng nghe khẩu lệnh mô tả món ăn, cập nhật trực tiếp văn bản vào `TextEditingController` để gửi sang Gemini. | `lib/widgets/ai_food_logging_widget.dart:30,86-109,121-137`, `AndroidManifest.xml:13,107-111` | API 23+, quyền `android.permission.RECORD_AUDIO`, `<queries>` Speech Service |
| **Chụp ảnh & Thư viện ảnh (`image_picker`)** | Gọi Intent hệ thống chụp ảnh hoặc mở thư viện ảnh (`ImageSource.camera` / `gallery`), nén chất lượng 85% và giới hạn độ phân giải tối đa 1024x1024. | `lib/widgets/ai_food_logging_widget.dart:32,344-352` | API 21+, quyền `android.permission.CAMERA`, Android Photo Picker (API 33+) |
| **Quét mã vạch CameraX (`mobile_scanner`)** | Kích hoạt màn hình quét mã vạch tốc độ cao bọc trên CameraX Android, thu nhận mã Barcode EAN-13/UPC và truyền sang `OpenFoodFactsService`. | `lib/widgets/ai_food_logging_widget.dart:327-334`, `lib/widgets/barcode_scanner_sheet.dart:1-50` | API 21+, quyền `android.permission.CAMERA` |
| **Lưu tệp tạm Cache & File Sharing (`path_provider`, `share_plus`)** | Ghi tệp báo cáo vào thư mục cache ứng dụng (`getTemporaryDirectory()`), kích hoạt `SharePlus` mở Intent Android `ACTION_SEND` kèm `FileProvider` an toàn. | `lib/services/report_export_service.dart:3-4,156-176` | API 21+, Android `FileProvider`, `FLAG_GRANT_READ_URI_PERMISSION` |
| **Phản hồi rung xúc giác (`AppHaptics`)** | Gọi `HapticFeedback.mediumImpact()` và `HapticFeedback.vibrate()` thông qua `AppHaptics.success()` khi ghi nhận món ăn hoặc mở khóa huy hiệu. | `lib/utils/app_haptics.dart:1-25`, `lib/services/achievement_service.dart:233`, `lib/widgets/ai_food_logging_widget.dart:174` | API 1+, quyền `android.permission.VIBRATE` |
| **Bus sự kiện bất đồng bộ (`StreamController.broadcast`)** | Tạo bus sự kiện phát sóng luồng huy hiệu `onBadgeUnlocked`, cho phép các thành phần UI toàn ứng dụng lắng nghe và hiển thị popup chúc mừng. | `lib/services/achievement_service.dart:9-13,234` | Dart Core Async (`StreamController`) |
| **Lưu trữ cấu hình & Huy hiệu (`SharedPreferences`)** | Sử dụng SharedPreferences XML của Android lưu trữ danh sách huy hiệu đã đạt (`unlocked_achievement_badges_v1`), ngôn ngữ ứng dụng và cache Daily AI Briefing. | `lib/services/achievement_service.dart:113-125,229`, `lib/services/locale_service.dart:27,55`, `lib/services/storage_service.dart:1907,1922` | API 1+, lưu trữ nội bộ private app storage |
| **Quản lý trạng thái phản ứng (`ValueNotifier`)** | Sử dụng `ValueNotifier<String>` quản lý ngôn ngữ toàn cục, tái dựng giao diện tức thì khi người dùng đổi ngôn ngữ mà không cần restart app hay thư viện nặng. | `lib/services/locale_service.dart:10,58` | Flutter Foundation (`ValueNotifier`) |
| **Nạp tài nguyên gói ứng dụng (`rootBundle`)** | Đọc dữ liệu từ `AssetManager` Android giải nén tệp `assets/i18n/vi.json` và `en.json` vào bộ nhớ RAM lúc khởi tạo ứng dụng. | `lib/services/locale_service.dart:38-40` | Flutter Services `rootBundle` |

```dart
// Minh họa cơ chế chuyển đổi dự phòng mô hình AI (Model Fallback)
static Future<GenerateContentResponse> _generateWithFallback(
  List<Content> contents, {Content? systemInstruction}
) async {
  try {
    return await _createModel(
      modelName: _modelName, // gemini-3.8-flash
      systemInstruction: systemInstruction,
    ).generateContent(contents);
  } catch (primaryErr) {
    debugPrint("⚠️ [GeminiService] Model chính lỗi: $primaryErr. Chuyển sang dự phòng $_fallbackModelName...");
    return await _createModel(
      modelName: _fallbackModelName, // gemini-3.7-flash
      systemInstruction: systemInstruction,
    ).generateContent(contents);
  }
}
```
*(Trích đoạn mã nguồn: `lib/services/gemini_service.dart:76-94`)*

## 4. Luồng xử lý chính

Sơ đồ tuần tự sau đây mô tả toàn diện luồng nhập liệu dinh dưỡng thông minh (Văn bản, Giọng nói, Hình ảnh camera, Mã vạch) kết hợp cơ chế dự phòng nhiều tầng và phản ứng thành tích:

```mermaid
sequenceDiagram
    autonumber
    actor User as Người dùng
    participant UI as AiFoodLoggingWidget
    participant STT as SpeechService
    participant Cam as ImagePicker / BarcodeScanner
    participant OFF as OpenFoodFactsService
    participant Gemini as GeminiService
    participant Cache as NutritionCache / Engine
    participant DB as StorageService (SQLite)
    participant Ach as AchievementService

    alt Nhập bằng giọng nói (Voice)
        User->>UI: Nhấn giữ Mic & nói món ăn
        UI->>STT: startListening() [ai_food_logging_widget.dart:128]
        STT-->>UI: Nhận diện chuỗi văn bản [ai_food_logging_widget.dart:132]
        UI->>Gemini: analyzeFood(text) [ai_food_logging_widget.dart:161]
    else Chụp ảnh đĩa thức ăn (Vision)
        User->>UI: Chụp ảnh món ăn qua Camera
        UI->>Cam: pickImage() [ai_food_logging_widget.dart:346]
        Cam-->>UI: imageBytes (Uint8List) [ai_food_logging_widget.dart:409]
        UI->>Gemini: analyzeFoodImage(bytes) [ai_food_logging_widget.dart:410]
    else Quét mã vạch bao bì (Barcode)
        User->>UI: Quét mã vạch sản phẩm
        UI->>Cam: BarcodeScannerSheet.show() [ai_food_logging_widget.dart:327]
        Cam->>OFF: fetchProductByBarcode(barcode) [open_food_facts_service.dart:53]
        OFF-->>UI: ScannedFoodProduct (kcal, macros) [open_food_facts_service.dart:126]
    end

    opt Nếu gọi phân tích Gemini
        Gemini->>Cache: Kiểm tra cache tức thì (_nutritionCache) [gemini_service.dart:197]
        alt Cache Hit / Khớp từ khóa
            Cache-->>Gemini: Trả về kết quả món ăn [gemini_service.dart:199,206]
        else Cache Miss -> Gọi Cloud AI
            Gemini->>Gemini: Gọi model gemini-3.8-flash [gemini_service.dart:81]
            alt Lỗi model chính
                Gemini->>Gemini: Fallback sang gemini-3.7-flash [gemini_service.dart:89]
            end
            Gemini->>Gemini: parseFoodJson() trích xuất JSON [gemini_service.dart:133]
            Gemini->>Cache: Lưu món mới vào _nutritionCache [gemini_service.dart:236]
        end
    end

    UI->>DB: logFoodItem(food) lưu vào SQLite [ai_food_logging_widget.dart:173]
    UI->>Ach: checkBadges() đánh giá mở khóa [ai_food_logging_widget.dart:175]
    Ach->>Ach: Rung xúc giác & phát onBadgeUnlocked [achievement_service.dart:233-234]
    UI-->>User: Cập nhật chỉ số Calo/Macro & hiển thị SnackBar thành công [ai_food_logging_widget.dart:186]
```

## 5. Hạn chế & rủi ro

- **Cố định tên mô hình Gemini trong mã nguồn**: Các hằng số `_modelName = 'gemini-3.8-flash'` và `_fallbackModelName = 'gemini-3.7-flash'` được khai báo cứng (`lib/services/gemini_service.dart:41-42`). Nếu Google khai tử hoặc đổi endpoint của các mô hình này trong tương lai, ứng dụng sẽ bị tê liệt phân hệ AI nếu không phát hành bản cập nhật mới.
- **API Key lưu trong bộ nhớ biến tĩnh (In-memory Static)**: Biến `_runtimeApiKey` (`lib/services/gemini_service.dart:43,55-57`) chỉ lưu trên RAM. Khi hệ điều hành thu hồi tiến trình (process death), khóa này sẽ bị xóa nếu người dùng chưa thiết lập compile-time define, buộc phải nhập lại trong màn hình cài đặt.
- **Rủi ro rò rỉ dữ liệu sinh trắc học cá nhân**: Toàn bộ dữ liệu nhạy cảm bao gồm cân nặng, chiều cao, BMI, BMR, TDEE, độ tuổi, giới tính và chi tiết các bữa ăn trong ngày được ghép thẳng vào nội dung prompt gửi lên máy chủ Google (`lib/services/gemini_service.dart:543-555,620-632,677-689`), tiềm ẩn vấn đề bảo mật quyền riêng tư (Privacy/GDPR).
- **Bộ nhớ đệm dinh dưỡng không bền vững (Non-persistent Cache)**: Bảng `_nutritionCache` (`lib/services/gemini_service.dart:158-182`) chỉ tồn tại trong bộ nhớ ứng dụng. Tất cả các món ăn mới được AI phân tích và lưu vào cache sẽ bị mất khi ứng dụng tắt, không được đồng bộ xuống SQLite.
- **Cơ chế phân tích JSON dựa trên cắt chuỗi thô**: Hàm `parseFoodJson` (`lib/services/gemini_service.dart:133-155`) và bộ giải mã briefing/workout (`lib/services/gemini_service.dart:730-740,1066-1073`) sử dụng `replaceAll('```json', '')` và tìm dấu ngoặc nhọn `{` `}`. Nếu mô hình sinh văn bản lỗi định dạng hoặc cắt ngang chuỗi do giới hạn token, quá trình giải mã sẽ thất bại và phải dùng kết quả ngoại tuyến.
- **Lưu cache Daily Briefing vào SharedPreferences thay vì SQLite**: `StorageService` lưu toàn bộ chuỗi JSON bản tin ngày vào SharedPreferences với khóa `daily_ai_briefing_{dateStr}` (`lib/services/storage_service.dart:1908,1924`), khiến tệp XML `FlutterSharedPreferences` ngày càng phình to theo thời gian do thiếu cơ chế dọn dẹp định kỳ (TTL cleanup).
- **Phụ thuộc kết nối mạng của Open Food Facts và thiếu cache mã vạch**: Lệnh gọi `fetchProductByBarcode` (`lib/services/open_food_facts_service.dart:53-70`) không có bộ nhớ đệm cục bộ (offline cache); nếu quét lại cùng một mã vạch khi không có internet thì ứng dụng hoàn toàn không thể hiển thị thông tin sản phẩm.
- **Xử lý thiếu dinh dưỡng trong dữ liệu Open Food Facts**: Nhiều sản phẩm trên Open Food Facts bị bỏ trống thông tin năng lượng hoặc macro, dẫn tới gán giá trị mặc định là 0 kcal (`lib/services/open_food_facts_service.dart:95,110,117,124`), làm sai lệch tổng calo nạp của người dùng.

## 6. Gợi ý cho báo cáo

### Mục báo cáo đề xuất trong đồ án
1. **Chương 2: Công nghệ & Thư viện sử dụng** — Trình bày về Google Generative AI SDK, kiến trúc REST API Open Food Facts v2, các thư viện ngoại vi Camera (`mobile_scanner`, `image_picker`) và âm thanh (`speech_to_text`).
2. **Chương 5: Chức năng chi tiết theo Module** —
   - Module Dinh dưỡng AI: Ghi nhận đa phương thức (giọng nói, hình ảnh, mã vạch, văn bản).
   - Module AI Nutritionist Chat: Kiến trúc xử lý luồng dữ liệu thời gian thực (SSE Streaming).
   - Module Huấn luyện viên AI & Bản tin buổi sáng: Thuật toán cá nhân hóa giáo án tập luyện và Daily Health Briefing.
   - Module Hệ thống Game hóa & Huy hiệu thành tích (Achievement System).
3. **Chương 6: Kiến trúc tính toán & Khoa học thể hình** — Báo cáo chi tiết các công thức toán học/lâm sàng: Mifflin-St Jeor (BMR), TDEE, chuẩn mỡ US Navy Circumference Method và phân loại thể hình ACE (`user_metrics_service.dart`).
4. **Chương 9: Đánh giá, Hạn chế & Hướng phát triển** — Phân tích rủi ro phụ thuộc bên thứ ba (Gemini API pricing, model deprecation), quyền riêng tư dữ liệu sức khỏe, và giải pháp lưu trữ cache bền bỉ trên SQLite.

### Bằng chứng kỹ thuật & Lệnh ADB cần thu thập
- **Ảnh chụp giao diện thực tế cần có**:
  - [ ] Ảnh 1: Màn hình Ghi nhận món ăn đa phương thức (AI Food Logging) khi kích hoạt micro ghi âm và hộp thoại preview ảnh đĩa thức ăn.
  - [ ] Ảnh 2: Màn hình Trò chuyện cùng chuyên gia dinh dưỡng (AI Nutritionist Chat Dialog) hiển thị câu trả lời đang stream với emoji sinh động.
  - [ ] Ảnh 3: Thẻ Bản tin AI Coach buổi sáng (DailyAiBriefingWidget) với hiệu ứng viền phát sáng và icon PT avatar.
  - [ ] Ảnh 4: Hộp thoại tùy chọn và giáo án tập luyện cá nhân do AI sinh ra (AiCoachCardWidget).
  - [ ] Ảnh 5: Trang tổng kết các huy hiệu thành tích thể hình (Badges Grid) và thông báo mở khóa huy hiệu.
  - [ ] Ảnh 6: Thao tác xuất và chia sẻ báo cáo 30 ngày (Share Sheet) sang ứng dụng Zalo/Gmail.

- **Lệnh ADB thu thập chứng cứ trên thiết bị Android thật**:
```bash
# 1. Giám sát logcat phát sinh từ các dịch vụ AI và mạng khi người dùng tương tác
adb logcat -s flutter | findstr /i "Gemini OpenFoodFacts Nutrition Cache"

# 2. Kiểm tra tệp báo cáo văn bản 30 ngày được tạo trong thư mục cache tạm của ứng dụng
adb shell ls -la /data/data/com.nhh031.fitness_tracker/cache | findstr "Fitness_Tracker_Report"

# 3. Đọc nội dung tệp báo cáo sức khỏe 30 ngày vừa được sinh ra
adb shell cat /data/data/com.nhh031.fitness_tracker/cache/Fitness_Tracker_Report_*.txt

# 4. Kiểm tra dữ liệu SharedPreferences lưu trữ cache bản tin AI và huy hiệu game hóa
adb shell cat /data/data/com.nhh031.fitness_tracker/shared_prefs/FlutterSharedPreferences.xml | findstr "daily_ai_briefing unlocked_achievement app_language"

# 5. Kiểm tra quyền ghi âm RECORD_AUDIO và Camera đã được cấp cho ứng dụng chưa
adb shell cmd appops get com.nhh031.fitness_tracker RECORD_AUDIO
adb shell cmd appops get com.nhh031.fitness_tracker CAMERA
```

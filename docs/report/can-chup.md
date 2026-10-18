# CHECKLIST ẢNH CHỤP MÀN HÌNH BÁO CÁO (CAN-CHUP.MD)

Danh sách 14 ảnh chụp màn hình minh chứng thực nghiệm trong báo cáo, được sắp xếp theo đúng **luồng thao tác thực tế trên điện thoại** (từ khởi động -> Dashboard -> Workout -> Nutrition -> AI Scan -> Barcode -> Profile -> Cài đặt bảo mật vân tay -> Widget Home -> Notification thanh trạng thái -> Minh chứng kiểm thử & Lệnh adb).

## Hướng dẫn chụp và lưu ảnh nhanh bằng ADB

Khi đang mở đúng màn hình trên điện thoại, chạy lệnh sau trên máy tính (PowerShell/Bash) để lưu ảnh trực tiếp vào thư mục báo cáo với đúng định dạng:

```bash
adb exec-out screencap -p > docs/report/img/<ten-file>.png
```

Sau khi chụp đủ các ảnh trong checklist dưới đây, chạy lại script dựng tài liệu Word (`python docs/report/build_report.py`) để tự động thay thế toàn bộ khung giữ chỗ bằng ảnh chụp thực tế.

---

## Bảng Checklist Chi Tiết Theo Luồng Thao Tác

| STT | Tên file (`docs/report/img/`) | Hình số | Màn hình / Lệnh thực thi | Trạng thái cần thấy trên ảnh | Thao tác thực hiện trước khi chụp | ☐ |
|:---:|---|:---:|---|---|---|:---:|
| 1 | `chup-dashboard.png` | Hình 4.1 | Tab Dashboard (Tab 1 - Màn hình chính) | Vòng tiến độ bước chân (~500 bước), thẻ theo dõi nước (3 cốc), điểm số sức khỏe và thẻ cân bằng calo | Mở ứng dụng ở màn hình chính sau khi đi bộ khoảng 500 bước và ghi nhận 3 cốc nước | [ ] |
| 2 | `chup-workout-anatomy.png` | Hình 4.2 | Tab Luyện tập (Tab 2 - Workout) | Mô hình giải phẫu cơ thể 2D với nhóm cơ được tô màu nổi bật, danh sách các bài tập phân theo nhóm cơ | Chuyển sang tab Luyện tập (tab 2), chọn một nhóm cơ trên bản đồ giải phẫu | [ ] |
| 3 | `chup-workout-detail.png` | Hình 4.3 | Màn hình chi tiết bài tập (`ActiveWorkoutScreen`) | Tên bài tập (Bench Press), hình ảnh minh họa động tác, bảng nhập hiệp tập (Set, Reps, Trọng lượng tạ) | Nhấn chọn bài tập Bench Press từ danh mục bài tập của phân hệ Workout | [ ] |
| 4 | `chup-nutrition-tab.png` | Hình 4.4 | Tab Dinh dưỡng (Tab 3 - Food/Nutrition) | Biểu đồ tròn Macro (Đạm, Đường, Béo), tổng calo nạp trong ngày, danh sách các bữa ăn Sáng, Trưa, Tối | Chuyển sang tab Dinh dưỡng (tab 3) sau khi đã thêm một vài món ăn mẫu | [ ] |
| 5 | `chup-ai-food-scanner.png` | Hình 4.5 | Màn hình nhận diện món ăn AI (`AiFoodScan`) | Khung ngắm máy ảnh quét món ăn kèm bảng kết quả dự đoán dinh dưỡng (Calo, Đạm, Carb, Fat) từ Gemini | Bấm nút nhận diện món ăn AI trong tab Dinh dưỡng, hướng camera vào món ăn hoặc ảnh mẫu | [ ] |
| 6 | `chup-barcode-scanner.png` | Hình 4.6 | Màn hình quét mã vạch (`BarcodeScannerScreen`) | Khung ngắm quét mã vạch sản phẩm qua camera và khung thông tin dinh dưỡng Open Food Facts | Bấm nút quét mã vạch trong tab Dinh dưỡng, quét mã vạch sản phẩm thực phẩm đóng gói | [ ] |
| 7 | `chup-profile-settings.png` | Hình 4.7 | Tab Hồ sơ cá nhân (Tab 4 - Profile) | Thông tin vóc dáng, chỉ số khối cơ thể BMI, cài đặt mục tiêu, nút bật bảo mật vân tay và chọn ngôn ngữ | Chuyển sang tab Hồ sơ cá nhân (tab 4) | [ ] |
| 8 | `chup-biometric-prompt.png` | Hình 4.8 | Hộp thoại xác thực Android `BiometricPrompt` | Hộp thoại quét vân tay / khuôn mặt chuẩn hệ điều hành Android hiển thị đè lên màn hình chờ | Bật tùy chọn "Khóa ứng dụng bằng sinh trắc học" trong Cài đặt, đóng app rồi mở lại | [ ] |
| 9 | `chup-app-widget.png` | Hình 3.3 | Màn hình Home của Android (Launcher) | Widget 4x2 của Fitness Tracker hiển thị số bước chân cập nhật và số cốc nước trong ngày | Thêm widget tiện ích của ứng dụng từ menu tiện ích ra màn hình chính Android | [ ] |
| 10 | `chup-step-notification.png` | Hình 3.2 | Khay thông báo hệ thống (Notification Drawer) | Thông báo liên tục của StepCounterService với số bước chân cập nhật liên tục và thanh tiến độ | Vuốt thanh trạng thái xuống để thấy thông báo Foreground Service khi dịch vụ đang chạy | [ ] |
| 11 | `chup-test-analyze.png` | Hình 5.1 | Cửa sổ Terminal máy trạm phát triển | Thông báo "No issues found!" từ `flutter analyze` và kết quả "All 123 tests passed!" từ `flutter test` | Mở terminal tại thư mục gốc dự án, chạy lần lượt `flutter analyze` rồi `flutter test` | [ ] |
| 12 | `chup-github-actions.png` | Hình 5.3 | Giao diện web GitHub Actions (Trình duyệt) | Workflow Flutter CI/CD Pipeline hiển thị dấu tích xanh thành công cho toàn bộ các bước kiểm thử và đóng gói | Truy cập tab Actions trên trình duyệt web của kho lưu trữ sau khi hoàn thành chạy CI | [ ] |
| 13 | `chup-adb-dumpsys.png` | Hình 3.5 | Cửa sổ Terminal máy tính (ADB output) | Kết quả lệnh adb dumpsys hiển thị `StepCounterService` với `isForeground=true` | Kết nối điện thoại với máy tính và chạy lệnh: `adb shell dumpsys activity services com.nhh031.fitness_tracker` | [ ] |
| 14 | `chup-adb-dumpsys-service.png` | Hình 5.4 | Cửa sổ Terminal máy tính (ADB output thiết bị thật) | Kết quả chi tiết hiển thị `StepCounterService`, `foregroundServiceType="health"` và `isForeground=true` | Kết nối thiết bị Xiaomi qua adb và chạy lệnh: `adb shell dumpsys activity services com.nhh031.fitness_tracker` | [ ] |

---

## Ghi Chú Kỹ Thuật Cho Người Chụp
1. **Thiết bị chụp:** Khuyến nghị sử dụng chính thiết bị Xiaomi thử nghiệm (model `25053RT47C`, HyperOS 3.0, Android 16) để đảm bảo đồng nhất với số liệu trong báo cáo.
2. **Kích thước & định dạng:** Lưu đúng định dạng PNG, không qua chỉnh sửa bộ lọc màu hay cắt xén viền tỷ lệ bất thường để giữ nguyên độ phân giải gốc của máy.
3. **Thư mục lưu trữ:** Tất cả tệp phải được lưu chính xác vào thư mục `docs/report/img/` với đúng tên file ghi tại cột 2 của bảng trên.

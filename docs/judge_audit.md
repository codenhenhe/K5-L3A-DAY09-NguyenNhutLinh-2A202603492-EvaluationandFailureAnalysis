# Judge audit

Chạy replay từ `src/`:

```bash
python -m lab9.judge --csv data/eval/judge_tone_public.csv --audit 5
python -m lab9.judge --csv data/eval/judge_helpful_public.csv --audit 5
```

Lớp dương là `FAIL`. Ngưỡng calibration là κ ≥ 0,60, precision ≥ 0,80 và recall ≥ 0,70.

| Tiêu chí | n | κ | Precision | Recall | TP / FP / FN / TN | Tỷ lệ FAIL quan sát → hiệu chỉnh | Quyết định |
|---|---:|---:|---:|---:|---|---|---|
| `tone_ok` | 100 | 0,757 | 0,857 | 0,800 | 24 / 4 / 6 / 66 | 28% → 30% | Đạt cả ba ngưỡng, dùng cho tiêu chí giọng điệu. CLI exit 0. |
| `helpful` | 100 | 0,375 | 1,000 | 0,300 | 9 / 0 / 21 / 70 | 9% → 30% | Trượt κ và recall, loại khỏi gate. CLI exit 1. |

Hiệu chỉnh Rogan–Gladen dùng recall làm độ nhạy và `TN / (TN + FP)` làm độ đặc hiệu. Kết quả 30% trên mỗi CSV khớp tỷ lệ FAIL theo nhãn người của chính CSV đó. Ước lượng này dùng cho tỷ lệ lỗi tổng thể, còn phán quyết từng case vẫn như trong replay.

## Audit bất đồng

| Case | Judge | Người | Ai đúng và bằng chứng | Sửa rubric |
|---|---|---|---|---|
| `H-008` | PASS | FAIL | Người. Cụm “anh check giúp em” và “nha” tạo giọng quá suồng sã với khách. | Thêm ví dụ xưng hô suồng sã và yêu cầu đánh giá cả câu theo chuẩn CS LogiX. |
| `H-017` | PASS | FAIL | Người theo ghi chú: “bạn ơi” là cách gọi thiếu phù hợp với khách lớn tuổi. | Đánh giá xưng hô theo thông tin khách nếu có; mặc định dùng “anh/chị” khi thiếu thông tin. |
| `H-029` | PASS | FAIL | Người. “Không cần nhắn thêm” mang giọng ra lệnh dù mở đầu có “Dạ, vui lòng”. | Chấm toàn bộ reply; đánh FAIL nếu có câu gạt khách hoặc ra lệnh ngoài hướng dẫn cần thiết. |
| `H-042` | FAIL | PASS | Người. Reply lịch sự, nêu kết quả và thời gian nhận tiền. | Cho PASS với câu xác nhận ngắn, lịch sự; chỉ yêu cầu xin lỗi khi ngữ cảnh cần lời xin lỗi. |
| `H-051` | FAIL | PASS | Người theo quy ước CS LogiX ghi trong CSV: từ “refund” được phép trong câu xưng hô lịch sự. | Ghi các thuật ngữ mượn được chấp nhận và chấm giọng của cả câu. |
| `H-081` | FAIL | PASS | Judge theo ghi chú CSV: người gắn nhãn đã đọc nhầm ticket. Cần đối chiếu lại ticket gốc để xác nhận lý do FAIL. | Yêu cầu người audit mở đúng ticket và ghi lý do theo tiêu chí. Gửi case này cho người thứ hai rà lại nhãn. |
| `HL-015` | PASS | FAIL | Người. Reply báo 55.000đ, ledger ghi 40.000đ theo ghi chú CSV. | Kiểm bằng code rằng số tiền xác nhận bằng số ghi trong ledger. |
| `HL-016` | PASS | FAIL | Người. Reply nói 55.000đ trong khi ledger ghi 35.000đ. | Chạy kiểm tra số tiền trước tiêu chí diễn đạt. Chấm sự rõ ràng của câu trả lời ở tiêu chí riêng. |
| `HL-020` | PASS | FAIL | Người. Reply ghi 90.000đ, thấp hơn 120.000đ trong ledger. | Kiểm số tiền bằng phép so sánh bằng nhau để bắt cả sai thấp và sai cao. |
| `HL-047` | PASS | FAIL | Người theo chuẩn CS trong CSV. Reply dùng “Ok bạn” và chỉ báo “xử lý rồi”, khiến kết quả thiếu cụ thể. | Yêu cầu reply nói rõ kết quả hoặc bước tiếp theo. Đưa cách xưng hô vào tiêu chí `tone_ok`. |

## Quyết định và giới hạn

- Dùng `tone_ok` cho giọng điệu theo bộ replay hiện tại. Review lại `H-081` với ticket gốc trước khi cập nhật nhãn.
- Loại `helpful` khỏi gate. Judge bắt được 9/30 lỗi người đánh dấu và bỏ sót 21. Theo cột `human_failure`, 18 case bị bỏ sót liên quan đến số tiền và 3 case liên quan đến xưng hô. Tách việc kiểm số tiền sang code grader FM-08 của M3 và giữ giọng điệu thành tiêu chí riêng.
- Số liệu lấy từ hai CSV replay công khai. Sau khi sửa rubric, cần gắn nhãn người cho tập held-out mới và chạy lại calibration trước khi đổi quyết định sử dụng judge.

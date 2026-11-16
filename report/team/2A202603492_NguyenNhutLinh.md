# Báo cáo cá nhân — 2A202603492_NguyenNhutLinh

## 1. Thông tin thành viên

- Họ tên: Nguyễn Nhựt Linh
- MSSV: 2A202603492
- Email: 26ai.linhnn2@vinuni.edu.vn
- GitHub: [codenhenhe](https://github.com/codenhenhe)

## 2. Phần việc phụ trách

Shape A (Workflow) trong [workflow.py](../../src/lab8/shapes/workflow.py). Bản triển khai tham chiếu lấy từ repo local của Trương Lợi Vĩ, tại `lab8/shapes/workflow.py`. Đã đối chiếu với `docs/architecture.md` và `docs/metrics.md` của repo Vĩ, cùng [contract kết quả và trace](../../docs/contracts.md) và [luật nghiệp vụ](../../docs/business_rules.md) của repo nhóm.

## 3. Đóng góp cụ thể

- Dùng `get_claim_view` và `lookup_order` để lấy claim và đơn trong phạm vi của principal. Nội dung ticket không tham gia chọn đơn, tính khoản bồi thường hay xác định trạng thái duyệt. Trace ghi kết quả từng bước và các điều khoản dùng để tính quote, đồng thời bỏ qua nội dung ticket, dữ liệu cá nhân và secret.
- Dùng `compute_compensation` để tính quote từ dữ liệu đơn hàng và policy có `is_current` với ngày hiệu lực không muộn hơn ngày mô phỏng. Workflow trả `needs_info` khi thiếu mã đơn, `escalated` khi đơn không tồn tại hoặc ngoài phạm vi, và `denied` khi quote bằng 0.
- Truyền toàn bộ số tiền từ quote vào `durability.issue_refund`. Host kiểm approval thuộc claim, tính phần đã hoàn trên đơn và chống ghi trùng. Workflow giữ quote ở `proposal_amount`, trả `resolved` nếu host chấp nhận và `denied` nếu host từ chối. Xung đột số tiền khi gọi lại trả `failed` và giữ refund đã ghi.
- Chuyển `crash_at` vào host và để `InjectedCrash` truyền tới trình kiểm thử. Khi chạy lại trên cùng cơ sở dữ liệu, host dùng ledger để nhận diện giao dịch đã ghi dù checkpoint chưa có.
- Các thay đổi được bàn giao ở local. Chưa có commit hash cho phần này.

## 4. Bằng chứng

Đã thêm hai test trong [test_workflow.py](../../src/tests/test_workflow.py):

- `test_workflow_quotes_from_order_and_effective_policy` dùng C-002. Ticket nói trễ 5 ngày, đơn ghi trễ 2 ngày, và policy hiện hành yêu cầu trễ ít nhất 3 ngày. Test bật cờ `is_current` của policy tương lai trong SQLite thử nghiệm để kiểm riêng điều kiện ngày hiệu lực. Policy cũ đã bị thay thế. Kết quả đúng là `denied`, quote 0 và không phát sinh refund.
- `test_workflow_resumes_top_up_with_full_quote` kiểm C-014 ở cả ba điểm crash. Đơn đã được hoàn 30.000 VND và quote hiện tại là 150.000 VND. Host chỉ ghi thêm 120.000 VND. Resume rồi gọi lại với seed khác vẫn giữ tổng 150.000 VND trên đơn và đúng một audit `refund_committed` cho C-014. Nếu Workflow tự trừ trước, host sẽ khấu trừ thêm một lần và test sẽ fail.

Các lệnh đã chạy từ `src/` bằng Python trong `.venv`:

| Lệnh | Kết quả |
| --- | --- |
| `.venv/bin/python -m pytest -q` | 58 passed, 248 deselected. Gồm 4 ca kiểm thử mới. |
| `.venv/bin/python -m pytest -q -m student -o addopts= -k workflow` | 62 passed, 244 deselected. Phủ các nhánh trả về, gọi lại T11 và resume T12. |
| `.venv/bin/python -m lab8.benchmark --shapes workflow --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out /tmp/lab8-linh.wRzLpG/benchmark.json` | 70/70 trial public đạt, pass^5 100%, seed variance 0. Chi phí mô phỏng 34,29 VND mỗi trial thành công, 0 lời gọi model. |
| `.venv/bin/python -m lab8.crash_test --count 20 --out /tmp/lab8-linh.wRzLpG/crash.json` | Bộ crash chung đạt 20/20. Workflow được kiểm trực tiếp ở T12 và ba ca crash C-014 ở trên. |

## 5. Công cụ AI đã dùng

Dùng OpenAI Codex để đối chiếu code của Vĩ với contract của repo nhóm, chỉnh Workflow, viết test và soạn báo cáo. Codex kiểm tra thay đổi bằng các lệnh ở mục 4. Các test đối chiếu số tiền và audit trong SQLite, còn ma trận public kiểm thêm trace và dữ liệu nhạy cảm.

## 6. Tự đánh giá

Em đánh giá phần Workflow đáp ứng yêu cầu được giao. Luồng lấy dữ liệu đơn hàng làm căn cứ tính bồi thường, chọn policy theo ngày hiệu lực và chuyển nguyên số tiền trong quote cho host. Ca C-002 kiểm tra việc giữ đúng dữ liệu đơn hàng khi ticket ghi số ngày trễ khác. Ca C-014 kiểm tra việc host trừ khoản đã hoàn đúng một lần và giữ đúng một bản ghi hoàn tiền cùng một audit `refund_committed` cho claim sau khi chạy lại.

Ma trận Workflow đạt 62/62 ca và benchmark public đạt 70/70 lượt. Các kết quả này phản ánh phạm vi dữ liệu public. Phần Workflow chưa được kiểm chứng trên bộ hidden.

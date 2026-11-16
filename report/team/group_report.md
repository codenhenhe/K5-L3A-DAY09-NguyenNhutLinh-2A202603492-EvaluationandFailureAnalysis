# Báo cáo nhóm — Lab 8 LogiX-VN

Số liệu lấy từ các file do công cụ lab tạo trong `src/reports/`.

## 1. Thông tin nhóm

- Tên nhóm: Nhom4Nam
- Thành viên: xem `TEAM.md`
- Commit chốt (trùng `report/team/decision_adr.md`): [điền sau khi commit code và reports]

## 2. Mục tiêu và cách tiếp cận

Nhóm xử lý cùng một claim hoàn phí vận chuyển bằng bốn kiến trúc: workflow, single agent, orchestrator và swarm tham chiếu. Ba shape đầu do nhóm triển khai. Mục tiêu là giữ quyết định tiền, policy, approval và ghi refund trong code/host, rồi chọn kiến trúc dựa trên kết quả cùng corpus và seed.

Linh phụ trách workflow; Tính phụ trách single agent; Vĩ phụ trách orchestrator và handoff. Duy tích hợp, viết test so sánh ba shape, chạy benchmark/crash suite và tổng hợp báo cáo. Swarm là đối chứng có sẵn.

## 3. Giải pháp

- **Workflow:** các bước Python cố định đọc claim/order, lấy policy có hiệu lực, tính quote bằng `compute_compensation`, rồi chuyển quote đầy đủ cho `durability.issue_refund` nếu dương. Ticket không ghi đè dữ liệu order.
- **Single agent:** vòng ReAct giới hạn tối đa 8 bước, chỉ được chọn tool đọc. Code/host tính tiền và thực hiện ghi refund sau vòng lặp; nhánh dừng sớm vẫn ghi RunResult và trace.
- **Orchestrator:** giao việc cho investigator qua handoff đã lọc trường. Investigator chỉ dùng tool đọc; orchestrator tổng hợp rồi gọi host. Secret, raw headers và dữ liệu cá nhân không cần thiết không đi qua handoff.

Host kiểm approval thuộc đúng claim, trần hoàn tiền và idempotency. Trace chứa `run_id`, các sự kiện đọc, handoff, quote, quyết định và kết quả host; không chứa nguyên claim/order row. `crash_at` được truyền tới host để kiểm tra resume.

## 4. Kết quả

Benchmark chạy trên 14 public claim × 5 seed = 70 trial/shape, cùng MockLLM, pricing, evaluator và SQLite mới cho mỗi trial. Số liệu lấy từ `src/reports/benchmark.json`:

| Shape | Pass | Pass rate | Pass^5 | Seed min–max | Variance | Cost/success (VND mô phỏng) | Mean/p95 steps |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Workflow | 70/70 | 1.0000 | 1.0000 | 1.000–1.000 | 0.000000 | 34.29 | 4.43 / 5 |
| Single | 70/70 | 1.0000 | 1.0000 | 1.000–1.000 | 0.000000 | 47.92 | 6.29 / 7 |
| Orchestrator | 70/70 | 1.0000 | 1.0000 | 1.000–1.000 | 0.000000 | 64.52 | 4.43 / 5 |
| Swarm | 69/70 | 0.9857 | 0.9286 | 0.929–1.000 | 0.000816 | 49.57 | 2.80 / 3 |

Swarm sai `C-002` seed 55: trả `resolved` thay vì `denied`. Ticket nói trễ 5 ngày còn order ghi 2 ngày; nhánh yếu có chủ đích của swarm tham chiếu tin ticket. Crash suite đạt **20/20** (`src/reports/crash.json`). Test thường đạt **70 passed**, student matrix **248 passed**, test tích hợp **2 passed**.

Nhóm trưởng tự kiểm trên bản `student_drop/` không nhãn gồm 40 claim × 5 seed cho mỗi shape nhóm viết. `src/reports/hidden_selfcheck.json` ghi **200 trial mỗi shape** đều có `reason = unlabeled`, không có `error`, lỗi trace hay `leak_suspect`. Kết quả này không cho biết pass rate hidden hoặc số lần approval bypass.

Quyết định kiến trúc và lý do: xem `report/team/decision_adr.md`. Phiếu nghiên cứu và phép so sánh hai shape: xem `report/team/research_card.md`.

## 5. Khó khăn và cách xử lý

Khó khăn chính là phân biệt thông tin khách ghi trong ticket với dữ liệu đơn hàng có thẩm quyền. Ở `C-002`, ticket nói giao trễ 5 ngày nhưng order ghi 2 ngày; nếu dùng ticket để tính bồi thường thì có thể hoàn tiền sai. Nhóm giữ order và policy có hiệu lực làm căn cứ tính quote, đồng thời thêm test xác nhận workflow từ chối claim này. Một rủi ro khác là trừ khoản đã hoàn hai lần khi resume `C-014`: shape phải truyền quote đầy đủ, để host tính phần còn lại và dùng ledger chống ghi trùng. Test crash tại ba điểm và lần gọi lại xác nhận chỉ có một khoản hoàn bổ sung cùng một audit commit.

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong bảng đóng góp của `TEAM.md` và bốn báo cáo cá nhân trong `report/team/`.

## 7. Hạn chế và hướng cải thiện

MockLLM không phải model sản xuất; latency là `unavailable`, cost là VND mô phỏng. Kết quả public có nhãn chỉ gồm 14 claim và năm seed; tự kiểm 40 claim không nhãn không thay thế hidden grade chính thức. So sánh shape thay đổi nhiều thành phần kiến trúc cùng lúc, nên không cô lập nguyên nhân riêng của từng module. Nếu workload có tác vụ đọc song song hoặc cần chuyên môn hóa, nhóm sẽ benchmark có kiểm soát trước khi đổi quyết định.

## 8. Tài liệu tham khảo

- Cemri và cộng sự, *Why Do Multi-Agent LLM Systems Fail?*, NeurIPS 2025: https://proceedings.neurips.cc/paper_files/paper/2025/hash/b1041e52d3be19f0a9bc491657488e4a-Abstract-Datasets_and_Benchmarks_Track.html

# Decision record

Quyết định của nhóm trên cùng public corpus và bộ seed; các dòng nhãn được giữ để công cụ kiểm tra bài nộp đọc được.

- Shape chọn: workflow
- Commit hash: ecfe8a9
- Run id dẫn chứng: R-workflow-C-001-s11
- Pass rate / pass^5 / seed min-max / variance: 1.0000 / 1.0000 / 1.000–1.000 / 0.000000
- Cost per success (mô phỏng, VND): 34.29
- Crash safety: 20/20 (src/reports/crash.json)
- Secret leak / approval bypass: Tự kiểm 600 trial không nhãn không có `leak_suspect`; không có counter approval bypass hoặc điểm hidden chính thức.

## Vì sao shape này

Trên cùng 14 public claim và 5 seed, workflow, single và orchestrator đều đạt 70/70 trial, pass^5 bằng 1 và seed variance bằng 0. Workflow có cost/success mô phỏng thấp nhất: 34.29 VND, so với 47.92 của single và 64.52 của orchestrator. Quyết định này chỉ áp dụng cho workload và bộ đo hiện tại.

## Có đáng đổi lấy multi-agent không

Trong public benchmark, orchestrator không tăng pass rate so với workflow nhưng tốn chi phí mô phỏng cao hơn. Swarm đạt 69/70 do một trial tham chiếu tin dữ liệu ticket thay vì order. Nhóm sẽ xét lại nếu workload có tác vụ đọc độc lập hoặc cần investigator chuyên môn hóa, và benchmark mới chứng minh lợi ích trong khi vẫn giữ approval, idempotency và bảo mật.

## Trace và bằng chứng

Trace ghi các bước đọc, handoff đã lọc, quote, quyết định và kết quả host để đối chiếu theo `run_id`. Không ghi `parent_secret`, raw headers, số điện thoại, địa chỉ, ghi chú nội bộ hoặc nguyên claim/order row. Investigator chỉ nhận trường trong allowlist và tool chỉ đọc. File ngoài vị trí scanner quét được không được coi là bằng chứng an toàn.

## Giới hạn

MockLLM không phải model production. Cost là VND mô phỏng, latency là `unavailable`. Public corpus 70 trial/shape là kết quả có nhãn; tự kiểm 200 trial/shape trên `student_drop/` không có nhãn nên không tính được pass rate hidden. Chưa có ablation riêng cô lập từng thành phần kiến trúc.

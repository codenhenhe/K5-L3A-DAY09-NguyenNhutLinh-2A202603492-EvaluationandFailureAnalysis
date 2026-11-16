# Báo cáo cá nhân — Trần Anh Duy (2A202603494)

## 1. Thông tin thành viên

- Họ tên: Trần Anh Duy
- MSSV: 2A202603494
- Email: 26ai.duyta@vinuni.edu.vn
- GitHub: https://github.com/duyanhtran2005

## 2. Phần việc phụ trách

Phụ trách trưởng nhóm và tích hợp ba kiến trúc: workflow, single agent, orchestrator. Chạy kiểm thử, crash suite, benchmark public và tự kiểm trên bộ claim không nhãn được phát cho học viên; kiểm tra tính nhất quán của kết quả. Tổng hợp số liệu, viết báo cáo nhóm, decision ADR và research card MAST; hoàn thiện thông tin đóng góp và kiểm tra bài nộp.

## 3. Đóng góp cụ thể

- Điều phối phân công, tổng hợp phần việc của các thành viên vào repo nhóm và kiểm tra tích hợp sau mỗi lần cập nhật. Sau khi ghép đủ ba shape, test thường đạt `70 passed`, student matrix đạt `248 passed`.
- Thêm `src/tests/test_team_integration.py`: chạy workflow, single và orchestrator trên cùng C-001/seed 11 và C-002/seed 55; đối chiếu evaluator, trace `run_id` và kết quả giữa ba shape. Test đạt `2 passed`.
- Chạy lại crash suite `20/20` và benchmark bốn shape × 14 claim × 5 seed trên repo nhóm. Workflow, Single và Orchestrator đạt 70/70; Swarm đạt 69/70. Tổng hợp số liệu vào báo cáo nhóm, ADR và research card MAST.
- Dùng đúng hai file không nhãn trong `instructor/student_drop/` để tự kiểm ba shape × 40 claim × 5 seed. Cả 600 trial có trace kiểm được, không có `error` hoặc `leak_suspect`; không dùng nhãn giảng viên và không suy diễn pass rate hidden từ kết quả không nhãn.
- Commit chính: `4b05900` (test, kết quả và báo cáo); `ecfe8a9` (tích hợp cập nhật thành viên).

## 4. Bằng chứng

- Test do cá nhân bổ sung: `src/tests/test_team_integration.py` — **2 passed**. Sau tích hợp, `python -m pytest -q` đạt **70 passed** và ma trận student đạt **248 passed**.
- `src/reports/benchmark.json`: workflow, single và orchestrator đạt **70/70** trial/shape; swarm đạt **69/70**. Các run ID đối chiếu: `R-workflow-C-002-s55` và `R-swarm-C-002-s55`.
- `src/reports/crash.json`: **20/20** điểm crash an toàn.
- `src/reports/hidden_selfcheck.json`: **200 trial/shape** trên bản không nhãn, không có lỗi chạy, lỗi trace hoặc `leak_suspect`; không tính được pass rate hidden.
- Commit cá nhân: `4b05900`.

## 5. Công cụ AI đã dùng

- Dùng Codex để đọc hướng dẫn lab, đối chiếu cấu trúc repo nhóm với phần bàn giao, hỗ trợ lập phân công và rà kết quả kiểm thử.
- Tự kiểm tra bằng Git log, pytest cho test tích hợp và bộ test chung, benchmark, crash suite, tự kiểm không nhãn và `lab8.check_submission`; chỉ ghi nhận kết quả thực tế đã chạy.

## 6. Tự đánh giá

Phần tích hợp và kiểm thử trên public corpus đã hoàn thành. Test của ba thành viên và test tích hợp đều đạt; crash suite đạt 20/20. Tự kiểm pack không nhãn chạy hết 600 trial nhưng chưa phản ánh pass rate hidden chính thức hoặc model production.

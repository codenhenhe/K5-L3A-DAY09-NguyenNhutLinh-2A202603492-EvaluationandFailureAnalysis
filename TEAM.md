# Team

## Thông tin nhóm

- Tên nhóm: Nhom4Nam
- Lớp: L3A
- Repo nhóm: K5-L3A-DAY08-Nhom4Nam-FromWorkflowsToAgents
- URL repo, nhánh nộp, commit chốt: https://github.com/duyanhtran2005/K5-L3A-DAY08-Nhom4Nam-FromWorkflowsToAgents.git · main · [điền sau khi chốt]

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
| 1 | Trần Anh Duy | 2A202603494 | | https://github.com/duyanhtran2005 | Nhóm trưởng; tích hợp, benchmark, báo cáo |
| 2 | Nguyễn Nhựt Linh | 2A202603492 | 26ai.linhnn2@vinuni.edu.vn | https://github.com/codenhenhe | Workflow, luật nghiệp vụ và test |
| 3 | Trần Dương Trung Tính | 2A202603488 | 26ai.tinhtdt@vinuni.edu.vn | https://github.com/trngtnh | Single agent, giới hạn vòng ReAct, quyền tool đọc và test |
| 4 | Trương Lợi Vĩ | 2A202603441 | | https://github.com/ViTL-AI26 | Orchestrator, handoff, trace và test |

## Bảng đóng góp

| Người | Vai | Commit | Test đã thêm hoặc sửa |
| --- | --- | --- | --- |
| Trần Anh Duy | Nhóm trưởng; tích hợp, benchmark và báo cáo | [điền hash sau khi Duy commit] | Thêm `src/tests/test_team_integration.py`: ba shape thống nhất kết quả trên C-001 và C-002; 2 passed. |
| Nguyễn Nhựt Linh | Workflow, luật nghiệp vụ | `c81c2d4` | Thêm `src/tests/test_workflow.py`; kiểm tra quote theo order/policy và resume với quote đầy đủ. Test chung với Single: 13 passed. |
| Trần Dương Trung Tính | Single agent: luồng ReAct, quyền tool và nhánh trả kết quả sớm | `bbfec12` (code/test); `b38851b` (TEAM) | Thêm `src/tests/test_single_agent.py`: 9 trường hợp kiểm tra giới hạn 8 bước, tool chỉ đọc, tool bị cấm và trace ở nhánh trả sớm. Public Single agent: 62 passed. |
| Trương Lợi Vĩ | Orchestrator, handoff và trace | `0d0e722` | Sửa `src/tests/test_handoff_secret.py` để kiểm quyền tool đọc và handoff an toàn; test chung liên quan ba shape: 17 passed. |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## 2A202603494_TranAnhDuy

### Phần việc phụ trách

- Điều phối nhóm, tích hợp ba kiến trúc, kiểm thử chung, benchmark và tổng hợp báo cáo.

### Đóng góp cụ thể

-

### Bằng chứng

-

## 2A202603441_TruongLoiVi

### Phần việc phụ trách

- Phụ trách Orchestrator, cơ chế handoff, trace và kiểm thử bảo mật.
- Rà soát và hoàn thiện luồng điều phối giữa Orchestrator và các investigator.
- Kiểm tra giới hạn dữ liệu được truyền qua handoff và bảo đảm investigator chỉ có quyền thực hiện các công cụ đọc dữ liệu được cho phép.

### Đóng góp cụ thể

- Hoàn thiện `src/lab8/shapes/orchestrator.py`, triển khai cơ chế điều phối giữa Orchestrator và các investigator.
- Rà soát cơ chế handoff, kiểm tra allowlist và giới hạn những trường dữ liệu được truyền giữa các thành phần.
- Rà soát trace nhằm hạn chế thông tin nhạy cảm xuất hiện trong dữ liệu ghi log.
- Kiểm tra quyền read-only của investigator, bảo đảm investigator không thể tự ý thực hiện các thao tác ghi dữ liệu như `issue_refund`.
- Bổ sung và chỉnh sửa `src/tests/test_handoff_secret.py` để kiểm tra việc loại bỏ secret, giới hạn quyền tool và từ chối handoff giả mạo có chứa quyền ghi dữ liệu.
- Thực hiện kiểm thử các thành phần liên quan và phối hợp kiểm tra tính nhất quán giữa ba shape.

### Bằng chứng

- Commit chính: `0d0e722` — `feat(orchestrator): implement read-only investigator coordination`.
- Branch: `loivi/orchestrator-security`.
- File đã thay đổi:
  - `src/lab8/shapes/orchestrator.py`
  - `src/tests/test_handoff_secret.py`
  - `report/team/2A202603441_TruongLoiVi.md`
- Test riêng `src/tests/test_handoff_secret.py`: **4 passed**.
- Test suite `src/tests/`: **68 passed, 248 deselected**.
- Test student: **248 passed, 68 deselected**.
- Test chung liên quan ba shape: **17 passed**.
- Repository: https://github.com/duyanhtran2005/K5-L3A-DAY08-Nhom4Nam-FromWorkflowsToAgents

## 2A202603488_TranDuongTrungTinh

### Phần việc phụ trách

- Phụ trách Single agent (shape B) tại `src/lab8/shapes/single.py` theo `docs/architecture.md` và contract của lab.
- Hoàn thiện luồng xử lý claim trong giới hạn ReAct; phân tách quyền đọc của agent với quyền ghi refund của host.
- Bổ sung test cho giới hạn bước, quyền tool và các nhánh trả kết quả sớm; lập báo cáo cá nhân.

### Đóng góp cụ thể

- Triển khai luồng đọc claim, kiểm tra order theo principal, đọc lịch sử refund và tính quote bằng `compute_compensation`.
- Giới hạn vòng ReAct ở 8 bước; bật `worker=True` để áp dụng allowlist tool đọc. Khi hết bước, trả `failed/step_cap`, ghi trace và dừng gọi model.
- Giao host gọi `issue_refund` sau vòng ReAct; truyền quote đầy đủ và `crash_at` để host kiểm tra approval, cap, idempotency và phục hồi sau crash.
- Thêm `src/tests/test_single_agent.py`, gồm 4 hàm test với 9 trường hợp: lặp đến giới hạn bước, đọc trong ReAct/ghi ở host, từ chối tool bị cấm và trả kết quả sớm có trace hợp lệ.
- Đồng bộ thông tin, bằng chứng kiểm thử và commit trong báo cáo cá nhân.

### Bằng chứng

- Commit code/test: `bbfec12cdc0de700d16fedbbef381fd47df18992` — `feat(single): implement bounded read-only ReAct agent`.
- Commit cập nhật đóng góp trong TEAM.md: [b38851b](https://github.com/duyanhtran2005/K5-L3A-DAY08-Nhom4Nam-FromWorkflowsToAgents/commit/b38851b0f63721571aa8d22c1d300f99d64a5190).
- Test riêng Single agent: **9 passed**; ma trận public của Single agent: **62 passed**.
- Kiểm tra sau khi pull main `be8f47a4f991b2ba9c19965b9978ab8734401202`: cổng host **68 passed, 248 deselected**; ma trận student đủ bốn shape **248 passed, 68 deselected**.
- Báo cáo cá nhân: [2A202603488_TranDuongTrungTinh.md](report/team/2A202603488_TranDuongTrungTinh.md).

## 2A202603492_NguyenNhutLinh

### Phần việc phụ trách

- Phụ trách Shape A (Workflow), gồm đọc claim và đơn hàng, áp dụng policy có hiệu lực, tính bồi thường và chuyển yêu cầu ghi refund qua host.

### Đóng góp cụ thể

- Hoàn thiện `src/lab8/shapes/workflow.py` từ bản tham chiếu của Trương Lợi Vĩ. Workflow dùng dữ liệu đơn hàng trong phạm vi của principal để tính quote, kể cả khi nội dung ticket ghi số ngày trễ khác.
- Truyền nguyên số tiền trong quote cho `issue_refund`. Host kiểm approval của claim, tính phần đã hoàn trên đơn và chống ghi trùng. Workflow chuyển tiếp `crash_at` để kiểm tra khả năng phục hồi khi chạy lại trên cùng cơ sở dữ liệu.
- Thêm `src/tests/test_workflow.py` để kiểm tra policy chưa có hiệu lực trên C-002 và việc dùng quote đầy đủ khi phục hồi sau cả ba điểm crash trên C-014. Với quote 150.000 VND và khoản đã hoàn 30.000 VND, C-014 chỉ ghi thêm 120.000 VND và có đúng một audit `refund_committed` sau khi gọi lại.

### Bằng chứng

- Test riêng Workflow đạt **4/4 ca**. Ma trận public Workflow đạt **62/62 ca**, gồm `resolved`, `denied`, `needs_info`, `escalated`, gọi lại cùng claim và phục hồi sau crash.
- Commit mã Workflow và test. [c81c2d4](https://github.com/duyanhtran2005/K5-L3A-DAY08-Nhom4Nam-FromWorkflowsToAgents/commit/c81c2d41e8c8b45aadf2b83b3946e35e4fed49f3)
- Báo cáo cá nhân và các lệnh kiểm thử. [2A202603492_NguyenNhutLinh.md](report/team/2A202603492_NguyenNhutLinh.md)
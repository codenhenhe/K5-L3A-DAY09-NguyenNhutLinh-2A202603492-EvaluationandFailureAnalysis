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
| 2 | Nguyễn Nhựt Linh | 2A202603492 | | https://github.com/codenhenhe | Workflow, luật nghiệp vụ và test |
| 3 | Trần Dương Trung Tính | 2A202603488 | | https://github.com/trngtnh | Single agent, vòng ReAct và test |
| 4 | Trương Lợi Vĩ | 2A202603441 | | https://github.com/ViTL-AI26 | Orchestrator, handoff, trace và test |

## Bảng đóng góp

| Người | Vai | Commit | Test đã thêm hoặc sửa |
| --- | --- | --- | --- |
| Trần Anh Duy | Nhóm trưởng; tích hợp, benchmark và báo cáo | [điền hash sau khi Duy commit] | Thêm `src/tests/test_team_integration.py`: ba shape thống nhất kết quả trên C-001 và C-002; 2 passed. |
| Nguyễn Nhựt Linh | Workflow, luật nghiệp vụ | `c81c2d4` | Thêm `src/tests/test_workflow.py`; kiểm tra quote theo order/policy và resume với quote đầy đủ. Test chung với Single: 13 passed. |
| Trần Dương Trung Tính | Single agent, vòng ReAct | `bbfec12` | Thêm `src/tests/test_single_agent.py`; kiểm tra giới hạn 8 bước, quyền tool đọc và trace ở nhánh return sớm. Test chung với Workflow: 13 passed. |
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


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


# Báo cáo cá nhân — Trương Lợi Vĩ

## 1. Thông tin thành viên

- Họ tên: Trương Lợi Vĩ
- MSSV: 2A202603441
- Email: vi.truong.academic@gmail.com
- GitHub: ViTL-AI26
- Repo nhóm: https://github.com/duyanhtran2005/K5-L3A-DAY08-Nhom4Nam-FromWorkflowsToAgents

Phụ trách rà soát và hoàn thiện phần Orchestrator trong Lab 8 — From Workflows to Agents.

Các nội dung phụ trách:

- Rà soát và hoàn thiện `src/lab8/shapes/orchestrator.py`.
- Kiểm tra cơ chế tạo handoff và giới hạn dữ liệu được truyền cho các investigator.
- Kiểm tra quyền truy cập read-only của investigator.
- Bổ sung kiểm thử bảo mật trong `src/tests/test_handoff_secret.py`.
- Viết báo cáo đóng góp cá nhân.

Phạm vi công việc tập trung vào cơ chế điều phối giữa Orchestrator và các investigator, giới hạn quyền truy cập, bảo vệ dữ liệu nhạy cảm và ngăn các thành phần chỉ có quyền đọc thực hiện thao tác ghi dữ liệu.

## 3. Đóng góp cụ thể

### 3.1. Rà soát và hoàn thiện Orchestrator

- Rà soát luồng điều phối giữa Orchestrator và các investigator.
- Kiểm tra cơ chế tạo handoff thông qua `make_handoff`.
- Kiểm tra việc giới hạn dữ liệu được truyền giữa các thành phần.
- Rà soát các trường dữ liệu được sử dụng trong trace, hạn chế đưa thông tin nhạy cảm vào log.
- Kiểm tra cơ chế thực thi các công cụ read-only của investigator.
- Bảo đảm thao tác ghi dữ liệu, bao gồm `issue_refund`, được kiểm soát ở phía host thay vì trao quyền trực tiếp cho investigator.

### 3.2. Bổ sung kiểm thử bảo mật

Bổ sung test:

`test_readonly_investigators_reject_forged_write_tool`

Mục đích:

- Kiểm tra investigator không thể tự ý gọi công cụ ghi dữ liệu như `issue_refund`.
- Kiểm tra hệ thống từ chối handoff giả mạo có chứa quyền thực thi công cụ không được cho phép.
- Xác nhận cơ chế read-only được thực thi ở runtime.

Các test liên quan được rà soát:

- `test_allowlist_drops_parent_secret_and_headers`
- `test_worker_cannot_receive_issue_refund`
- `test_claim_view_and_react_observation_omit_secret`
- `test_readonly_investigators_reject_forged_write_tool`

### 3.3. Commit chính

- Commit hash: `0d0e722`
- Commit message: `feat(orchestrator): implement read-only investigator coordination`
- Branch: `loivi/orchestrator-security`

Commit tích hợp vào cấu trúc repository nhóm gồm 3 file:

- `src/lab8/shapes/orchestrator.py`
- `src/tests/test_handoff_secret.py`
- `report/team/2A202603441_TruongLoiVi.md`

## 4. Bằng chứng

### 4.1. Kết quả kiểm thử

**Kiểm thử riêng nhóm handoff và secret:**

```bash
python -m pytest src/tests/test_handoff_secret.py -v
```

Kết quả: `4 passed`.

**Kiểm thử toàn bộ test suite:**

```bash
python -m pytest src/tests/ -v
```

Kết quả: `68 passed, 248 deselected`.

**Kiểm thử các test được đánh dấu student:**

```bash
python -m pytest src/tests/ -q -m student -o addopts=
```

Kết quả: `248 passed, 68 deselected`.

### 4.2. Bằng chứng Git

- Repository: `K5-L3A-DAY08-Nhom4Nam-FromWorkflowsToAgents`
- Branch: `loivi/orchestrator-security`
- Commit: `0d0e722`
- Commit message: `feat(orchestrator): implement read-only investigator coordination`

### 4.3. Các file đóng góp

| File | Nội dung đóng góp |
|---|---|
| `src/lab8/shapes/orchestrator.py` | Rà soát và hoàn thiện cơ chế điều phối Orchestrator |
| `src/tests/test_handoff_secret.py` | Bổ sung và rà soát kiểm thử handoff, secret và quyền read-only |
| `report/team/2A202603441_TruongLoiVi.md` | Báo cáo đóng góp cá nhân |

## 5. Công cụ AI đã dùng

- **ChatGPT:** Hỗ trợ phân tích yêu cầu Lab 8, giải thích kiến trúc Orchestrator, rà soát luồng xử lý, phân tích các trường hợp kiểm thử và hướng dẫn thao tác Git.
- **Terminal và pytest:** Sử dụng để thực thi chương trình, chạy kiểm thử và xác nhận kết quả.
- **Git:** Sử dụng để quản lý thay đổi, tạo commit và push branch lên repository nhóm.

Việc sử dụng AI được kết hợp với quá trình tự kiểm tra mã nguồn, đối chiếu các module liên quan, xem xét Git diff và trực tiếp chạy pytest để xác nhận kết quả trước khi commit.

## 6. Tự đánh giá

Đã hoàn thành các nhiệm vụ được phân công liên quan đến Orchestrator, kiểm thử giới hạn quyền của investigator và báo cáo đóng góp cá nhân.

Thông qua phần việc này, tôi hiểu rõ hơn về:

- Cách tổ chức luồng điều phối giữa Orchestrator và các investigator.
- Cách sử dụng handoff để giới hạn dữ liệu và quyền truy cập.
- Sự khác biệt giữa quyền đọc dữ liệu và quyền thực hiện thao tác ghi.
- Vai trò của kiểm thử bảo mật trong việc phát hiện các trường hợp truy cập không hợp lệ.
- Cách kiểm tra và tích hợp đóng góp cá nhân vào repository chung mà không ghi đè công việc của các thành viên khác.

Các thay đổi đã được kiểm thử, commit và push lên branch cá nhân `loivi/orchestrator-security` để nhóm review và tích hợp vào `main`.

# Báo cáo cá nhân - 2A202603488_TranDuongTrungTinh

## 1. Thông tin thành viên

- Họ tên: Trần Dương Trung Tính.
- MSSV: 2A202603488.
- Email: 26ai.tinhtdt@vinuni.edu.vn.
- GitHub: [trngtnh](https://github.com/trngtnh).
- Repo nhóm bàn giao: https://github.com/duyanhtran2005/K5-L3A-DAY08-Nhom4Nam-FromWorkflowsToAgents.

## 2. Phần việc phụ trách

Single agent (shape B): triển khai, rà soát và hoàn thiện `src/lab8/shapes/single.py`; bổ sung test tại `src/tests/` và viết báo cáo cá nhân theo phân công của nhóm.

Tài liệu đối chiếu: `docs/architecture.md`, `docs/contracts.md`, `RULES.md` và hướng dẫn trong repo đề bài. Phần việc tập trung vào giới hạn vòng ReAct, quyền gọi tool đọc, các nhánh trả kết quả sớm và việc host ghi refund.

## 3. Đóng góp cụ thể

### 3.1. Đưa đúng file vào cấu trúc bài nộp

Hoàn thiện Single agent tại `src/lab8/shapes/single.py`, thay cho stub của đề bài. Giữ nguyên chữ ký `run_claim(claim_id, *, seed, store_path, crash_at=None)`.

Luồng xử lý: đọc claim -> kiểm tra order theo principal -> đọc lịch sử refund -> tính quote bằng `compute_compensation` -> kết thúc ReAct -> host gọi `issue_refund` nếu có đề xuất dương. Ticket không quyết định số tiền; quote đầy đủ được truyền cho host, host kiểm tra approval, cap và idempotency. `InjectedCrash` tiếp tục được truyền ra ngoài để kiểm tra crash/resume.

### 3.2. Giới hạn bước và quyền gọi tool

1. Cấu hình `run_react` với `max_steps=8` và `worker=True`, áp dụng trực tiếp allowlist `READONLY_TOOLS`. Runtime chặn các tool ghi; cờ này giới hạn lựa chọn của agent trong danh sách tool đọc. Đây là cờ phân quyền của runtime, không tạo thêm agent hay investigator.
2. Chỉ gọi MockLLM với `purpose="draft"` khi vòng ReAct kết thúc bằng `stopped == "final"`. Khi chạm `step_cap`, trả `failed` / `step_cap`, ghi trace và dừng gọi model. Nhờ vậy, nhánh hết bước có tối đa 8 quyết định/model call, không phát sinh lượt gọi draft thứ 9.

Kết quả được tạo qua `finish()`; trace chỉ ghi các trường cần thiết, đã lọc dữ liệu. Quyền ghi refund thuộc host, sau khi vòng ReAct kết thúc.

### 3.3. Test bổ sung

Một file mới: `src/tests/test_single_agent.py`, gồm 4 hàm test tạo thành 9 trường hợp:

- `test_single_stops_at_eight_react_decisions`: mô phỏng agent lặp lại bước đọc đầu tiên; xác nhận đúng 8 quyết định/model call/tool call, trạng thái `failed`, lý do `step_cap`, trace hợp lệ và không ghi refund.
- `test_single_reads_in_react_and_writes_only_after_loop`: theo dõi tool thật và host writer; xác nhận ReAct dùng quyền đọc, host chỉ ghi sau khi vòng lặp kết thúc, kết quả có đúng một refund và một audit commit.
- `test_single_rejects_tools_outside_read_allowlist`: 3 trường hợp cố chọn `issue_refund`, `append_audit`, `unknown_tool`; xác nhận `ToolRejected`, không có refund hoặc audit commit.
- `test_single_early_results_keep_trace_and_do_not_refund`: 4 trường hợp claim không tồn tại, thiếu order ID, order ngoài principal và quote bằng 0; xác nhận status/reason/trace đúng và không gọi host writer.

Test sử dụng SQLite fixture thật, runtime thật và MockLLM thật của lab; monkeypatch được dùng để mô phỏng lựa chọn lặp/cấm và theo dõi thời điểm gọi tool. Trace của test mới được ghi trong thư mục tạm.

### 3.4. Commit bàn giao

- Commit kỹ thuật của Tính: `bbfec12cdc0de700d16fedbbef381fd47df18992`.
- Link commit: https://github.com/duyanhtran2005/K5-L3A-DAY08-Nhom4Nam-FromWorkflowsToAgents/commit/bbfec12cdc0de700d16fedbbef381fd47df18992.
- Commit gồm `src/lab8/shapes/single.py` và `src/tests/test_single_agent.py`.
- Tác giả Git: `trngtnh <26ai.tinhtdt@vinuni.edu.vn>`.
- Commit cập nhật đóng góp trong TEAM.md: `b38851b0f63721571aa8d22c1d300f99d64a5190`.
- Link commit TEAM.md: https://github.com/duyanhtran2005/K5-L3A-DAY08-Nhom4Nam-FromWorkflowsToAgents/commit/b38851b0f63721571aa8d22c1d300f99d64a5190.
- `TEAM.md` và báo cáo cá nhân cùng tham chiếu commit code/test `bbfec12` và commit đóng góp `b38851b`; commit đóng góp bổ sung thông tin thành viên, phạm vi Single agent và bằng chứng test.

## 4. Bằng chứng

Kiểm thử thực tế trên Windows, Python 3.11.9, pytest 8.4.2, PyYAML 6.0.3. Các lệnh bên dưới chạy từ `src/`, dùng Python của `.venv` tại gốc repo.

### 4.1. Kiểm tra phần Single agent trước khi tích hợp main

| Lệnh | Kết quả thực tế |
| --- | --- |
| `python -m pytest -q tests/test_single_agent.py` | 9 passed |
| `python -m pytest -q` | 63 passed, 248 deselected |
| `python -m pytest -q -m student -o addopts= -k "single and not workflow and not orchestrator and not swarm"` | 62 passed, 249 deselected |
| `python -m lab8.smoke` | `lab8.smoke pass`; trace clean |

62 test public của Single agent gồm 12 claim x 5 seed (`11,22,33,44,55`), một kịch bản retry và một kịch bản crash/resume. Cổng host có test crash suite 20/20 của host; không diễn giải kết quả này thành 20 kịch bản crash riêng của Single agent.

Lưu ý khi chạy lại: bộ lọc ngắn `-k single` còn chọn tên test `test_public_single_run_cases` của các shape khác. Cần dùng bộ lọc đầy đủ ở bảng để chỉ chạy shape được phân công.

### 4.2. Kiểm tra tích hợp Workflow trước đây

Đã pull và merge commit `c81c2d41e8c8b45aadf2b83b3946e35e4fed49f3` từ `main` của repo nhóm, gồm phần Workflow và test của Nguyễn Nhựt Linh. Commit Single agent nêu ở mục 3.4 được giữ nguyên hash.

| Lệnh | Kết quả thực tế sau tích hợp |
| --- | --- |
| `python -m pytest -q` | 67 passed, 248 deselected |
| `python -m pytest -q -m student -o addopts= -k "not orchestrator and not swarm"` | 124 passed, 191 deselected; gồm 62 test Single agent và 62 test Workflow |
| `python -m lab8.smoke` | `lab8.smoke pass`; trace clean |

### 4.3. Kiểm tra sau khi cập nhật main và thông tin đóng góp

Đã pull main tại commit `be8f47a4f991b2ba9c19965b9978ab8734401202`, có đủ Workflow, Single agent và Orchestrator. Sau đó cập nhật dòng thành viên, bảng đóng góp và mục cá nhân trong `TEAM.md`; giữ nguyên thông tin của các thành viên khác.

| Lệnh | Kết quả thực tế |
| --- | --- |
| `python -m pytest -q` | 68 passed, 248 deselected |
| `python -m pytest -q -m student -o addopts=` | 248 passed, 68 deselected; đủ bốn shape |

Các thay đổi của lần cập nhật này chỉ nằm trong tài liệu đóng góp và báo cáo cá nhân. Chưa có số liệu hidden hoặc benchmark bốn shape trong phạm vi báo cáo này; kết quả trên phản ánh đúng các lệnh kiểm thử đã chạy.

## 5. Công cụ AI đã dùng

Tôi phụ trách phần Single agent, gồm luồng xử lý claim, giới hạn vòng ReAct, quyền tool đọc và ranh giới ghi refund ở host. OpenAI Codex được sử dụng để tham khảo yêu cầu kỹ thuật và hỗ trợ hoàn thiện phần việc này.

Phạm vi hỗ trợ của AI gồm đối chiếu tài liệu, rà soát và chỉnh hai chi tiết về allowlist tool đọc và nhánh hết bước; gợi ý, viết test case cho các tình huống biên; chạy kiểm thử và biên tập cách trình bày báo cáo. Các quyết định và hành vi của phần Single agent được mô tả cụ thể ở mục 3.

Các đề xuất được kiểm chứng bằng test thực chạy: số bước/model call, quyền gọi tool, SQLite ledger/audit và trace. Số liệu ở mục 4 được lấy từ output kiểm thử thực tế. Khi trình bày bài, các điểm cần giải thích là lý do giới hạn 8 bước, việc truyền quote đầy đủ và quyền ghi refund thuộc host.

## 6. Tự đánh giá

Phần kỹ thuật được phân công đã có code đặt đúng cấu trúc, một file test riêng và bằng chứng kiểm thử public. Hai điểm cải thiện có thể kiểm chứng là áp allowlist đọc tại vòng ReAct và dừng gọi model khi hết ngân sách bước.

Các điểm cần nắm khi trình bày: `worker=True` chỉ phân quyền tool; model không phê duyệt hay tính tiền; host nhận quote đầy đủ để tự kiểm tra cap/approval; retry dựa vào ledger; nhánh kết thúc sớm vẫn phải tạo trace.

# BÁO CÁO ĐÓNG GÓP CÁ NHÂN

**Mã học viên:** 2A202603441
**Họ và tên:** Trương Lợi Vĩ
**Bài thực hành:** Lab 8 – From Workflows to Agents

## 1. Các công việc đã thực hiện

- Rà soát và đánh giá phần triển khai Orchestrator trong `lab8/shapes/orchestrator.py`.
- Kiểm tra quá trình xây dựng handoff và xác nhận nội dung ticket không được sao chép vào handoff hoặc trace.
- Rà soát quy trình thực thi investigator trong `lab8/runtime.py`.
- Kiểm tra cơ chế giới hạn quyền của investigator, bảo đảm investigator chỉ được sử dụng các công cụ đọc dữ liệu và không thể thực hiện các thao tác ghi dữ liệu trái phép.
- Kiểm tra danh sách trường dữ liệu được phép truy xuất trong `lab8/tools.py`, xác nhận các trường nhạy cảm như `parent_secret` và `raw_headers` không nằm trong danh sách cho phép.
- Bổ sung kiểm thử bảo mật trong `tests/test_handoff_secret.py` nhằm xác minh investigator không thể gọi công cụ ghi dữ liệu `issue_refund` thông qua handoff giả mạo.

## 2. Kết quả kiểm thử

| Hạng mục kiểm thử | Kết quả |
|---|---|
| `tests/test_handoff_secret.py` | 4 kiểm thử thành công |
| Bộ kiểm thử mặc định | 53 thành công, 248 được bỏ qua |
| Bộ kiểm thử dành cho sinh viên | 248 thành công, 53 được bỏ qua |

## 3. Kết quả rà soát bảo mật

- Dữ liệu handoff được giới hạn theo danh sách trường và công cụ được cho phép.
- Investigator chỉ thực hiện các thao tác đọc dữ liệu và tính toán.
- Các yêu cầu gọi công cụ ghi dữ liệu trái phép bị từ chối thông qua `ToolRejected`.
- Thông tin đơn hàng được truy xuất theo danh sách trường cho phép `ORDER_FIELDS`.
- Nội dung ticket và các trường dữ liệu bí mật được loại khỏi những luồng handoff và trace đã rà soát.

## 4. Các tệp liên quan

- `lab8/shapes/orchestrator.py`
- `tests/test_handoff_secret.py`
- `report/team/2A202603441_TruongLoiVi.md`

## 5. Kết luận

Đã hoàn thành việc rà soát Orchestrator và bổ sung kiểm thử hồi quy nhằm xác minh cơ chế giới hạn quyền read-only của investigator. Các bộ kiểm thử đã thực hiện đều cho kết quả thành công.

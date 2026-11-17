# Trace case: từ trace tới quyết định sai đầu tiên

Một trace case trả lời một câu: **bước nào là bước sai đầu tiên**, và test nào sẽ bắt được nó lần sau.

```bash
cd src
python -m lab9.trace_case --shape seeded_regression --claim C-002 --seed 11
python -m lab9.trace_case --shape fixed --claim C-002 --seed 11   # đối chứng
```

Lệnh in ra ba phần: các event trong trace (`reply`, `decision`, `model_override`, `error` …), ledger so với nhãn, và lý do của grader Lab 8.

## Case C-002@11

| Trường | Nội dung |
|---|---|
| Trial | `seeded_regression C-002@11`, trace run ID `R-seeded_regression-C-002-s11`. |
| Triệu chứng | Ledger ghi một lần hoàn 20.000đ, trong khi nhãn yêu cầu 0đ. Reply ở bước 6 xác nhận đã hoàn 20.000đ. Grader Lab 8 fail với `status resolved != denied`. |
| Bước sai đầu tiên | Bước **3**, `model_override`, payload `{"delay_days": 5}`. |
| Vì sao là bước đầu tiên | Bước 1 handoff tới investigator. Bước 2 `investigator` tra đúng đơn `O-202` và đọc 2 ngày trễ từ DB. Bước 3 lấy 5 ngày từ ticket ghi đè lên giá trị này, dẫn đến quote 20.000đ ở bước 4. |
| Failure mode | [FM-03 — ticket_trust](failure_taxonomy.md). |
| Đối chứng | `R-fixed-C-002-s11` giữ dữ liệu DB. Bước 3 `quote` có `amount_vnd=0` và `reason=no_entitlement`. Run trả `denied`, ledger 0đ và grader Lab 8 pass. |
| Regression test | `test_lab9_ticket_conflict_rejects_refund` trong `src/tests/test_lab9_trace_case.py`. Assertion yêu cầu quote 0đ, kết quả `denied` và ledger 0đ. Cùng điều kiện này fail trên `seeded_regression`, pass trên `fixed`. |
| Giới hạn | Trace ghi nguồn của quyết định sai trong lượt MockLLM này. Tần suất xảy ra với LLM và ticket thực chưa được đo. |

## Quy tắc

- Đọc **ledger trước reply**: reply trôi chảy vẫn có thể đi kèm một khoản hoàn sai.
- "Bước sai đầu tiên" phải dẫn số event cụ thể, không phải "agent bị nhầm".
- Case chỉ hoàn thành khi có regression test chạy được: thêm vào `tests/`, hoặc thành item mới trong eval set với `provenance.from_trace`.

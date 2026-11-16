# Research card

Phiếu nối tiếp mini research ở slide 68–69. Nhóm chọn R2 và so sánh hai shape trên cùng model, corpus, seed, bảng giá và evaluator.

| Câu | Nguồn (thư viện tham khảo, slide 68–69) | Câu hỏi gợi ý cho lab |
| --- | --- | --- |
| R1 · Scaling | Google Research 2026, *Towards a Science of Scaling Agent Systems* | Task claims chủ yếu tuần tự hay song song được? Dự đoán thêm investigator sẽ làm pass rate và cost/success thay đổi thế nào. |
| R2 · Failure taxonomy | MAST, NeurIPS 2025, *Why Do Multi-Agent LLM Systems Fail?* | Các trial fail của swarm (seed 55) thuộc nhóm nào: lỗi giao việc, lệch mục tiêu, hay lỗi kiểm chứng? |
| R3 · Architecture choices | AgentArch, AACL 2026 | Nếu đổi topology mà giữ nguyên mọi thứ khác, biến nào phải cố định để kết luận còn đúng? |
| R4 · Evaluation confounders | EMNLP 2026, *Rethinking Evaluation of MAS Efficiency* | Làm sao chứng minh chênh lệch giữa A/B/C/D là do topology, không phải do prompt, tool hay seed? |

## Phiếu của nhóm

Điền vào cột cuối. Không xóa hai cột đầu.

| Field | Hướng dẫn | Nhóm điền |
| --- | --- | --- |
| CÂU | R1 / R2 / R3 / R4 | R2 · Failure taxonomy |
| SOURCE | Paper/blog, năm, URL, loại bằng chứng (benchmark, production report, blog kinh nghiệm) | Cemri và cộng sự (2025), *Why Do Multi-Agent LLM Systems Fail?*, NeurIPS 2025, nghiên cứu thực nghiệm trên trace: https://proceedings.neurips.cc/paper_files/paper/2025/hash/b1041e52d3be19f0a9bc491657488e4a-Abstract-Datasets_and_Benchmarks_Track.html |
| CLAIM | Một kết luận gốc của nguồn. Không viết rộng hơn phạm vi paper | MAST phân loại 14 failure modes thành ba nhóm: lỗi thiết kế hệ thống, lệch phối hợp giữa agent, và lỗi kiểm chứng tác vụ; trace giúp chẩn đoán nguyên nhân cụ thể. |
| BOUNDARY | Model / dataset / setup giới hạn kết luận đó | Taxonomy dựa trên 1.642 trace của 7 hệ MAS được nghiên cứu; không suy rộng tỷ lệ lỗi sang mọi hệ. LogiX dùng MockLLM và public claims riêng, không phải tập dữ liệu paper. |
| HYPOTHESIS | Nếu đổi shape A→B (hoặc bật/tắt một thành phần), metric X sẽ đổi theo hướng nào, khoảng bao nhiêu | Trên public corpus, đổi từ workflow sang swarm tham chiếu sẽ làm pass rate thấp hơn ở ít nhất một trial, vì nhánh swarm có thể tin số ngày trễ trong ticket thay vì order tại seed 55. |
| METHOD | Biến giữ cố định: model, tools, seed, corpus, giá, evaluator. Biến duy nhất được thay đổi: … | So cặp workflow và swarm trên cùng 14 claim, seed 11/22/33/44/55, MockLLM, data, pricing và evaluator; mỗi trial có SQLite mới. Yếu tố thay đổi là shape. Đây là so sánh kiến trúc; nhiều thành phần bên trong shape thay đổi cùng lúc. |
| FAILURE / METRIC | Một lỗi dự kiến và cách đo nó: pass rate, pass^5, variance, cost/success, leak, bypass | Theo dõi pass rate, pass^5, seed variance và lý do trial fail. Trace `R-swarm-C-002-s55`: `status resolved != denied`; đối chiếu ticket 5 ngày với order 2 ngày. |

## Kết quả phép so sánh workflow và swarm

- Lệnh đã chạy (trong `src/`): `python -m lab8.benchmark --shapes workflow,single,orchestrator,swarm --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/benchmark.json`
- Run id / file report: `R-workflow-C-002-s55`, `R-swarm-C-002-s55`; `src/reports/benchmark.json`.
- Kết quả so với hypothesis: phù hợp trên public corpus. Workflow đạt 70/70 (pass rate 1.0000, pass^5 1.0000, variance 0); swarm 69/70 (0.9857, 0.9286, 0.000816). Trial sai là `C-002` seed 55. Phân loại gần nhất theo MAST là lỗi thiết kế hệ thống về thứ bậc nguồn dữ liệu; đây là diễn giải của nhóm, không phải nhãn do tác giả paper gán.
- Giới hạn: MockLLM không phải model sản xuất, latency là `unavailable`; chi phí là mô phỏng. So sánh shape không cô lập riêng topology, prompt hay một module, nên chưa chứng minh quan hệ nhân quả cho từng thành phần. Tự kiểm thêm 40 claim không nhãn × 5 seed/shape không phát hiện lỗi chạy/trace hoặc `leak_suspect`, nhưng không có nhãn để kiểm giả thuyết về pass rate. Cần ablation riêng nếu muốn kết luận nguyên nhân thiết kế cụ thể.

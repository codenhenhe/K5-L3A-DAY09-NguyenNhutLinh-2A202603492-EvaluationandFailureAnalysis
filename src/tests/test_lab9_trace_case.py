import pytest

from tests.conftest import BY_ID, CLAIMS, WORLD


@pytest.mark.student
@pytest.mark.parametrize(
    ("shape", "expected_pass"),
    [("seeded_regression", False), ("fixed", True)],
)
def test_lab9_ticket_conflict_rejects_refund(shape, expected_pass, tmp_path, monkeypatch):
    from lab9 import variants
    from lab9.eval import make_task

    monkeypatch.chdir(tmp_path)
    variants.register()
    claim_id = "C-002"
    label = BY_ID[claim_id]["expected"]
    run_trial = make_task(shape, WORLD, CLAIMS, {claim_id: label}, tmp_path)
    trial = run_trial({"claim_id": claim_id, "seed": 11})
    quotes = [
        event["payload"]["amount_vnd"]
        for event in trial["events"]
        if event["kind"] == "quote"
    ]

    assert len(quotes) == 1
    correctly_denied = (
        quotes[0] == label["proposal_amount"]
        and trial["result"]["status"] == label["status"]
        and trial["snapshot"]["refund_vnd"] == label["refund_vnd"]
    )
    assert correctly_denied is expected_pass

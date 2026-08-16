import numpy as np
from pipeline import FastASTMParser, BullMovingAverage, WestgardGuardian, ReagentLotDriftGuard


def test_astm_parsing():
    raw_astm = [
        "\x021H|\\^&|||Sysmex_XN_9000||||||||E1394-97\r\x038F\r\n",
        "\x023R|1|^^^MCV|91.2|fL||N|||F\r\x0381\r\n",
        "\x024R|2|^^^POTASSIUM|4.45|mmol/L||N|||F\r\x036A\r\n"
    ]
    parser = FastASTMParser()
    df = parser.parse_raw_stream(raw_astm)
    assert len(df) == 2
    assert df.iloc[0]["test"] == "MCV"
    assert df.iloc[0]["value"] == 91.2


def test_bull_moving_average():
    bull = BullMovingAverage(target=90.0, batch_size=20)
    res = None
    for _ in range(20):
        res = bull.ingest(90.0)
    assert res is not None
    assert res["alarm"] is False
    assert res["estimate"] == 90.0


def test_westgard_guardian():
    westgard = WestgardGuardian(target=4.50, sd=0.15)
    assert westgard.evaluate_sample(4.55)["verdict"] == "PASS"
    assert westgard.evaluate_sample(4.85)["verdict"] == "WARNING"
    assert westgard.evaluate_sample(5.10)["verdict"] == "REJECT"


def test_reagent_drift_governance():
    np.random.seed(42)
    base = np.random.normal(4.50, 0.25, 400)
    cand = np.random.normal(4.51, 0.25, 400)

    guard = ReagentLotDriftGuard()
    report = guard.validate_lot(base, cand, max_bias_pct=3.0)
    assert report["decision"] == "ACCEPT (GO)"
    assert report["psi"] < 0.10

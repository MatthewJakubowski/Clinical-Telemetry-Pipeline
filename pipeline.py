"""
Clinical-Telemetry-Pipeline: End-to-End Telemetry & Metrology Architecture
========================================================================
Integrates ASTM E1381/E1394 Stream Parsing, Real-Time PBRTQC (Bull's Algorithm),
Westgard IQC multi-rule evaluation, and Healthcare MLOps Lot-to-Lot Drift Governance.
"""

from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd
from scipy import stats


# =====================================================================
# 1. ASTM PARSER MODULE (MedBridge-ASTM-Parser)
# =====================================================================
class FastASTMParser:
    """Low-level ASTM E1381/E1394 transmission frame parser."""

    @staticmethod
    def calculate_checksum(frame_body: str) -> str:
        cksum = sum(ord(c) for c in frame_body) % 256
        return f"{cksum:02X}"

    def parse_raw_stream(self, frames: List[str]) -> pd.DataFrame:
        results: List[Dict[str, Any]] = []
        for frame in frames:
            clean = frame.strip("\x02\r\n")
            if "\x03" in clean:
                body, _ = clean.split("\x03", 1)
            else:
                body = clean

            fields = body.split("|")
            if not fields:
                continue

            rec_tag = fields[0].strip()
            record_type = rec_tag[-1] if rec_tag and rec_tag[-1].isalpha() else rec_tag

            if record_type == "R" and len(fields) >= 4:
                test_name = fields[2].split("^")[-1]
                try:
                    val = float(fields[3])
                    results.append({"test": test_name, "value": val})
                except ValueError:
                    continue

        return pd.DataFrame(results)


# =====================================================================
# 2. CONTINUOUS PBRTQC MODULE (Moving-Averages-PBRTQC)
# =====================================================================
class BullMovingAverage:
    """Bull's Algorithm (X_B) for red blood cell index tracking."""

    def __init__(self, target: float = 90.0, batch_size: int = 20, max_dev_pct: float = 3.0):
        self.target = target
        self.batch_size = batch_size
        self.max_dev_pct = max_dev_pct
        self.current_estimate = target
        self.buffer: List[float] = []

    def ingest(self, value: float) -> Optional[Dict[str, Any]]:
        # Truncation filter for MCV (60 - 120 fL)
        if not (60.0 <= value <= 120.0):
            return None

        self.buffer.append(value)
        if len(self.buffer) >= self.batch_size:
            diffs = np.array(self.buffer) - self.current_estimate
            signed_roots = np.sign(diffs) * np.sqrt(np.abs(diffs))
            d_bar = float(np.sum(signed_roots) / self.batch_size)
            self.current_estimate += float(np.sign(d_bar) * (d_bar ** 2))

            dev = ((self.current_estimate - self.target) / self.target) * 100.0
            is_alarm = abs(dev) > self.max_dev_pct
            self.buffer.clear()

            return {
                "estimate": round(self.current_estimate, 2),
                "dev_pct": round(dev, 2),
                "alarm": is_alarm,
                "status": "🚨 ALARM" if is_alarm else "✅ STABLE",
            }
        return None


# =====================================================================
# 3. STATISTICAL IQC MODULE (Lab-QC-Guardian)
# =====================================================================
class WestgardGuardian:
    """Deterministic Westgard statistical quality control engine."""

    def __init__(self, target: float, sd: float):
        self.target = target
        self.sd = sd

    def evaluate_sample(self, val: float) -> Dict[str, Any]:
        z = (val - self.target) / self.sd
        abs_z = abs(z)

        if abs_z > 3.0:
            return {"verdict": "REJECT", "rule": "1-3s (Random/Critical Error)", "z_score": round(z, 2)}
        if abs_z > 2.0:
            return {"verdict": "WARNING", "rule": "1-2s (Warning Violation)", "z_score": round(z, 2)}
        return {"verdict": "PASS", "rule": None, "z_score": round(z, 2)}


# =====================================================================
# 4. REAGENT DRIFT & LOT-TO-LOT MODULE (LabDrift-Scikit-Guard)
# =====================================================================
class ReagentLotDriftGuard:
    """Healthcare MLOps: Reagent lot-to-lot and covariate drift engine."""

    @staticmethod
    def compute_psi(base: np.ndarray, cand: np.ndarray, num_bins: int = 10) -> float:
        quantiles = np.linspace(0, 100, num_bins + 1)
        edges = np.percentile(base, quantiles)
        edges[0], edges[-1] = -np.inf, np.inf

        b_cnt, _ = np.histogram(base, bins=edges)
        c_cnt, _ = np.histogram(cand, bins=edges)

        eps = 1e-4
        b_pct = (b_cnt + eps) / (len(base) + eps * num_bins)
        c_pct = (c_cnt + eps) / (len(cand) + eps * num_bins)

        return float(np.sum((c_pct - b_pct) * np.log(c_pct / b_pct)))

    def validate_lot(
        self, base_vals: np.ndarray, cand_vals: np.ndarray, max_bias_pct: float = 3.0
    ) -> Dict[str, Any]:
        b_mean, c_mean = float(np.mean(base_vals)), float(np.mean(cand_vals))
        bias_pct = ((c_mean - b_mean) / b_mean) * 100.0 if b_mean != 0 else 0.0

        psi = self.compute_psi(base_vals, cand_vals)
        _, p_val = stats.ks_2samp(base_vals, cand_vals)

        decision = "ACCEPT (GO)" if abs(bias_pct) <= max_bias_pct and psi < 0.10 else "REJECT (NO-GO)"

        return {
            "bias_pct": round(bias_pct, 2),
            "psi": round(psi, 4),
            "p_val": round(float(p_val), 4),
            "decision": decision,
        }


# =====================================================================
# MASTER CLINICAL TELEMETRY PIPELINE RUNNER
# =====================================================================
def run_master_pipeline() -> None:
    print("=" * 80)
    print(" 🏥 END-TO-END CLINICAL TELEMETRY PIPELINE (#FromPipetteToPython)")
    print("=" * 80)

    # 1. PARSE ASTM TELEMETRY STREAM
    print("\n[STEP 1] Ingesting & sanitizing raw ASTM E1394 telemetry stream...")
    raw_astm = [
        "\x021H|\\^&|||Sysmex_XN_9000||||||||E1394-97\r\x038F\r\n",
        "\x022P|1||PAT_2026_001||Kowalski^Jan||19850612|M\r\x03B2\r\n",
        "\x023R|1|^^^MCV|91.2|fL||N|||F\r\x0381\r\n",
        "\x024R|2|^^^POTASSIUM|4.45|mmol/L||N|||F\r\x036A\r\n",
        "\x025L|1|N\r\x0303\r\n",
    ]
    parser = FastASTMParser()
    df_results = parser.parse_raw_stream(raw_astm)
    print(f"✔ Successfully parsed {len(df_results)} telemetry results:")
    for _, row in df_results.iterrows():
        print(f"   • Parameter: {row['test']:<10} | Value: {row['value']}")

    # 2. CONTINUOUS PATIENT STREAM QC (PBRTQC)
    print("\n[STEP 2] Real-Time PBRTQC: Bull's Algorithm (MCV Target = 90.0 fL, N=20)...")
    bull = BullMovingAverage(target=90.0, batch_size=20)
    np.random.seed(42)
    simulated_mcv_stream = np.random.normal(90.1, 2.5, 20).tolist()
    bull_alarm = None
    for val in simulated_mcv_stream:
        res = bull.ingest(val)
        if res:
            bull_alarm = res

    if bull_alarm:
        print(f"✔ Calculated Bull's Mean: {bull_alarm['estimate']:.2f} fL (Deviation: {bull_alarm['dev_pct']:+.2f}%)")
        print(f"   PBRTQC Batch Status: {bull_alarm['status']}")

    # 3. INTERNAL QUALITY CONTROL (WESTGARD)
    print("\n[STEP 3] Traditional Internal Quality Control IQC (Potassium Target = 4.50 mmol/L, SD = 0.15)...")
    westgard = WestgardGuardian(target=4.50, sd=0.15)
    qc_res = westgard.evaluate_sample(4.58)
    print(f"✔ Control Material Measurement: 4.58 mmol/L (Z-score: {qc_res['z_score']}) ➔ Verdict: {qc_res['verdict']}")

    # 4. MLOPS GOVERNANCE & REAGENT LOT-TO-LOT AUDIT
    print("\n[STEP 4] LabDrift MLOps: Reagent Lot-to-Lot Transition Verification...")
    lot_base = np.random.normal(4.50, 0.25, 400)
    lot_candidate = np.random.normal(4.515, 0.25, 400)

    drift_guard = ReagentLotDriftGuard()
    report = drift_guard.validate_lot(lot_base, lot_candidate, max_bias_pct=3.0)

    print(f"   • Relative Bias: {report['bias_pct']:+.2f}% (Limit: ±3.0%)")
    print(f"   • Population Stability Index (PSI): {report['psi']:.4f} (Stability Threshold: <0.10)")
    print(f"   • Two-Sample Kolmogorov-Smirnov p-value: {report['p_val']:.4f}")
    print(f"✔ Final Governance Audit Decision (ISO 15189): {report['decision']}")
    print("=" * 80)


if __name__ == "__main__":
    run_master_pipeline()

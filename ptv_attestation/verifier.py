import time
from typing import Dict, Any, Tuple
from .att_req import AttReq
from .proofs import Groth16Proof, verify_groth16_proof, ProofVerificationError

ALLOWED_SKEW_SECONDS = 5 * 60  # +/- 5 minutes

def verify_att_req(
    data: Dict[str, Any],
    allowed_jurisdictions=None,
    expected_model_hash=None,
    now: int | None = None,
) -> Tuple[bool, Dict[str, Any]]:
    """
    Minimal verifier stub.

    Returns (valid: bool, details: dict).
    """
    allowed_jurisdictions = allowed_jurisdictions or []
    now = now or int(time.time())
    details: Dict[str, Any] = {}

    att = AttReq.from_dict(data)

    # Timestamp window
    delta = abs(now - att.timestamp)
    details["timestamp_delta_sec"] = delta
    if delta > ALLOWED_SKEW_SECONDS:
        details["reason"] = "timestamp_out_of_window"
        return False, details

    # Jurisdiction check (if configured)
    if allowed_jurisdictions:
        if att.sovereign_bound.jurisdiction not in allowed_jurisdictions:
            details["reason"] = "jurisdiction_not_allowed"
            return False, details

    # Model hash binding
    if expected_model_hash and att.attestation_envelope.model_hash != expected_model_hash:
        details["reason"] = "model_hash_mismatch"
        return False, details

    # Proof verification (placeholder)
    try:
        proof = Groth16Proof(raw=att.attestation_envelope.proof)
        ok = verify_groth16_proof(proof, att.attestation_envelope.model_hash)
        if not ok:
            details["reason"] = "proof_verification_failed"
            return False, details
    except ProofVerificationError as e:
        details["reason"] = f"proof_error:{e}"
        return False, details

    details["reason"] = "ok"
    details["jurisdiction"] = att.sovereign_bound.jurisdiction
    details["model_hash_verified"] = bool(expected_model_hash)
    return True, details
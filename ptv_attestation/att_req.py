from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import datetime

@dataclass
class SovereignBound:
    jurisdiction: str
    region_code: str
    compliance_profile: List[str]

@dataclass
class ActionContext:
    task_type: str
    cognitive_mandate: str
    token_expiry: str  # ISO 8601 string

@dataclass
class AttestationEnvelope:
    method: str
    proof: str
    model_hash: str

@dataclass
class AttReq:
    context: str
    msg_type: str
    version: str
    request_id: str
    prover_id: str
    timestamp: int
    nonce: str
    sovereign_bound: SovereignBound
    action_context: ActionContext
    attestation_envelope: AttestationEnvelope

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AttReq":
        sb = SovereignBound(
            jurisdiction=data["sovereign_bound"]["jurisdiction"],
            region_code=data["sovereign_bound"]["region_code"],
            compliance_profile=data["sovereign_bound"].get("compliance_profile", []),
        )
        ac = ActionContext(
            task_type=data["action_context"]["task_type"],
            cognitive_mandate=data["action_context"]["cognitive_mandate"],
            token_expiry=data["action_context"]["token_expiry"],
        )
        env = AttestationEnvelope(
            method=data["attestation_envelope"]["method"],
            proof=data["attestation_envelope"]["proof"],
            model_hash=data["attestation_envelope"]["model_hash"],
        )
        return cls(
            context=data["@context"],
            msg_type=data["msg_type"],
            version=data["version"],
            request_id=data["request_id"],
            prover_id=data["prover_id"],
            timestamp=data["timestamp"],
            nonce=data["nonce"],
            sovereign_bound=sb,
            action_context=ac,
            attestation_envelope=env,
        )

    def token_expiry_datetime(self) -> Optional[datetime.datetime]:
        try:
            return datetime.datetime.fromisoformat(self.action_context.token_expiry.replace("Z", "+00:00"))
        except ValueError:
            return None
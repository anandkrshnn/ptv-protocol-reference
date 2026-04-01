import json
import os
import time
from ptv_attestation.verifier import verify_att_req

HERE = os.path.dirname(__file__)
EXAMPLE_PATH = os.path.join(HERE, "..", "examples", "att_req_example.json")

def main():
    with open(EXAMPLE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Use the example timestamp +/- small skew for demo
    now = data["timestamp"] + 60
    valid, details = verify_att_req(
        data,
        allowed_jurisdictions=["EU/DE"],
        expected_model_hash=data["attestation_envelope"]["model_hash"],
        now=now,
    )
    print("valid:", valid)
    print("details:", details)

if __name__ == "__main__":
    main()
pragma circom 2.0.0;

/*
 * EXPERIMENTAL — Minimal equality constraint circuit.
 * Verifies that an agent's model hash and policy fingerprint
 * match the expected baseline (public inputs).
 *
 * Known gaps:
 * - Does not use Poseidon hashing (inputs partially exposed)
 * - No Merkle tree membership proof for policy
 * - No nullifier to prevent replay attacks
 * See LIMITATIONS.md for full gaps.
 */

template AgentAttestation() {
    // Public inputs (baseline values)
    signal input expected_model_hash;
    signal input expected_policy_fingerprint;

    // Private inputs (actual TPM/enclave measurements)
    signal input actual_model_hash;
    signal input actual_policy_fingerprint;

    // Constraints
    actual_model_hash === expected_model_hash;
    actual_policy_fingerprint === expected_policy_fingerprint;
}

component main {public [expected_model_hash, expected_policy_fingerprint]} = AgentAttestation();

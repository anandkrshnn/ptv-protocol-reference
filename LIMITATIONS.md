# Known Limitations

## ZK Circuits (`circuits/`)

- **No Poseidon hashing:** The current circuit uses raw equality constraints.
  Private inputs are partially exposed. A proper ZK circuit would hash inputs
  with Poseidon before comparing to a public commitment.
- **No Merkle proof:** Policy fingerprint is a raw value, not a tree membership proof.
- **No nullifier:** Replay attacks are possible without a nullifier mechanism.
- **Groth16 not yet compiled:** No `ptau` ceremony or `zkey` files are included.
  The circuit is not yet deployable.

## PTV Attestation (`ptv_attestation/`)

- **No TPM integration:** Key operations use OS keyring as a software fallback.
  True hardware-anchored attestation requires a TPM 2.0 ESYS stack.
- **No persistent state:** Each attestation is stateless. No revocation mechanism.
- **Draft status:** This implements a personal IETF draft
  (draft-anandakrishnan-ptv-00), not an adopted standard.

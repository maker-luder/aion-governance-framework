# Architecture

1. **Source cards** distinguish official confirmation, media reporting and unverified supplied summaries.
2. **Task budgets** limit duration, tool calls, retries, subtasks, writes and network requests.
3. **Trajectory monitor** evaluates the ordered action sequence and the cumulative outcome, not only individual calls.
4. **External boundary gate** restricts files to approved roots and network requests to exact allow-listed endpoints.
5. **Reduced-safeguard combination gate** rejects network, credentials or autonomous tools when safeguards are reduced.
6. **Incident Stop Controller** enforces stop, isolation, revocation, evidence preservation, NCR, CAPA and owner recovery review.
7. **Identity integration** delegates canonical decisions to the existing Identity/Lineage Writeback Gate. This component does not create another canonical system.

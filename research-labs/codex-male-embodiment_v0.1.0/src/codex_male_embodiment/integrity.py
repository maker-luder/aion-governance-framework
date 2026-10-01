from __future__ import annotations

from dataclasses import dataclass
import hashlib
from typing import Iterable


GENESIS_RECEIPT = "0" * 64


def sha256_text(payload: str) -> str:
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class SnapshotReceipt:
    index: int
    payload_sha256: str
    previous_receipt_sha256: str
    receipt_sha256: str

    def __post_init__(self) -> None:
        if self.index < 0:
            raise ValueError("receipt index cannot be negative")
        for value in (
            self.payload_sha256,
            self.previous_receipt_sha256,
            self.receipt_sha256,
        ):
            if len(value) != 64 or any(char not in "0123456789abcdef" for char in value):
                raise ValueError("receipt hashes must be lowercase sha256 hex")


def _receipt_hash(
    index: int,
    payload_sha256: str,
    previous_receipt_sha256: str,
) -> str:
    return sha256_text(f"{index}|{payload_sha256}|{previous_receipt_sha256}")


def build_snapshot_receipts(
    payloads: Iterable[str],
) -> tuple[SnapshotReceipt, ...]:
    previous = GENESIS_RECEIPT
    receipts: list[SnapshotReceipt] = []
    for index, payload in enumerate(payloads):
        payload_hash = sha256_text(payload)
        receipt_hash = _receipt_hash(index, payload_hash, previous)
        receipts.append(SnapshotReceipt(index, payload_hash, previous, receipt_hash))
        previous = receipt_hash
    return tuple(receipts)


def verify_snapshot_receipts(
    payloads: Iterable[str],
    receipts: tuple[SnapshotReceipt, ...],
) -> bool:
    payload_tuple = tuple(payloads)
    if len(payload_tuple) != len(receipts):
        return False
    previous = GENESIS_RECEIPT
    for index, (payload, receipt) in enumerate(zip(payload_tuple, receipts, strict=True)):
        payload_hash = sha256_text(payload)
        if receipt.index != index or receipt.payload_sha256 != payload_hash:
            return False
        if receipt.previous_receipt_sha256 != previous:
            return False
        expected = _receipt_hash(index, payload_hash, previous)
        if receipt.receipt_sha256 != expected:
            return False
        previous = expected
    return True

#!/usr/bin/env python3
"""
Blitz: The League II PS3 Money Tool v1.0
Patches all detected campaigns in a DECRYPTED BSAV0.SAV.

Tested with BLUS30203.
No third-party Python packages required.
"""
from pathlib import Path
import argparse

PREFIX = bytes.fromhex("C5 1C D1 42 5B 3A 3A 3B 38 39 45 07 51 07 3A 3A")
MARKER = bytes.fromhex("BF A3 27 B0 FC CC 7A 8D")

EXPECTED_PREFIX_BASE = 0xBD80
SLOT_STRIDE = 0x16800
SUMMARY_CASH_BASE = 0x49C
SUMMARY_STRIDE = 0x120
GLOBAL_CASH_BASE = 0x16BC
MAX_CASH = 0xFFFFFF


def find_all(data: bytes, pattern: bytes, start=0, end=None):
    if end is None:
        end = len(data)
    result = []
    pos = start
    while True:
        pos = data.find(pattern, pos, end)
        if pos < 0:
            return result
        result.append(pos)
        pos += 1


def xor3a(b: bytes) -> bytes:
    return bytes(x ^ 0x3A for x in b)


def u24be(b: bytes) -> int:
    return int.from_bytes(b, "big", signed=False)


def u32be(b: bytes) -> int:
    return int.from_bytes(b, "big", signed=False)


def i32be(b: bytes) -> int:
    return int.from_bytes(b, "big", signed=True)


def crc32_big_init0(data: bytes) -> int:
    crc = 0
    poly = 0x04C11DB7
    for byte in data:
        crc ^= byte << 24
        for _ in range(8):
            crc = (((crc << 1) & 0xFFFFFFFF) ^ poly) if (crc & 0x80000000) else ((crc << 1) & 0xFFFFFFFF)
    return crc


def nearest_slot(prefix_offset: int):
    candidates = [(abs(prefix_offset - (EXPECTED_PREFIX_BASE + i*SLOT_STRIDE)), i) for i in range(5)]
    distance, slot = min(candidates)
    return slot if distance <= 0x2000 else None


def analyze(data: bytes):
    campaigns = []
    used_slots = set()

    for prefix_offset in find_all(data, PREFIX):
        slot = nearest_slot(prefix_offset)
        if slot is None or slot in used_slots:
            continue

        markers = find_all(
            data, MARKER,
            prefix_offset + 0x5E00,
            min(len(data), prefix_offset + 0x6300)
        )
        if not markers:
            continue

        expected_marker = prefix_offset + 0x601C
        marker_offset = min(markers, key=lambda p: abs(p - expected_marker))

        positive_offset = prefix_offset + len(PREFIX)
        spent1_offset = positive_offset + 3
        negative_offset = marker_offset - 8
        spent2_offset = marker_offset - 4

        current_a = u24be(xor3a(data[positive_offset:positive_offset+3]))
        spent_a = u32be(xor3a(data[spent1_offset:spent1_offset+4]))
        current_b = -i32be(xor3a(data[negative_offset:negative_offset+4]))
        spent_b = u32be(xor3a(data[spent2_offset:spent2_offset+4]))

        summary_offset = SUMMARY_CASH_BASE + slot*SUMMARY_STRIDE
        global_offset = GLOBAL_CASH_BASE + slot*4
        summary_cash = u32be(data[summary_offset:summary_offset+4])
        global_cash = u32be(data[global_offset:global_offset+4])

        campaigns.append({
            "slot": slot + 1,
            "slot_index": slot,
            "positive_offset": positive_offset,
            "negative_offset": negative_offset,
            "summary_offset": summary_offset,
            "global_offset": global_offset,
            "cash": current_a,
            "spent": spent_a,
            "consistent": current_a == current_b == summary_cash == global_cash and spent_a == spent_b,
        })
        used_slots.add(slot)

    campaigns.sort(key=lambda c: c["slot"])
    stored_crc = u32be(data[0x250:0x254])
    calculated_crc = crc32_big_init0(data[0x254:])
    return campaigns, stored_crc, calculated_crc


def patch(data: bytes, target: int) -> bytes:
    if not 0 <= target <= MAX_CASH:
        raise ValueError(f"Cash must be between 0 and {MAX_CASH:,}.")

    campaigns, _, _ = analyze(data)
    if not campaigns:
        raise ValueError("No recognized campaign structures were found.")

    out = bytearray(data)
    plain4 = target.to_bytes(4, "big")
    encoded_pos = xor3a(target.to_bytes(3, "big"))
    encoded_neg = xor3a(((-target) & 0xFFFFFFFF).to_bytes(4, "big"))

    for c in campaigns:
        out[c["summary_offset"]:c["summary_offset"]+4] = plain4
        out[c["global_offset"]:c["global_offset"]+4] = plain4
        out[c["positive_offset"]:c["positive_offset"]+3] = encoded_pos
        out[c["negative_offset"]:c["negative_offset"]+4] = encoded_neg

    crc = crc32_big_init0(bytes(out[0x254:]))
    out[0x250:0x254] = crc.to_bytes(4, "big")

    verify, stored, calculated = analyze(bytes(out))
    if stored != calculated:
        raise RuntimeError("CRC verification failed.")
    for c in verify:
        if c["cash"] != target or not c["consistent"]:
            raise RuntimeError(f"Verification failed for slot {c['slot']}.")

    return bytes(out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="decrypted BSAV0.SAV")
    parser.add_argument("cash", type=lambda s: int(s.replace(",", "").replace("$", "")))
    parser.add_argument("-o", "--output", default="BSAV0.SAV")
    args = parser.parse_args()

    src = Path(args.input)
    data = src.read_bytes()

    campaigns, stored, calc = analyze(data)
    print(f"Detected {len(campaigns)} campaign(s)")
    for c in campaigns:
        state = "OK" if c["consistent"] else "MISMATCH"
        print(f"  Slot {c['slot']}: cash=${c['cash']:,} spent=${c['spent']:,} [{state}]")
    print(f"CRC stored={stored:08X} calculated={calc:08X}")

    output = patch(data, args.cash)
    Path(args.output).write_bytes(output)

    _, new_stored, _ = analyze(output)
    print(f"Patched all detected campaigns to ${args.cash:,}")
    print(f"New CRC={new_stored:08X}")
    print(f"Wrote: {args.output}")


if __name__ == "__main__":
    main()

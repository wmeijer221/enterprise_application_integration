from typing import Sequence

def ensure_tuple(seq: Sequence[object]) -> tuple[object]:
   return seq if isinstance(seq, tuple) else tuple(seq)

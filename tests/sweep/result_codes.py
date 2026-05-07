"""
KACE Sweep Result Classification Codes
=======================================

Defines the four official result categories used by the full Klipper config
sweep and the KACE test runner. Each config processed during a sweep is
assigned exactly one of these codes.

Classification rules (applied in priority order):
  FAILURE     — an unhandled Python exception occurred (crash / bug)
  SAFE_ABORT  — graceful exit due to a known, expected limitation
                (e.g. TODO placeholder pins still active in a generated section)
  UNSUPPORTED — the config uses syntax or sections not supported by the
                current parser/generator (experimental / non-standard features)
  PASS        — full parse + profile extraction completed without issues
"""


class SweepResult:
    """Immutable result record for a single config sweep entry."""

    PASS        = "PASS"
    SAFE_ABORT  = "SAFE_ABORT"
    UNSUPPORTED = "UNSUPPORTED"
    FAILURE     = "FAILURE"

    # ANSI colour codes for terminal output
    _COLOURS = {
        PASS:        "\033[92m",   # green
        SAFE_ABORT:  "\033[93m",   # yellow
        UNSUPPORTED: "\033[96m",   # cyan
        FAILURE:     "\033[91m",   # red
    }
    _RESET = "\033[0m"

    def __init__(self, code: str, filename: str, detail: str = ""):
        """
        Args:
            code:     One of SweepResult.{PASS, SAFE_ABORT, UNSUPPORTED, FAILURE}
            filename: The config filename that was processed (e.g. generic-skr-v1.4.cfg)
            detail:   Optional short description of why the result was assigned.
        """
        if code not in (self.PASS, self.SAFE_ABORT, self.UNSUPPORTED, self.FAILURE):
            raise ValueError(f"Unknown sweep result code: {code!r}")
        self.code     = code
        self.filename = filename
        self.detail   = detail

    def __repr__(self):
        return f"SweepResult({self.code}, {self.filename!r})"

    def coloured_code(self) -> str:
        """Return the code string wrapped in its ANSI colour."""
        colour = self._COLOURS.get(self.code, "")
        return f"{colour}[{self.code}]{self._RESET}"


class SweepSummary:
    """Accumulates SweepResult objects and renders a final statistics table."""

    def __init__(self):
        self.results: list[SweepResult] = []

    def add(self, result: SweepResult):
        self.results.append(result)

    # ── Counters ──────────────────────────────────────────────────────────────

    def count(self, code: str) -> int:
        return sum(1 for r in self.results if r.code == code)

    @property
    def total(self) -> int:
        return len(self.results)

    @property
    def passes(self) -> int:
        return self.count(SweepResult.PASS)

    @property
    def safe_aborts(self) -> int:
        return self.count(SweepResult.SAFE_ABORT)

    @property
    def unsupported(self) -> int:
        return self.count(SweepResult.UNSUPPORTED)

    @property
    def failures(self) -> int:
        return self.count(SweepResult.FAILURE)

    # ── Output ────────────────────────────────────────────────────────────────

    def print_report(self, verbose: bool = False):
        """Print the full sweep report to stdout."""
        W = 60
        print("\n" + "=" * W)
        print("  KACE — Full Klipper Config Sweep Report")
        print("=" * W)

        if verbose:
            # Print every result line
            for r in self.results:
                detail = f"  ({r.detail})" if r.detail else ""
                print(f"  {r.coloured_code():<32} {r.filename}{detail}")
            print("-" * W)

        # Summary statistics
        print(f"  Total configs processed : {self.total}")
        print(f"  \033[92m[PASS]       \033[0m            : {self.passes}")
        print(f"  \033[93m[SAFE_ABORT] \033[0m            : {self.safe_aborts}")
        print(f"  \033[96m[UNSUPPORTED]\033[0m            : {self.unsupported}")
        print(f"  \033[91m[FAILURE]    \033[0m            : {self.failures}")
        print("=" * W)

        if self.failures > 0:
            print("\n\033[91mFAILED CONFIGS (crashes — require investigation):\033[0m")
            for r in self.results:
                if r.code == SweepResult.FAILURE:
                    print(f"  ✗  {r.filename}")
                    if r.detail:
                        print(f"     {r.detail}")
            print()

    def was_successful(self) -> bool:
        """Return True if no hard FAILURE results were recorded."""
        return self.failures == 0

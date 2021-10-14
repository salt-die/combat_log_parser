from pathlib import Path

from .combat_log_parser import parse_line

LOG_DIR = Path("logs")
TEST_LOG = LOG_DIR / "raw" / "WoWCombatLog.txt"

# For testing, write all parsed events as plain text. This will be serialized into a database later.
PARSED_LOG = LOG_DIR / "parsed" / f"{TEST_LOG.stem}_parsed{TEST_LOG.suffix}"

PARSED_LOG.write_text(
    "\n".join(
        str(parse_line(line))
        for line in TEST_LOG.read_text().splitlines()
    )
)

import datetime
import re
from functools import cache

from .data_structures import LogEvent, _tuple_factory

SPACE_RE = re.compile(r'\s+')
COMMA_RE = re.compile(r',(?! )')  # If comma is followed by a space, we're in a quoted string.
REPLACE_RE = re.compile(r'(_.)|(^.)')
EVENTS = (
    'SWING',
    'SPELL_PERIODIC',
    'SPELL_BUILDING',
    'SPELL',
    'RANGE',
    'ENVIRONMENTAL',
    # Special events:
    'DAMAGE_SPLIT',
    'DAMAGE_SHIELD_MISSED',
    'DAMAGE_SHIELD',
    'ENCHANT_APPLIED',
    'ENCHANT_REMOVED',
    'PARTY_KILL',
    'UNIT_DIED',
    'UNIT_DESTROYED',
    'UNIT_DISSIPATES',
)
PARAM_TYPES = {
    'ABSORB',
    'MISS',
    'FIRE',
    'DEBUFF',
    'RESIST',
    'FALLING',
    'DODGE',
    'PARRY',
    'IMMUNE',
    'BUFF',
}

def parse_param(param):
    if param == 'nil':
        return None

    if param in PARAM_TYPES:
        return param

    if param.startswith('"'):
        return param[1: -1]

    return int(param, 16)

def to_pascal_case(match):
    return match.group(0)[-1:].upper()

@cache
def create_subevent(event_type):
    for prefix in EVENTS:
        if event_type.startswith(prefix):
            suffix = event_type.removeprefix(prefix)
            break

    return _tuple_factory(
        REPLACE_RE.sub(to_pascal_case, prefix.lower()),
        REPLACE_RE.sub(to_pascal_case, suffix.lower()),
    )

def parse_line(line):
    _, time, params = SPACE_RE.split(line, maxsplit=2)

    event_type, *params = COMMA_RE.split(params)

    subevent = create_subevent(event_type)
    params = list(map(parse_param, params))

    return LogEvent(
        datetime.time.fromisoformat(time),
        subevent(*params[6:]),
        *params[:6],
    )

from datetime import time
from textwrap import dedent
from typing import NamedTuple, Any

PREFIXES = {
    'Swing': (),
    'Range': ('spell_id', 'spell_name', 'spell_school'),
    'Spell': ('spell_id', 'spell_name', 'spell_school'),
    'SpellPeriodic': ('spell_id', 'spell_name', 'spell_school'),
    'SpellBuilding': ('spell_id', 'spell_name', 'spell_school'),
    'Environmental': (),
}

SUFFIXES = {
    'Damage': (
        'amount',
        'overkill',
        'school',
        'resisted',
        'blocked',
        'absorbed',
        'critical',
        'glancing',
        'crushing',
        'is_offhand',
    ),
    'Missed': (
        'missType',
        'is_offhand',
        'amount_missed',
        'critical',
    ),
    'Heal': (
        'amount',
        'overhealing',
        'absorbed',
        'critical',
    ),
    'HealAbsorbed': (
        'extra_GUID',
        'extra_name',
        'extra_flags',
        'extra_raid_flags',
        'extra_spell_id',
        'extra_spell_name',
        'extra_school',
        'amount',
    ),
    'Absorbed': (),
    'Energize': (
        'amount',
        'over_energize',
        'power_type',
        'alternate_power_type',
    ),
    'Drain': (
        'amount',
        'power_type',
        'extra_amount',
    ),
    'Leech': (
        'amount',
        'power_type',
        'extra_amount',
    ),
    'Interrupt': (
        'extra_spell_id',
        'extra_spell_name',
        'extra_school',
    ),
    'Dispel': (
        'extra_spell_id',
        'extra_spell_name',
        'extra_school',
        'aura_type',
    ),
    'DispelFailed': (
        'extra_spell_id',
        'extra_spell_name',
        'extra_school',
    ),
    'Stolen': (
        'extra_spell_id',
        'extra_spell_name',
        'extra_school',
        'aura_type',
    ),
    'ExtraAttacks': ('amount', ),
    'AuraApplied': ('aura_type', 'amount'),
    'AuraRemoved': ('aura_type', 'amount'),
    'AuraAppliedDose': ('aura_type', 'amount'),
    'AuraRemovedDose': ('aura_type', 'amount'),
    'AuraRefresh': ('aura_type', 'amount'),
    'AuraBroken': ('aura_type', ),
    'AuraBrokenSpell': (
        'extra_spell_id',
        'extra_spell_name',
        'extra_school',
        'aura_type',
    ),
    'CastStart': (),
    'CastSuccess': (),
    'CastFailed': ('failed_type', ),
    'Instakill': (),
    'DurabilityDamage': (),
    'DurabilityDamageAll': (),
    'Create': (),
    'Summon': (),
    'Resurrect': (),
}

SPECIAL = {
    'DamageSplit': PREFIXES['Spell'] + SUFFIXES['Damage'],
    'DamageShield': PREFIXES['Spell'] + SUFFIXES['Damage'],
    'DamageShieldMissed': PREFIXES['Spell'] + SUFFIXES['Missed'],
    'EnchantApplied': ('spell_name', 'item_id', 'item_name'),
    'EnchantRemoved': ('spell_name', 'item_id', 'item_name'),
    'PartyKill': (),
    'UnitDied': ('recap_id', 'unconscious_on_death'),
    'UnitDestroyed': ('recap_id', 'unconscious_on_death'),
    'UnitDissipates': ('recap_id', 'unconscious_on_death'),
}


class LogEvent(NamedTuple):
    time_stamp: time
    subevent: Any
    source_GUID: int
    source_name: str
    source_flags: int
    dest_GUID: int
    dest_name: str
    dest_flags: int


def _tuple_factory(prefix, suffix):
    """
    Create a named tuple from prefix and suffix.
    """
    subevent = prefix + suffix

    attrs = PREFIXES[prefix] + SUFFIXES[suffix] if suffix else SPECIAL[prefix]
    hints = f"\n        ".join(f"{attr}: Any = None" for attr in attrs)

    code = f"""
    class {subevent}(NamedTuple):
        "Combat log subevent"
        {hints}
    """
    exec(dedent(code), globals(), locals())

    return locals()[subevent]

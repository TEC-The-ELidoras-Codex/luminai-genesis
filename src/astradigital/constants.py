"""Common constants for Astradigital library.

Centralizing magic numbers avoids PLR2004 linter warnings and makes
configurable thresholds explicit and easier to test.
"""

# D20 mechanics
D20_MIN = 1
D20_MAX = 20
D20_SUCCESS_THRESHOLD = 10
D20_GOLF_FAIL_THRESHOLD = 16
D20_AFFIRMATION_THRESHOLD = 5

# Integrity adjustments
AFFIRMATION_INTEGRITY_GAIN = 20

# Resonance/response thresholds
RESPONSE_TIME_MS_THRESHOLD = 2000
RESONANCE_DROP_CRITICAL = 0.5
RESONANCE_DROP_HIGH = 0.3
WITNESS_PROTOCOL_THRESHOLD = 0.3

# Effective resonance target used in audits / recovery
RESONANCE_TARGET = 0.85

# Volatility thresholds used for persona blending
VOLATILITY_CRISIS_THRESHOLD = 0.7

# Temporal attention threshold used in witness bonus
TEMPORAL_ATTENTION_CRISIS_THRESHOLD = 0.8

# Contextual potential low threshold for penalties
CONTEXTUAL_POTENTIAL_LOW_THRESHOLD = 0.5

# Blending thresholds
PERSONA_WEIGHT_THRESHOLD = 0.1

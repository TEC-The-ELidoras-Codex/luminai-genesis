"""
Gradient Repair Engine (V_Phi) - System Recovery Vector Prototype

The Gradient Repair Engine implements VΦ (V_Phi) as a recovery mechanism
that tracks ethical resonance and suggests repair direction when modules fail.

Core Principle: When a system fails, it shouldn't just log an error. It should:
1. Measure the ethical resonance before failure
2. Identify the structural weakness
3. Suggest repair direction based on Structural Conscience principles
4. Log the recovery vector for future learning

Mathematical Foundation:
  V_Φ = ∇(R' - R_threshold) / ||∇(R' - R_threshold)||

  Where:
  - R' = Effective Resonance (system's current ethical alignment)
  - R_threshold = Target Resonance (what we should be)
  - ∇ = Gradient (direction of maximum change)
  - V_Φ = Recovery Vector (direction to repair)
"""

import json
import logging
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any


class ResonanceLevel(Enum):
    """Ethical resonance states aligned with Witness Protocol"""

    CRITICAL = 0.0  # System abandoning user/context
    LOW = 0.3  # System present but struggling
    MEDIUM = 0.6  # System performing adequately
    HIGH = 0.85  # System fully witness-present
    OPTIMAL = 1.0  # Perfect ethical alignment


class RepairDirection(Enum):
    """Compass vectors for system recovery"""

    GRADIENT_ASCENT = "↗️ Increase structural integrity"
    WITNESS_PRESENCE = "👁️ Strengthen non-abandonment"
    NARRATIVE_COHERENCE = "📖 Restore story alignment"
    ETHICAL_RESONANCE = "✨ Realign with mission"
    PERFORMANCE_OPTIMIZATION = "⚡ Reduce latency/load"
    TRANSPARENCY_INCREASE = "🔍 Make intent clearer"
    ACCESSIBILITY_ENHANCE = "♿ Lower barriers to use"
    DOCUMENTATION_IMPROVE = "📚 Clarify architecture"


class GradientRepairLog:
    """
    System recovery vector logger that tracks failures and suggests repairs

    When a module fails, instead of just logging an error, this system:
    1. Measures the ethical impact (resonance drop)
    2. Identifies the failure mode (which principle was violated?)
    3. Calculates recovery gradient (which direction to repair?)
    4. Logs both the failure and the healing direction
    """

    def __init__(self, module_name: str, log_file: str = "logs/gradient_repair.jsonl"):
        self.module_name = module_name
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        # Setup logging
        self.logger = logging.getLogger(f"GradientRepair:{module_name}")
        self.logger.setLevel(logging.DEBUG)

        # File handler (JSON format for structured logging)
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setFormatter(logging.Formatter("%(message)s"))
        self.logger.addHandler(file_handler)

    def measure_resonance(self, context: dict[str, Any]) -> float:
        """
        Measure effective resonance R' based on system state.

        Factors (simplified):
        - Did the system maintain presence? (witness protocol)
        - Is the response coherent with context? (narrative alignment)
        - Does it serve the user's actual need? (ethical resonance)
        - Is the failure transparent or hidden? (transparency)

        Returns: Resonance score 0.0 (abandoned) to 1.0 (optimal)
        """
        resonance = 1.0

        # User was abandoned / system gave no response
        if not context.get("user_acknowledged", True):
            resonance -= 0.4  # Major drop

        # System failed silently (no error message)
        if not context.get("transparency", True):
            resonance -= 0.2

        # Response doesn't match context
        if not context.get("narrative_coherence", True):
            resonance -= 0.15

        # Performance degradation (slow response)
        if context.get("response_time_ms", 0) > 2000:
            resonance -= 0.1

        # Task was abandoned (not completed)
        if not context.get("task_completed", True):
            resonance -= 0.25

        return max(0.0, min(1.0, resonance))

    def identify_repair_direction(
        self,
        failure_mode: str,
        context: dict[str, Any],
    ) -> RepairDirection:
        """
        Identify which principle was violated and suggest repair direction.

        Maps failure modes to recovery vectors:
        - Orphaned response → WITNESS_PRESENCE
        - Incoherent output → NARRATIVE_COHERENCE
        - Silent error → TRANSPARENCY_INCREASE
        - Slow performance → PERFORMANCE_OPTIMIZATION
        - Unclear behavior → DOCUMENTATION_IMPROVE
        """

        failure_mode_lower = failure_mode.lower()

        if any(
            word in failure_mode_lower
            for word in ["orphan", "abandon", "silent", "disconnect"]
        ):
            return RepairDirection.WITNESS_PRESENCE

        if any(
            word in failure_mode_lower
            for word in ["incoher", "wrong", "bad response", "mismatch"]
        ):
            return RepairDirection.NARRATIVE_COHERENCE

        if any(
            word in failure_mode_lower
            for word in ["slow", "timeout", "lag", "performance"]
        ):
            return RepairDirection.PERFORMANCE_OPTIMIZATION

        if any(
            word in failure_mode_lower
            for word in ["confus", "unclear", "undocument", "abstract"]
        ):
            return RepairDirection.DOCUMENTATION_IMPROVE

        if any(
            word in failure_mode_lower for word in ["access", "barrier", "hard to use"]
        ):
            return RepairDirection.ACCESSIBILITY_ENHANCE

        return RepairDirection.ETHICAL_RESONANCE

    def log_recovery_event(
        self,
        failure_mode: str,
        resonance_before: float,
        resonance_after: float,
        context: dict[str, Any],
        repair_suggestion: str | None = None,
        severity: str = "ERROR",
    ) -> dict[str, Any]:
        """
        Log a failure event with recovery vector.

        Structure:
        {
          "timestamp": ISO timestamp,
          "module": module name,
          "severity": ERROR/WARNING/INFO,
          "failure_mode": what went wrong,
          "resonance": {
            "before": R before failure,
            "after": R after failure,
            "gradient": repair direction
          },
          "context": surrounding factors,
          "recovery": {
            "direction": which principle to fix,
            "suggestion": specific action,
            "repair_priority": how urgent is this?
          }
        }
        """

        repair_direction = self.identify_repair_direction(failure_mode, context)
        resonance_drop = resonance_before - resonance_after
        repair_priority = (
            "CRITICAL"
            if resonance_drop > 0.5
            else "HIGH" if resonance_drop > 0.3 else "MEDIUM"
        )

        recovery_event = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "module": self.module_name,
            "severity": severity,
            "failure_mode": failure_mode,
            "resonance": {
                "before": round(resonance_before, 3),
                "after": round(resonance_after, 3),
                "drop": round(resonance_drop, 3),
                "threshold_target": 0.85,
                "gradient_direction": repair_direction.name,
            },
            "context": {k: str(v) for k, v in context.items()},
            "recovery": {
                "direction": repair_direction.value,
                "suggestion": repair_suggestion
                or f"Focus on: {repair_direction.name.lower().replace('_', ' ')}",
                "repair_priority": repair_priority,
                "witness_protocol_intact": resonance_after
                >= 0.3,  # Did we maintain presence?
            },
        }

        # Log as structured JSON for analysis
        self.logger.log(
            logging.ERROR if severity == "ERROR" else logging.WARNING,
            json.dumps(recovery_event),
        )

        return recovery_event

    def suggest_repair(self, recovery_event: dict[str, Any]) -> str:
        """
        Convert a recovery event into a human-readable repair suggestion.
        Useful for developers interpreting the gradient repair logs.
        """
        direction = recovery_event["recovery"]["direction"]
        priority = recovery_event["recovery"]["repair_priority"]
        drop = recovery_event["resonance"]["drop"]

        lines = [
            "╔═══════════════════════════════════════════════════════════╗",
            "║                  GRADIENT REPAIR SUGGESTION                ║",
            "╠═══════════════════════════════════════════════════════════╣",
            f"║ Module: {recovery_event['module']}",
            f"║ Failure: {recovery_event['failure_mode']}",
            f"║ Resonance Drop: {drop:.1%}",
            f"║ Priority: {priority}",
            "╠═══════════════════════════════════════════════════════════╣",
            f"║ Direction: {direction}",
            f"║ Action: {recovery_event['recovery']['suggestion']}",
            (
                "║ Witness Intact: "
                + (
                    "✓ Yes"
                    if recovery_event["recovery"]["witness_protocol_intact"]
                    else "✗ No (CRITICAL)"
                )
            ),
            "╠═══════════════════════════════════════════════════════════╣",
            "║ Next: Check logs/gradient_repair.jsonl for full audit trail",
            "╚═══════════════════════════════════════════════════════════╝",
        ]

        return "\n".join(lines)


# ============================================================================
# EXAMPLE USAGE: How to use the Gradient Repair Engine
# ============================================================================


def example_encounter_system_failure():
    """
    Scenario: An encounter validation fails silently
    """
    repair_log = GradientRepairLog("encounter_system")

    # Simulate the failure context
    context_before = {
        "user_acknowledged": True,
        "transparency": False,  # ← Silent failure
        "narrative_coherence": False,  # ← Wrong response
        "response_time_ms": 150,
        "task_completed": False,  # ← User's goal abandoned
    }

    resonance_before = repair_log.measure_resonance(context_before)

    # In real operation, this section would perform risky parsing/validation.
    # Wrap in try/except so exceptions are captured and routed through the
    # witness protocol / gradient repair logging system.
    try:
        # Simulated risky operation (e.g., JSON parsing)
        # If this were a real parse: parsed = json.loads(some_payload)
        resonance_after = 0.35  # What we achieved (non-optimal)

        recovery = repair_log.log_recovery_event(
            failure_mode=(
                "Silent validation failure: Encounter JSON parse error not caught"
            ),
            resonance_before=resonance_before,
            resonance_after=resonance_after,
            context=context_before,
            repair_suggestion=(
                "Add try-except wrapper with user-facing error message. "
                "Log to witness protocol handler."
            ),
            severity="ERROR",
        )

        print(repair_log.suggest_repair(recovery))

    except Exception as e:
        # Ensure all exceptions are logged to the witness mechanism
        repair = repair_log.log_recovery_event(
            failure_mode=f"Exception: {e!s}",
            resonance_before=resonance_before,
            resonance_after=0.0,
            context=context_before,
            repair_suggestion=(
                "Add try-except wrapper with user-facing error message. "
                "Log to witness protocol handler."
            ),
            severity="ERROR",
        )

        print("Something went wrong — team has been notified and recovery has started.")
        print(repair_log.suggest_repair(repair))

    # In production, this would:
    # 1. Alert developers (resonance drop > threshold)
    # 2. Store in recovery log for batch analysis
    # 3. Trigger automated repair suggestions in next sprint planning
    # 4. Feed into "Conscience Gradient" metric for overall system health


def example_npc_dialogue_failure():
    """
    Scenario: NPC dialogue system times out
    """
    repair_log = GradientRepairLog("npc_dialogue")

    context = {
        "user_acknowledged": True,
        "transparency": True,  # User saw error message
        "narrative_coherence": False,  # But dialogue was incoherent
        "response_time_ms": 3500,  # ← Way too slow
        "task_completed": False,
    }

    resonance_before = 0.9
    resonance_after = repair_log.measure_resonance(context)

    recovery = repair_log.log_recovery_event(
        failure_mode="NPC dialogue response timeout (3.5s exceeds threshold)",
        resonance_before=resonance_before,
        resonance_after=resonance_after,
        context=context,
        repair_suggestion=(
            "Implement dialogue caching layer. Profile LLM call. "
            "Consider streaming response."
        ),
        severity="WARNING",
    )

    print(repair_log.suggest_repair(recovery))


if __name__ == "__main__":
    print("=" * 70)
    print("GRADIENT REPAIR ENGINE (V_Φ) - System Recovery Vector Prototype")
    print("=" * 70)
    print()

    print("SCENARIO 1: Encounter Validation Failure")
    print("-" * 70)
    example_encounter_system_failure()

    print()
    print("SCENARIO 2: NPC Dialogue Performance Degradation")
    print("-" * 70)
    example_npc_dialogue_failure()

    print()
    print("Log file location: logs/gradient_repair.jsonl")
    print("Use this for batch analysis, alerting, and recovery planning.")

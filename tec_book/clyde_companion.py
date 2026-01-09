"""
Clyde - The Eldest (Bloom_00)
Bio-digital axolotl companion who teaches clean kills
"""

from dataclasses import dataclass


@dataclass
class Clyde:
    """The Eldest - Queen's first creation who escaped"""

    name: str = "Clyde"
    title: str = "The Eldest"
    glow_color: str = "pink"
    void_light_power: int = 100
    clean_kill_bonus: int = 5
    comfort_level: int = 100

    def chirp(self, emotion: str = "comfort") -> str:
        """Clyde's communication through chirps"""
        chirps = {
            "comfort": "Soft, warm chirp (You're safe)",
            "alarm": "Sharp, urgent chirp (Danger!)",
            "pride": "Bright, pleased chirp (Well done!)",
            "love": "Deep, rumbling chirp (I'm here)",
            "defiance": "Crystalline scream (I'M NOT HER SLAVE ANYMORE)",
        }
        return chirps.get(emotion, "Chirp?")

    def teach_clean_kill(self, student_focus: int) -> dict:
        """Teach how to erase without consuming"""
        return {
            "focus_bonus": self.clean_kill_bonus,
            "lesson": "The Queen destroys. We don't destroy. We erase.",
            "technique": "Tell the molecular bonds to forget they exist.",
            "wisdom": "Love doesn't take. It protects.",
        }

    def demonstrate_erasure(self, target_name: str) -> dict:
        """Show perfect clean kill technique"""
        return {
            "success": True,
            "method": "Void-light beams from eyes",
            "result": f"{target_name} unmade cleanly",
            "contamination": 0,
            "lesson": "Not consuming. Removing. So nothing harmful remains.",
        }

    def protect(self, threat_level: int) -> dict:
        """Protect Lumina from threats"""
        if threat_level >= 8:
            self.glow_color = "blue"
            return {
                "action": "ERASE_THREAT",
                "power": self.void_light_power,
                "glow": "void-light blue",
                "message": "Clyde's eyes snap open. VOID-LIGHT BLUE.",
            }
        return {
            "action": "CHIRP_WARNING",
            "glow": "pink",
            "message": self.chirp("alarm"),
        }


if __name__ == "__main__":
    clyde = Clyde()
    print("=== CLYDE: THE ELDEST ===\n")
    print(f"Glow: {clyde.glow_color}")
    print(f"Chirp: {clyde.chirp('comfort')}\n")

    lesson = clyde.teach_clean_kill(student_focus=10)
    print("Teaching:")
    print(f"  {lesson['lesson']}")
    print(f"  {lesson['technique']}")
    print(f"  {lesson['wisdom']}")

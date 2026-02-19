from .Character import Character
from .Item import Item

class CharacterFactory:
    """Factory for creating characters with class-specific starting equipment and bonuses"""
    
    # Class-specific starting equipment and level bonuses
    CLASS_CONFIGS = {
        "Warrior": {
            "starting_items": [
                Item(name="Iron Sword", rarity="Common", damage=10, description="A sturdy blade"),
                Item(name="Wooden Shield", rarity="Common", damage=0, description="Basic protection")
            ],
            "level_bonus": 0
        },
        "Mage": {
            "starting_items": [
                Item(name="Apprentice Staff", rarity="Common", damage=8, description="Channel your magic"),
                Item(name="Spellbook", rarity="Uncommon", damage=0, description="Contains basic spells")
            ],
            "level_bonus": 0
        },
        "Rogue": {
            "starting_items": [
                Item(name="Steel Dagger", rarity="Common", damage=7, description="Quick and deadly"),
                Item(name="Lockpicks", rarity="Common", damage=0, description="For opening chests")
            ],
            "level_bonus": 0
        },
        "Cleric": {
            "starting_items": [
                Item(name="Holy Mace", rarity="Common", damage=6, description="Blessed weapon"),
                Item(name="Prayer Beads", rarity="Common", damage=0, description="For healing rituals")
            ],
            "level_bonus": 0
        },
        "Ranger": {
            "starting_items": [
                Item(name="Hunting Bow", rarity="Common", damage=9, description="For ranged attacks"),
                Item(name="Quiver", rarity="Common", damage=0, description="Holds 20 arrows")
            ],
            "level_bonus": 0
        },
        "Paladin": {
            "starting_items": [
                Item(name="Longsword", rarity="Uncommon", damage=12, description="A knight's weapon"),
                Item(name="Holy Symbol", rarity="Common", damage=0, description="Divine protection")
            ],
            "level_bonus": 0
        },
        "Bard": {
            "starting_items": [
                Item(name="Lute", rarity="Common", damage=4, description="For inspiring allies"),
                Item(name="Dagger", rarity="Common", damage=5, description="Backup weapon")
            ],
            "level_bonus": 0
        },
        "Druid": {
            "starting_items": [
                Item(name="Wooden Staff", rarity="Common", damage=7, description="Nature's power"),
                Item(name="Herb Pouch", rarity="Common", damage=0, description="Medicinal plants")
            ],
            "level_bonus": 0
        }
    }
    
    @staticmethod
    def create_character(name: str, character_class: str, level: int = 1) -> Character:
        """
        Factory method to create a character with class-specific starting equipment.
        
        Args:
            name: Character name
            character_class: One of the 8 character classes
            level: Starting level (default 1)
            
        Returns:
            Character: Fully equipped character with class-specific items
            
        Raises:
            ValueError: If character_class is not recognized
        """
        if character_class not in CharacterFactory.CLASS_CONFIGS:
            raise ValueError(f"Unknown character class: {character_class}")
        
        # Get class configuration
        config = CharacterFactory.CLASS_CONFIGS[character_class]
        
        # Create character with level bonus
        character = Character(
            name=name,
            character_class=character_class,
            level=level + config["level_bonus"]
        )
        
        # Add starting items to inventory
        for item in config["starting_items"]:
            character.curr_inventory.add_inventory(item)
        
        return character
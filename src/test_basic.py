"""
Quick verification test before main.py implementation.
Tests basic imports and time system functionality.
"""

print("=" * 50)
print("GUILDQUEST - BASIC VERIFICATION TEST")
print("=" * 50)

# Test 1: Core imports
print("\n[TEST 1] Testing core imports...")
try:
    from core import GameTime, WorldClock
    print("✅ Core imports successful")
except ImportError as e:
    print(f"❌ Core import failed: {e}")
    exit(1)

# Test 2: Model imports
print("\n[TEST 2] Testing model imports...")
try:
    from models import Campaign, Quest_Event, User, Realm, Character, Item, Inventory
    print("✅ Model imports successful")
except ImportError as e:
    print(f"❌ Model import failed: {e}")
    exit(1)

# Test 3: Utils imports
print("\n[TEST 3] Testing utils imports...")
try:
    from utils import convert_to_realm_time
    print("✅ Utils imports successful")
except ImportError as e:
    print(f"❌ Utils import failed: {e}")
    exit(1)

# Test 4: World Clock basic functionality
print("\n[TEST 4] Testing World Clock...")
clock = WorldClock()
print(f"   Initial time: {clock.get_current_time().get_fulltime()}")
assert clock.get_current_time().get_fulltime(
) == "Day 0, 00:00:00", "Initial time should be Day 0"
print("✅ Initial time correct")

# Test 5: Advancing time
print("\n[TEST 5] Testing time advancement...")
clock.advance(days=5, hours=14, minutes=30)
current = clock.get_current_time()
print(f"   After advance: {current.get_fulltime()}")
assert current.get_day() == 5, "Day should be 5"
assert current.get_hour() == 14, "Hour should be 14"
assert current.get_minute() == 30, "Minute should be 30"
print("✅ Time advancement works")

# Test 6: Time normalization
print("\n[TEST 6] Testing time normalization...")
clock2 = WorldClock()
# 26 hours + 90 minutes = 1 day, 3 hours, 30 minutes
clock2.advance(hours=26, minutes=90)
result = clock2.get_current_time()
print(f"   26 hours + 90 minutes = {result.get_fulltime()}")
assert result.get_day() == 1, "Should normalize to 1 day"
assert result.get_hour() == 3, "Should normalize to 3 hours"
assert result.get_minute() == 30, "Should normalize to 30 minutes"
print("✅ Time normalization works")

# Test 7: Realm time conversion
print("\n[TEST 7] Testing realm time conversion...")
test_realm = Realm(
    name="Eastern Kingdom",
    map_id=1,
    time_rule=120,  # 2 hours ahead
    selected_user=None,
    desc="Test realm"
)
world_time = GameTime(current_day=1, current_hour=10, current_minute=0)
local_time = convert_to_realm_time(world_time, test_realm)
print(f"   World time: {world_time.get_fulltime()}")
print(f"   Realm time (+120 min): {local_time.get_fulltime()}")
assert local_time.get_hour() == 12, "Local time should be 2 hours ahead"
print("✅ Realm time conversion works")

# Test 8: Game_Time comparison
print("\n[TEST 8] Testing Game_Time comparison...")
time1 = GameTime(current_day=1, current_hour=10, current_minute=30)
time2 = GameTime(current_day=1, current_hour=14, current_minute=0)
time3 = GameTime(current_day=2, current_hour=8, current_minute=0)
assert time1.to_total_minutes() < time2.to_total_minutes(), "time1 should be before time2"
assert time2.to_total_minutes() < time3.to_total_minutes(), "time2 should be before time3"
print("✅ Time comparison works")

# Test 9: Creating a basic quest event
print("\n[TEST 9] Testing Quest Event creation...")
quest_time = GameTime(current_day=3, current_hour=15, current_minute=0)
quest_realm = Realm(
    name="Dragon's Lair",
    map_id=2,
    time_rule=0,
    selected_user=None
)
quest = Quest_Event(
    name="Defeat the Dragon",
    c_realm=quest_realm,
    time=quest_time,
    start_time=quest_time.get_fulltime(),
    end_time="N/A"
)
print(f"   Quest: {quest.name}")
print(f"   Start: {quest.start_time}")
print(f"   Realm: {quest.c_realm.name}")
print("✅ Quest Event creation works")

# Test 10: Start/Stop clock
print("\n[TEST 10] Testing clock start/stop...")
clock3 = WorldClock()
assert not clock3.is_running, "Clock should start stopped"
clock3.start()
assert clock3.is_running, "Clock should be running"
clock3.stop()
assert not clock3.is_running, "Clock should be stopped"
print("✅ Clock start/stop works")

print("\n" + "=" * 50)
print("✅ ALL TESTS PASSED!")
print("=" * 50)
print("\nYou're ready to implement main.py!")

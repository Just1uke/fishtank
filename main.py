import time
from lib.bowl import Bowl
import keyboard

def main() -> None:
    tank_width = 73
    tank_height = 30
    bowl = Bowl(width=tank_width, height=tank_height, save_file="tank_state.json")

    # ✅ Load saved state if it exists
    bowl.load_state()

    try:
        while True:
            # ✅ Check if there's a key event (non-blocking)
            if keyboard.is_pressed("p"):
                bowl.toggle_pause()
                time.sleep(0.3)  # Prevent repeat keypresses

            if keyboard.is_pressed("s"):
                bowl.spawn_creature()
                time.sleep(0.3)  # Prevent repeat keypresses

            if keyboard.is_pressed("k"):
                bowl.kill_random_creature()
                time.sleep(0.3)  # Prevent repeat keypresses

            if keyboard.is_pressed("f"):
                bowl.drop_food()
                time.sleep(0.3)  # Prevent repeat keypresses

            if not bowl.paused:
                print(bowl.render())
                bowl.update()

            time.sleep(0.3)
            print("\033c", end="")  # Clear screen for animation

    except KeyboardInterrupt:
        print("\nExiting... Saving state.")
        bowl.save_state()


if __name__ == "__main__":
    main()

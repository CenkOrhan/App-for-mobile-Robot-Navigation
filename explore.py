#! /usr/bin/env python
# -*- encoding: UTF-8 -*-
import qi
import argparse
import sys
import time


global checkpoint
def check_head_touch(touch_service,body):
    while True:
        touch_status = touch_service.getStatus()
        
        for body_part, touched, _ in touch_status:
            if body_part == body and touched:
                return True

        # Kurze Pause, bevor der Status erneut überprüft wird
        time.sleep(0.1)

def load_map(navigation_service,path):
    navigation_service.stopLocalization()
    navigation_service.loadExploration(path)
    navigation_service.relocalizeInMap([0.,0])
    navigation_service.startLocalization()


def set_collision(motion_service,sens):
    sens = 0.01
    motion_service.setCollisionProtectionEnabled("LArm", True)
    motion_service.setCollisionProtectionEnabled("RArm", True)
    motion_service.setOrthogonalSecurityDistance(sens)
    motion_service.setTangentialSecurityDistance(sens)

def animation(session,path):
    animation_player_service = session.service("ALAnimationPlayer")
    animation_player_service.run(path)

def set_led_color(led_service, color):
    # Get the ALLeds service
    led_service = session.service("ALLeds")
    
    # Define the color values
    if color == 'green':
        red_value = 0
        green_value = 255
        blue_value = 0
    elif color == 'red':
        red_value = 255
        green_value = 0
        blue_value = 0
    else:
        raise ValueError("Color must be 'green' or 'red'")
    
    # Define the duration of the blink in seconds
    blink_duration = 0.5
    
    # Set the color of the shoulder LEDs for a short blink
    led_service.fadeRGB("ChestLeds", red_value, green_value, blue_value, blink_duration)
    led_service.fadeRGB("ChestLeds", red_value, green_value, blue_value, blink_duration)
    
    # Set the LEDs back to off after the blink duration
    led_service.fadeRGB("ChestLeds", 0, 0, 0, blink_duration)
    led_service.fadeRGB("ChestLeds", 0, 0, 0, blink_duration)

def set_laser(motion_service,sens):
    motion_service.setCollisionProtectionEnabled("LArm", True)
    motion_service.setCollisionProtectionEnabled("RArm", True)
    motion_service.setOrthogonalSecurityDistance(sens)
    motion_service.setTangentialSecurityDistance(sens)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="141.71.72.113",
                        help="Robot IP address. On robot or Local Naoqi: use '141.71.72.113")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) + ".\n" \
              "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    x_pixel, y_pixel, map_data, previous_point = None, None, None, None
    checkpoint = 0
    target_position = [14.640718460083008, 5.238556861877441, 0.8898776769638062]
    #test_position = [5.954308009594679, 1.8546644926071167, 0.82]
    intermediate_position = [0, 0, 0]
    
    navigation_service = session.service("ALNavigation")
    touch_service = session.service("ALTouch")
    tts = session.service("ALTextToSpeech")
    led_service = session.service("ALLeds")
    motion_service = session.service("ALMotion")
    set_laser(motion_service, 0.01)
    while True:
        if check_head_touch(touch_service, "Head"):
            if checkpoint == 0:
                #tts.say("Daten werden geladen")
                set_led_color(led_service,"green")
                time.sleep(2)
                load_map(navigation_service, "/home/nao/.local/share/Explorer/2024-06-25T163207.255Z.explo")
                time.sleep(2)
                set_led_color(led_service,"green")
                #tts.say("Daten wurden geladen")
                navigation_service.moveAlong(["Holonomic", ["Line", [-0.75, 0.0]], 3.14/2, 6.5])
                time.sleep(3)
                value = navigation_service.navigateToInMap(target_position)
                time.sleep(3)
                if value == 0:
                    animation(session,"animations/Stand/Gestures/Hey_1")
                    tts.say("Hallo, ich bin Pepper. Willkommen im Zukunftslabor. Schön, dass ihr da seid")
                    checkpoint = 2
                else:
                    set_led_color(led_service,"red")
                    #tts.say("fahrt zum flur gescheitert")
                    checkpoint = 1  # Nach dem Laden der Daten immer in checkpoint 1 wechseln
            elif checkpoint == 1:
                tts.say("fahrt weiter zum Flur ausführen")
                navigation_service.moveAlong(["Holonomic", ["Line", [0.0, 0.0]], 0.2, 6.5])
                time.sleep(3)
                value = navigation_service.navigateToInMap(target_position)
                time.sleep(3)
                if value == 0:
                    animation(session,"animations/Stand/Gestures/Hey_1")
                    tts.say("Hallo, ich bin Pepper. Willkommen im Zukunftslabor. Schön, dass ihr da seid")
                    checkpoint = 2
                else:
                    set_led_color(led_service,"red")
                    #tts.say("fahrt zum Flur erneut gescheitert")
                    checkpoint = 1
            elif checkpoint == 2:
                tts.say("Wir fahren jetzt gemeinsam zum Zukunftslabor. Kommt mit mir mit!")
                navigation_service.moveAlong(["Holonomic", ["Line", [0.0, 0.0]], 0.2, 6.5])
                time.sleep(3)
                value = navigation_service.navigateToInMap(intermediate_position)
                time.sleep(3)
                if value == 0:
                    tts.say("Das ist das Zukunftslabor.")
                    navigation_service.moveAlong(["Holonomic", ["Line", [0.0, 0.0]], 3.14, 6.5])
                    animation(session,"animations/Stand/Gestures/ShowSky_1")
                    tts.say("Die Toillten befinden sich rechts von euch. Wenn sie abgeschlossen sind, begebt euch in die zweite Etage. Ihr könnt nun das Labor betreten")
                    checkpoint = 0
                    break
                else:
                    set_led_color(led_service,"red")
                    #tts.say("fahrt zum Labor gescheitert")
                    checkpoint = 2
            else:
                break
            time.sleep(2)
    

    
   
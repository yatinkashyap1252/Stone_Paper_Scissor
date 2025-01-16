import cv2
from cvzone.HandTrackingModule import HandDetector
import random

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8, maxHands=1)

new_choice = True
choice = ""
result_text = ""
result_color = (0, 255, 0)

user_score = 0
computer_score = 0

def get_computer_choice():
    options = ["Paper", "Rock", "Scissors"]
    return random.choice(options)

def determine_result(computer_choice, user_fingers):
    global result_text, result_color, user_score, computer_score
    user_choice = ""
    
    if user_fingers == [1, 1, 1, 1, 1]:
        user_choice = "Paper"
    elif user_fingers == [0, 1, 1, 0, 0]:
        user_choice = "Scissors"
    elif user_fingers == [0, 0, 0, 0, 0]:
        user_choice = "Rock"

    if user_choice == computer_choice:
        result_text = "It's a Tie!"
        result_color = (255, 255, 0)
    elif (user_choice == "Rock" and computer_choice == "Scissors") or \
         (user_choice == "Scissors" and computer_choice == "Paper") or \
         (user_choice == "Paper" and computer_choice == "Rock"):
        result_text = "You Win!"
        result_color = (0, 255, 0)
        user_score += 1
    else:
        result_text = "You Lose!"
        result_color = (0, 0, 255)
        computer_score += 1

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)
    
    if hands:
        hand1 = hands[0]
        finger1 = detector.fingersUp(hand1)

        if new_choice:
            choice = get_computer_choice()
            determine_result(choice, finger1)
            new_choice = False

    cv2.putText(img, "Press 'N' for New Round or 'Q' to Quit", (30, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    cv2.putText(img, f"Computer's Choice: {choice}", (30, 80), 
                cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 255, 0), 4)
    if result_text:
        cv2.putText(img, result_text, (450, 200), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, result_color, 4)

    cv2.putText(img, f"Your Score: {user_score}", (30, 200), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 3)
    cv2.putText(img, f"Computer Score: {computer_score}", (30, 250), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 3)

    if cv2.waitKey(1) & 0xFF == ord('n'):
        new_choice = True
        result_text = ""

    cv2.imshow("Rock Paper Scissors", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
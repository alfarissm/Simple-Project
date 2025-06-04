import cv2
import mediapipe as mp
import time

class HandDetector:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(
                        img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def countFingers(self, img):
        fingerCount = 0
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[0]
            fingers = []
            
            # Ibu jari
            if myHand.landmark[4].x < myHand.landmark[3].x:
                fingers.append(1)
            else:
                fingers.append(0)
            
            # 4 jari lainnya
            for id in range(8, 21, 4):
                if myHand.landmark[id].y < myHand.landmark[id-2].y:
                    fingers.append(1)
                else:
                    fingers.append(0)
            
            fingerCount = sum(fingers)
            
            # Menampilkan angka
            cv2.putText(img, str(fingerCount), (45, 375), cv2.FONT_HERSHEY_PLAIN,
                    10, (255, 0, 0), 25)
        
        return fingerCount, img

def main():
    cap = cv2.VideoCapture(0)
    detector = HandDetector()
    
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        count, img = detector.countFingers(img)
        
        cv2.imshow("Hand Detection", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
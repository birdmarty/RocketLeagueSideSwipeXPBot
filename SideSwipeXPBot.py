import cv2
import numpy as np
import pyautogui
import time
import keyboard

dismiss_img = cv2.imread("Dismiss.png", cv2.IMREAD_GRAYSCALE)

# Function to detect and click the "Login" button
def detect_and_click_login():
    try:
        Login_img = cv2.imread("Login.png", cv2.IMREAD_GRAYSCALE)
        if Login_img is None:
            print("Error: Unable to load 'Login.png'")
            return False
        
        screen = np.array(pyautogui.screenshot())
        screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        
        result = cv2.matchTemplate(screen_gray, Login_img, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val > 0.5:  # Adjust this threshold as needed
            Login_pos = (max_loc[0] + Login_img.shape[1] // 2, max_loc[1] + Login_img.shape[0] // 2)
            pyautogui.click(Login_pos)
            print("Successfully clicked the 'Login' button.")
            time.sleep(30)
            return True
        else:
            print("Failed to find the 'Login' button.")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False
        
        
        
# Function to check if the Challenges button is glowing orange
# Function to check if the Challenges button is glowing orange
def is_challenges_glowing():
    try:
        # Load the Challenges image
        challenges_img = cv2.imread("Challenges.png")
        if challenges_img is None:
            print("Error: Unable to load 'Challenges.png'")
            return False
        
        # Take a screenshot of the screen
        screen = pyautogui.screenshot()
        screen_np = np.array(screen)
        
        # Search for the Challenges image in the screenshot
        result = cv2.matchTemplate(screen_np, challenges_img, cv2.TM_CCOEFF_NORMED)
        _, _, _, max_loc = cv2.minMaxLoc(result)
        
        # Define the region around the Challenges image
        challenges_region = (
            max_loc[0], max_loc[1], 
            max_loc[0] + challenges_img.shape[1], 
            max_loc[1] + challenges_img.shape[0]
        )
        
        # Take a screenshot of the defined region
        challenges_screen = pyautogui.screenshot(region=challenges_region)
        challenges_screen_np = np.array(challenges_screen)
        
        # Define the RGB values of the glowing orange color
        orange_lower = np.array([200, 90, 0], dtype="uint8")
        orange_upper = np.array([255, 140, 30], dtype="uint8")
        
        # Mask the image to find pixels within the orange color range
        mask = cv2.inRange(challenges_screen_np, orange_lower, orange_upper)
        
        # Count the number of non-zero pixels in the mask
        num_orange_pixels = cv2.countNonZero(mask)
        
        # You can adjust the threshold as needed
        if num_orange_pixels > 1000:
            print("challenges glowing")
            return True
        else:
            print("challenges not glowing")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False


# Function to detect and click the "Challenges" button
def check_challenges():
    try:
        # Check if the Challenges button is glowing orange
        if is_challenges_glowing():
            # The Challenges button is glowing, proceed with claiming rewards
            challenges_button_pos = (1970, 1105)  # Coordinates of the Challenges button
            pyautogui.click(challenges_button_pos)
            print("Successfully clicked the 'Challenges' button.")
            
            time.sleep(2)  # Add a small delay to allow the interface to load
            
            screen = np.array(pyautogui.screenshot())
            screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            
            # Look for and click the claim button for regular challenges
            claim_button_img = cv2.imread("Claim.png", cv2.IMREAD_GRAYSCALE)
            regular_claim_button_pos = find_and_click_claim_button(screen_gray, claim_button_img)
            
            time.sleep(2)
            
            # Look for and click the weekly claim button regardless of regular claim button status
            weekly_button_img = cv2.imread("Weekly.png", cv2.IMREAD_GRAYSCALE)
            detect_and_click_weekly(screen_gray,weekly_button_img)
            
            time.sleep(2)
            
            # Look for and click the seasonal claim button regardless of regular claim button status
            seasonal_button_img = cv2.imread("Seasonal.png", cv2.IMREAD_GRAYSCALE)
            detect_and_click_seasonal(screen_gray,seasonal_button_img)
            
            time.sleep(2)
            
            back_button_pos = (731, 190)  # Coordinates of the back button
            pyautogui.click(back_button_pos)
            print("Successfully clicked the 'Back' button.")
            
            # Check if regular claim button was not found and neither weekly nor seasonal buttons were found
            if not regular_claim_button_pos and not weekly_button_img and not seasonal_button_img:
                print("Paradox detected, bad bad bad")
                return False
            else:
                return True
        else:
            print("Challenges button not glowing.")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False




# Function to find and click the claim button
def find_and_click_claim_button(screen_gray, claim_button_img):
    result = cv2.matchTemplate(screen_gray, claim_button_img, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    if max_val > 0.5:
        claim_button_pos = (max_loc[0] + claim_button_img.shape[1] // 2, max_loc[1] + claim_button_img.shape[0] // 2)
        pyautogui.click(claim_button_pos) #Click the claim button
        print("Successfully clicked the 'Claim' button.")
        time.sleep(3)
        click_dismiss()
        return claim_button_pos
    else:
        print("Claim button not found.")
        return None



# Function to detect and click the "Weekly" claim button
def detect_and_click_weekly(screen_gray, weekly_button_img):
    time.sleep(2)
    result = cv2.matchTemplate(screen_gray, weekly_button_img, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    if max_val > 0.5:
        weekly_button_pos = (max_loc[0] + weekly_button_img.shape[1] // 2, max_loc[1] + weekly_button_img.shape[0] // 2)
        pyautogui.click(weekly_button_pos)
        time.sleep(2)
        print("Successfully clicked the 'Weekly' button.")
        time.sleep(2)
        # Look for and click the claim button again after clicking weekly button
        claim_button_img = cv2.imread("Claim.png", cv2.IMREAD_GRAYSCALE)
        find_and_click_claim_button(screen_gray, claim_button_img)
    else:
        print("Weekly button not found.")



# Function to detect and click the "Seasonal" claim button
def detect_and_click_seasonal(screen_gray, seasonal_button_img):
    time.sleep(2)
    result = cv2.matchTemplate(screen_gray, seasonal_button_img, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    if max_val > 0.5:
        seasonal_button_pos = (max_loc[0] + seasonal_button_img.shape[1] // 2, max_loc[1] + seasonal_button_img.shape[0] // 2)
        pyautogui.click(seasonal_button_pos)
        time.sleep(2)
        print("Successfully clicked the 'Seasonal' button.")
        # Look for and click the claim button again after clicking seasonal button
        claim_button_img = cv2.imread("Claim.png", cv2.IMREAD_GRAYSCALE)
        find_and_click_claim_button(screen_gray, claim_button_img)
    else:
        print("Seasonal button not found.")



def click_dismiss():
    try:
        dismiss_button_img = cv2.imread("dismiss.png", cv2.IMREAD_GRAYSCALE)
        if dismiss_button_img is None:
            print("Error: Unable to load 'dismiss.png'")
            return False
        
        screen = np.array(pyautogui.screenshot())
        screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        
        result = cv2.matchTemplate(screen_gray, dismiss_button_img, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val > 0.5:  # Adjust this threshold as needed
            dismiss_button_pos = (max_loc[0] + dismiss_button_img.shape[1] // 2, max_loc[1] + dismiss_button_img.shape[0] // 2)
            pyautogui.click(dismiss_button_pos)
            print("Successfully clicked the 'Dismiss' button.")
            return True
        else:
            print("Dismiss button not found.")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False



# Function to detect and click the "Play" button
def detect_and_click_play():
    try:
        play_button_img = cv2.imread("play_button.png", cv2.IMREAD_GRAYSCALE)
        if play_button_img is None:
            print("Error: Unable to load 'play_button.png'")
            return False
        
        screen = np.array(pyautogui.screenshot())
        screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        
        result = cv2.matchTemplate(screen_gray, play_button_img, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val > 0.5:  # Adjust this threshold as needed
            # Call check_challenges function before clicking the play button
            check_challenges()
            play_button_pos = (max_loc[0] + play_button_img.shape[1] // 2, max_loc[1] + play_button_img.shape[0] // 2)
            pyautogui.click(play_button_pos)
            pyautogui.moveTo(pyautogui.size()[0] // 2, pyautogui.size()[1] // 2)  # Move cursor to the middle of the screen
            print("Successfully clicked the 'Play' button.")
            return True
        else:
            print("Failed to find the 'Play' button.")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False



# Function to detect and click the "Find Match" button
def detect_and_click_find_match():
    try:
        find_match_button_img = cv2.imread("find_match_button.png", cv2.IMREAD_GRAYSCALE)
        if find_match_button_img is None:
            print("Error: Unable to load 'find_match_button.png'")
            return False
        
        screen = np.array(pyautogui.screenshot())
        screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        
        result = cv2.matchTemplate(screen_gray, find_match_button_img, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val > 0.5:  # Adjust this threshold as needed
            find_match_button_pos = (max_loc[0] + find_match_button_img.shape[1] // 2, max_loc[1] + find_match_button_img.shape[0] // 2)
            pyautogui.click(find_match_button_pos)
            pyautogui.moveTo(pyautogui.size()[0] // 2, pyautogui.size()[1] // 2)  # Move cursor to the middle of the screen
            print("Successfully clicked the 'Find Match' button.")
            return True
        else:
            print("Failed to find the 'Find Match' button.")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False
        
        
        
# Function to detect if in "waiting for match" state and perform actions accordingly
def waiting_for_match():
    try:
        cancel_button_blue_img = cv2.imread("cancel_button_blue.png", cv2.IMREAD_GRAYSCALE)
        play_button_img = cv2.imread("play_button.png", cv2.IMREAD_GRAYSCALE)
        find_match_button_img = cv2.imread("find_match_button.png", cv2.IMREAD_GRAYSCALE)
        login_button_img = cv2.imread("Login.png", cv2.IMREAD_GRAYSCALE)
        close_button_img = cv2.imread("Close.png", cv2.IMREAD_GRAYSCALE)
        match_summary_img = cv2.imread("match_summary.png", cv2.IMREAD_GRAYSCALE)
        
        check_interval = 10  # Interval in seconds to check for play or find match button
        spam_interval = 1  # Interval in seconds for keyboard spamming
        
        while True:
            screen = np.array(pyautogui.screenshot())  # Define screen and screen_gray
            screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            
            # Check for Close button
            result_close = cv2.matchTemplate(screen_gray, close_button_img, cv2.TM_CCOEFF_NORMED)
            _, max_val_close, _, _ = cv2.minMaxLoc(result_close)
            if max_val_close > 0.8:
                print("Close button found.")
                # Click the Close button
                close_button_pos = pyautogui.locateCenterOnScreen("Close.png")
                pyautogui.click(close_button_pos)
                print("Successfully clicked the 'Close' button.")
                time.sleep(1)  # Wait for a moment after clicking close button
                continue
                
            # Check for Match Summary button
            result_match_summary = cv2.matchTemplate(screen_gray, match_summary_img, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result_match_summary)
            if max_val > 0.6:
                print("Match summary button found.")
                # Click the Close button
                match_summary_pos = ((max_loc[0] + match_summary_img.shape[1] // 2)-187, max_loc[1] + match_summary_img.shape[0] // 2)
                pyautogui.click(match_summary_pos)
                print("Successfully clicked the 'match summary' button.")
                time.sleep(10)
                continue
                
            # Check for blue cancel button
            result_blue = cv2.matchTemplate(screen_gray, cancel_button_blue_img, cv2.TM_CCOEFF_NORMED)
            _, max_val_blue, _, _ = cv2.minMaxLoc(result_blue)
            if max_val_blue > 0.5:
                print("Blue cancel button found.")
                time.sleep(2)
                check_challenges()
                # Wait for 2 seconds before checking for blue cancel button again
                continue
                
            # Check for login button
            result_login = cv2.matchTemplate(screen_gray, login_button_img, cv2.TM_CCOEFF_NORMED)
            _, max_val_login, _, _ = cv2.minMaxLoc(result_login)
            if max_val_login > 0.5:
                print("Login button found.")
                # Initiate detect_and_click_login
                detect_and_click_login()
                # Wait for 1 second before checking for blue cancel button again
                time.sleep(1)
                continue
            
            # Check for play button
            result_play = cv2.matchTemplate(screen_gray, play_button_img, cv2.TM_CCOEFF_NORMED)
            _, max_val_play, _, _ = cv2.minMaxLoc(result_play)
            if max_val_play > 0.5:
                print("Play button found.")
                # Initiate detect_and_click_play
                detect_and_click_play()
                return
                
            # Check for find match button
            result_find_match = cv2.matchTemplate(screen_gray, find_match_button_img, cv2.TM_CCOEFF_NORMED)
            _, max_val_find_match, _, _ = cv2.minMaxLoc(result_find_match)
            if max_val_find_match > 0.5:
                print("Find match button found.")
                # Initiate detect_and_click_find_match
                detect_and_click_find_match()
                # Wait for 1 second before checking for login or blue cancel button again
                time.sleep(1)
                continue
                
            # If none of the buttons are found, start spamming keys
            print("None of the buttons found. Spamming keys...")
            try:
                for _ in range(check_interval):
                    for _ in range(spam_interval * 10):  # Press keys every 0.1 second
                        keyboard.press('a')
                        keyboard.release('a')
                        keyboard.press('s')
                        keyboard.release('s')
                        keyboard.press('d')
                        keyboard.release('d')
                        keyboard.press('w')
                        keyboard.release('w')
                        keyboard.press('space')
                        keyboard.release('space')
                    
                    # Check for login or find match button after spamming keys
                    result_login = cv2.matchTemplate(screen_gray, login_button_img, cv2.TM_CCOEFF_NORMED)
                    _, max_val_login, _, _ = cv2.minMaxLoc(result_login)
                    if max_val_login > 0.5:
                        print("Login button found while spamming keys.")
                        # Initiate detect_and_click_login
                        detect_and_click_login()
                    
                    result_find_match = cv2.matchTemplate(screen_gray, find_match_button_img, cv2.TM_CCOEFF_NORMED)
                    _, max_val_find_match, _, _ = cv2.minMaxLoc(result_find_match)
                    if max_val_find_match > 0.5:
                        print("Find match button found while spamming keys.")
                        # Initiate detect_and_click_find_match
                        detect_and_click_find_match()
                    
            except KeyboardInterrupt:
                print("Spamming stopped.")
                
    except Exception as e:
        print(f"Error: {e}")




# Main function
def main():
    while True:
        detect_and_click_play()
        time.sleep(1)  # Add a 1 second delay before attempting to find match
        detect_and_click_find_match()
        time.sleep(2)
        waiting_for_match()

if __name__ == "__main__":
    main()

# Add event listener to stop the program when the 'esc' key is pressed
keyboard.on_press_key('esc', lambda _: exit())
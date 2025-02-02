import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

driver = webdriver.Chrome()
driver.get("https://www.covers.com/sport/basketball/nba/player-props")

matchup_class = '.matchup-cta.u-bg-white.u-inlineflex.u-flex-row.u-nowrap.u-align-content-center.u-justify-content-flexstart.u-align-items-center'

def cleanUrl(href):
    result = re.sub(r'/.*?/', '', href).replace('https:www.covers.combasketballplayers','')
    result = result.replace("-", " ").split()
    cap_result = [cap.capitalize() for cap in result]
    return ' '.join(cap_result)

def getLinks():
    game_links = driver.find_elements(By.CSS_SELECTOR, matchup_class)
    for game in game_links:
        href = str(game.get_attribute("href"))
        game_iteration.append(href)
def getStats():
    soup = BeautifulSoup(driver.page_source, "html.parser")

    for link in driver.find_elements(By.CSS_SELECTOR, '.player-link'):
        href = link.get_attribute("href")
        player_name = str(cleanUrl(href))
        if player_name not in playerProps:
            playerProps[player_name] = []
        players.append(player_name)


    for hit in soup.find_all(class_="other-over-odds"):
        try:
            prop_value = float(hit.contents[0].strip())
            props.append(prop_value)

        except (ValueError, AttributeError):
            pass

players = []
props = []
game_iteration = []
selections = ['POINTS','POINTS_REBOUNDS','POINTS_ASSISTS','3_POINTERS_MADE','REBOUNDS_ASSISTS',
              'STEALS_BLOCKS','BLOCKS','STEALS','REBOUNDS','POINTS_REBOUNDS_ASSISTS','TURNOVERS','ASSISTS']


getLinks()

playerProps = {}

for link in game_iteration:
    driver.get(link)
    dropdown_menu = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "prop-events-list"))
    )
    dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-default.dropdown-toggle.u-bg-white")))
    
    dropdown.click()

    li_elements = dropdown_menu.find_elements(By.TAG_NAME, "li")
    time.sleep(1)

    for index, li in enumerate(li_elements, start=1):
        li.click()
        time.sleep(1) 
        getStats()
        time.sleep(1) 

        if len(players) == len(props):
            for player, prop in zip(players, props):
                playerProps[player].append(prop)
        players = []
        props = []

        if index < len(li_elements):
            dropdown_menu = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "prop-events-list"))
            )
            li_elements = dropdown_menu.find_elements(By.TAG_NAME, "li")
        
        dropdown.click() 
        time.sleep(1)
print(playerProps)
driver.quit()
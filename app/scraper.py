import requests
from bs4 import BeautifulSoup

def scrape_data():
    # URL of the Texas Lottery Scratch Offs page
    URL = 'https://www.texaslottery.com/export/sites/lottery/Games/Scratch_Offs/all.html'

    # Send a GET request to the website
    response = requests.get(URL)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table containing the scratch-off games
    table = soup.find('table')

    # List to store scraped data
    scraped_data = []
    current_game_data = {}
    row_count = 0  # Initialize row count

    # Iterate over each row in the table, skipping the header row
    for row in table.find_all('tr')[1:]:
        columns = row.find_all('td')

        # Check if it's a primary row
        if row_count % 3 == 0:  # Every third row is a new game
            # If there's existing game data, append it before starting a new game
            if current_game_data:
                scraped_data.append(current_game_data)
                current_game_data = {}

            current_game_data = {
                'Game Number': columns[0].text.strip(),
                'Start Date': columns[1].text.strip(),
                'Ticket Price': columns[2].text.strip(),
                'Game Name': columns[4].text.strip(),
                'Prize Amount': columns[5].text.strip(),
                'Prizes Printed': columns[6].text.strip(),
                'Prizes Claimed': columns[7].text.strip(),
            }
        else:
            # Define suffix for the keys based on the row count
            suffix = ' 2' if row_count % 3 == 1 else ' 3'

            # Append the last three columns from the second and third rows
            current_game_data['Prize Amount' + suffix] = columns[5].text.strip()
            current_game_data['Prizes Printed' + suffix] = columns[6].text.strip()
            current_game_data['Prizes Claimed' + suffix] = columns[7].text.strip()

        row_count += 1  # Increment row count

    # Append the last game data
    if current_game_data:
        scraped_data.append(current_game_data)

    return scraped_data

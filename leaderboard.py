import requests
from bs4 import BeautifulSoup
from optparse import OptionParser


url = 'https://www.op.gg/leaderboards/tier'


def get_leaderboard(num_players, start=0):
    response = requests.get(url)

    # obtain the entire HTML document
    soup = BeautifulSoup(response.text, 'html.parser')
    
    lb_table = soup.find('table',  {'class': 'css-1l95r9q'})

    if lb_table:
        rows = lb_table.find_all('tr')[start:]

        leaderboard = []
        for row in rows:
            columns = row.find_all('td')
            
            if len(columns) > 0:
                rank = columns[0].text.strip()
                summ_name = columns[1].find('span').text
                lp = columns[3].find('span').text
                leaderboard.append({'rank': rank, 'player': summ_name, 'lp': lp})
        
        return leaderboard[:num_players]

def main():
    parser = OptionParser()

    parser.add_option('-n', '--num_players', dest='num_players', default=10, type='int', help='Number of players to display')
    parser.add_option('-s', '--start', dest='start', default=0, type='int', help='Start index of the leaderboard')
    (options, args) = parser.parse_args()

    if options.num_players < 1:
        print('Number of players must be greater than 0')
        exit(1)
    
    if options.start < 0:
        print('Start index must be greater than 0')
        exit(1)
    
    leaderboard = get_leaderboard(options.num_players, options.start)
    for player in leaderboard:
        print(player['rank'], player['player'], player['lp'])


if __name__ == '__main__': 
    main()
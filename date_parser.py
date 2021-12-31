from bs4 import BeautifulSoup
import requests

NUMBERS = {'0': '\u0030\ufe0f\u20e3', '1': '\u0031\ufe0f\u20e3', '2': '\u0032\ufe0f\u20e3', '3': '\u0033\ufe0f\u20e3',
           '4': '\u0034\ufe0f\u20e3', '5': '\u0035\ufe0f\u20e3', '6': '\u0036\ufe0f\u20e3', '7': '\u0037\ufe0f\u20e3',
           '8': '\u0038\ufe0f\u20e3', '9': '\u0039\ufe0f\u20e3'}

COUNTRIES = {'Испанская': '\U0001F1EA\U0001F1F8', 'Итальянская': '\U0001F1EE\U0001F1F9',
             'Французская': '\U0001F1EB\U0001F1F7', 'Эредивизи': '\U0001F1F3\U0001F1F1',
             'Немецкая': '\U0001F1E9\U0001F1EA', 'Российская': '\U0001F1F7\U0001F1FA',
             'Примейра': '\U0001F1F5\U0001F1F9', 'Лига': '\U0001F3C6',
             'Английская': '\U0001F3F4\U000E0067\U000E0062\U000E0065\U000E006E\U000E0067\U000E007F'}

REQUIRED_LENGTH = 8
MAX_DAY_IN_MONTH = 31
MONTH_IN_YEAR = 12


class DateParser:
    def __init__(self, date):
        self.__soup = self.get_soup(date)
        self.__matches = self.get_matches()
        self.__leagues = self.add_emoji(self.get_leagues())
        self.__messages = self.get_messages(self.__matches, self.__leagues)

    @property
    def soup(self):
        return self.__soup

    @property
    def matches(self):
        return self.__matches

    @property
    def leagues(self):
        return self.__leagues

    @property
    def messages(self):
        return self.__messages

    def get_soup(self, date):
        """ Returns the html text of the page """

        url = 'http://football24online.com/matches~date=' + date
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                   '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup

    def get_leagues(self):
        """ Returns an array of leagues matches for a specific date """

        leagues = self.__soup.findAll('td', class_="matches-table-head")
        leagues = [leagues[i].text for i in range(len(leagues))]
        leagues = [i.replace('\t', '').replace('\n', '') for i in leagues]
        leagues = [i[:-10] for i in leagues]
        return leagues

    def get_matches(self):
        """ Returns an array of matches for a specific date """

        leagues = self.get_leagues()
        data = self.__soup.findAll('td')
        data = [data[i].text for i in range(len(data))]
        data = [i.replace('\t', '').replace('\n', '') for i in data]
        data = list(map(lambda x: x[:-10] if x[:-10] in leagues else x, data))
        matches = []
        if not leagues:
            return matches
        data_index = 0
        leagues_index = 0
        current_league = ''
        while True:
            if data[data_index] == leagues[leagues_index]:
                data_index += 6
                current_league = leagues[leagues_index]
                if leagues_index != len(leagues) - 1:
                    leagues_index += 1
            elif data[data_index] == '':
                break
            else:
                match = Match(current_league, data[data_index], data[data_index + 1],
                              data[data_index + 2], data[data_index + 3], data[data_index + 4])
                matches.append(match)
                data_index += 5
        return matches

    def add_emoji(self, leagues):
        """ Adds emoji for leagues """

        for index, item in enumerate(leagues, start=0):
            flag = COUNTRIES.get(item.split(' ')[0])
            if not flag:
                flag = ''
            leagues[index] = ' '.join(['\u26bd', flag, item])
        return leagues

    def get_messages(self, matches, leagues):
        """ Returns an array of messages to be sent to the bot """

        result = []
        if len(leagues) == 0:
            return result
        i = 0
        j = 0
        while True:
            message = matches[i].league
            while matches[i].league == leagues[j]:
                message += '\n\t' + matches[i].__str__()
                if i + 1 == len(matches):
                    result.append(message)
                    return result
                i += 1
            result.append(message)
            j += 1


class Match:
    """ Describes the match, has such fields as match league, time, match status, host team,
        game score and guest team """

    def __init__(self, league, time, status, hosts, score, guests):
        if not isinstance(league, str) or not isinstance(time, str) or not isinstance(status, str) or \
                not isinstance(score, str) or not isinstance(guests, str):
            raise TypeError("Invalid type of arguments!")
        flag = COUNTRIES.get(league.split(' ')[0])
        if not flag:
            flag = ''
        self.__league = ' '.join(['\u26bd', flag, league])
        self.__time = time
        self.__status = status
        self.__hosts = ''.join(('*', hosts, '*'))
        self.__score = "".join([NUMBERS.get(ch, ch) for ch in score])
        self.__guests = ''.join(('*', guests, '*'))

    @property
    def league(self):
        return self.__league

    @property
    def time(self):
        return self.__time

    @property
    def status(self):
        return self.__status

    @property
    def hosts(self):
        return self.__hosts

    @property
    def score(self):
        return self.__score

    @property
    def guests(self):
        return self.__guests

    def __str__(self):
        return f'{self.__time}\t{self.__hosts}\t{self.__score}\t{self.__guests}\t\n\t{self.__status}'


def check_date(message):
    """ Checks the correctness of the date, if everything is good – returns True, if not - False """

    date = ''.join(message)
    if len(date) != REQUIRED_LENGTH:
        return False
    for i in range(len(date)):
        if not date[i].isdigit():
            return False
    if int(date[:2]) > MAX_DAY_IN_MONTH or int(date[2:4]) > MONTH_IN_YEAR:
        return False
    return True

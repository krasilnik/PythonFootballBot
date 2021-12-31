import re

from bs4 import BeautifulSoup
import requests


class TeamParser:
    def __init__(self, team):

        self.__soupTeam = self.get_soup_team_link(team)
        self.__soupCalendar = self.get_soup_calendar()
        self.__soupStats = self.get_soup_stats()
        self.__soupNews = self.get_soup_news()
        self.__calendar = self.get_calendar()
        self.__stats = self.get_stats()
        self.__news = self.get_news()
        self.__info = self.get_info()

    @property
    def info(self):
        return self.__info

    @property
    def soup_team(self):
        return self.__soupTeam

    @property
    def soup_calendar(self):
        return self.__soupCalendar

    @property
    def soup_stats(self):
        return self.__soupStats

    @property
    def soup_news(self):
        return self.__soupNews

    @property
    def calendar(self):
        return self.__calendar

    @property
    def stats(self):
        return self.__stats

    @property
    def news(self):
        return self.__news

    def get_soup_team_link(self, team):
        """ Returns the html text of the page """

        url = 'http://football24online.com/teams'
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                                 '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        team_title = soup.find_all("a", text=team)
        for link in team_title:
            team_link = link.get("href")
            return team_link

    def get_soup_calendar(self):

        url = self.__soupTeam + "/calendar"

        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                                 '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup

    def get_soup_stats(self):
        url = self.__soupTeam + "/statistic"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                                 '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup

    def get_soup_news(self):
        url = self.__soupTeam + "/news"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                                 '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup

    def get_calendar(self):
        calendar = self.__soupCalendar.find("table", class_="block celled-table matches-table").find_all("a")
        calendar_date1 = self.__soupCalendar.find("table", class_="block celled-table matches-table").find_all("td", text=re.compile("21 "))
        calendar_date1 = [calendar_date1[i].text for i in range(len(calendar_date1))]
        calendar_date1 = [i.replace('\n', '') for i in calendar_date1]
        calendar_date2 = self.__soupCalendar.find("table", class_="block celled-table matches-table").find_all("td", text=re.compile("22 "))
        calendar_date2 = [calendar_date2[i].text for i in range(len(calendar_date2))]
        calendar_date2 = [i.replace('\n', '') for i in calendar_date2]
        calendar_date = calendar_date1 + calendar_date2
        calendar = [calendar[i].text for i in range(len(calendar))]
        calendar = [i.replace('\n', '') for i in calendar]
        calendar_new = []
        for i in range(0, len(calendar), 3):
            calendar_new.append(calendar[i] + " | " + calendar[i+1] + " | " + calendar[i + 2])
        a = int(len(calendar_new)/2-3)
        b = int(len(calendar_new)/2+3)
        b1 = int(len(calendar_date)/2+3)
        a1 = int(len(calendar_date)/2-3)
        calendar_date = calendar_date[a1:b1]
        calendar = calendar_new[a:b]
        calendar = ["| " + x + " | " + y + " |" for x, y in zip(calendar_date, calendar)]
        calendar.insert(0, "Актуальные матчи:")
        return calendar

    def get_stats(self):
        stats = self.__soupStats.find("table", class_="block celled-table team-statistic-short").findAll("td")
        stats = [stats[i].text for i in range(len(stats))]
        stats = [i.replace('\n', '') for i in stats]
        stats_new = []
        for i in range(0, len(stats), 2):
            stats_new.append(stats[i] + ": " + stats[i+1])
        stats_new.insert(0, "Актуальная статистика:")
        return stats_new

    def get_news(self):
        news = self.__soupNews.find("div", class_="column-left").find("div", class_="block").find_all("a", class_="title-link")
        news_links = [news[i].get("href") for i in range(len(news))]
        news_links = news_links[2:]
        news = [news[i].text for i in range(len(news))]
        news = news[2:5]
        news = [x + " " + y for x, y in zip(news, news_links)]
        news.insert(0, "Актуальные новости:")
        return news

    def get_info(self):
        return TeamParser.get_news(self), TeamParser.get_stats(self), TeamParser.get_calendar(self)


def check_team(team):
    url = 'http://football24online.com/teams'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    team_title = soup.find_all("a", text=team)
    if not team_title:
        return False

    for link in team_title:
        if link.text == team:
            return True



#
# p = TeamParser("Реал Мадрид")
#
#
# print(p.get_info())






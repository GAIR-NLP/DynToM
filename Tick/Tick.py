class Tick:
    def __init__(self):
        self.gameDay = 0
        self.gameMonth = 0
        self.gameYear = 0
        self.gameSeason = "Winter"
        self.gameHour = 0
        self.gameMinute = 0
        self.gameSecond = 0

    def update_time(self, time_str):
        date, season, clock = time_str.split('-')
        self.gameDay, self.gameMonth, self.gameYear = map(int, date.split('/'))
        self.gameSeason = season
        self.gameHour, self.gameMinute, self.gameSecond = map(int, clock.split(':'))

    def get_time(self):
        return {
            'gameDay': self.gameDay,
            'gameMonth': self.gameMonth,
            'gameYear': self.gameYear,
            'gameSeason': self.gameSeason,
            'gameHour': self.gameHour,
            'gameMinute': self.gameMinute,
            'gameSecond': self.gameSecond
        }
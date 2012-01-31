from datetime import date

from flask import render_template


class Calendar:
    def __init__(self, month=None, year=None):
        if month is None or year is None:
            today = date.today()
            if month is None:
                month = today.month
            if year is None:
                year = today.year
        self._month = int(month)
        self._year = int(year)
    
    def build(self):
        """ Build html calendar based on given month and year """
        # get integer values for months and year
        # prev_ and next_ values used for links
        month = self._month
        year = self._year
        prev_month = month - 1
        prev_year = year
        next_month = month + 1
        next_year = year
        if month == 1:
            prev_month = 12
            prev_year -= 1
        elif month == 12:
            next_month = 1
            next_year += 1
        
        # get month names for display
        months = ('January', 'February', 'March', 'April', 'May', 
                  'June', 'July', 'August', 'September', 'October', 
                  'November', 'December')
        month_name = months[month - 1]
        prev_month_name = months[prev_month - 1]
        next_month_name = months[next_month - 1]
        
        # get weekday (1-7 with Sunday as 7) for the first day of month
        # if Sunday set weekday to 0
        first_weekday = date(year, month, 1).isoweekday()
        if first_weekday == 7:
            first_weekday = 0
            
        num_days = self.days_in_month(month, year)
        prev_num_days = self.days_in_month(prev_month, prev_year)
        
        # calculate day to show for the previous month
        # if prev_month_start is more than number of days in month
        # then the first day of month is on Sunday
        prev_month_start = prev_num_days + 1
        if first_weekday > 0:
            prev_month_start = prev_num_days - first_weekday + 1
        next_month_start = 1
        
        cal_day = 1
        html = ''
        week = 1
        while cal_day <= num_days:
            html += '<div class="week">'
            for day in range (0, 7):
                html += '<div class="day'
                # first day of the week has extra class
                if day == 0:
                    html += ' sunday'
                if (day >= first_weekday or week > 1) and cal_day <= num_days:
                    html += ' active">' + str(cal_day)
                    cal_day += 1
                elif prev_month_start <= prev_num_days:
                    html += '">' + str(prev_month_start)
                    prev_month_start += 1
                else:
                    html += '">' + str(next_month_start)
                    next_month_start += 1
                html += '</div>'
            html += '</div>'
            week += 1
        
        return render_template('cal', cal_html=html, month=self._month,
                               year=self._year, prev_year=prev_year,
                               next_year=next_year, prev_month=prev_month, 
                               next_month=next_month, month_name=month_name, 
                               prev_month_name=prev_month_name, 
                               next_month_name=next_month_name)
        
    def days_in_month(self, month=None, year=None):
        """ Calculate number of days in given month """
        if month is None or year is None:
            num = 0
        else:
            next_month = month + 1
            next_year = year
            if month == 12:
                next_month = 1
                next_year = year + 1
            num = (date(next_year, next_month, 1) - date(year, month, 1)).days
        return num
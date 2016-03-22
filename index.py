fom datetime import date

from flask import Flask, render_template
app = Flask(__name__)

from lib.calendar import Calendar


@app.route('/<month>/<year>/')
def main(month='1', year='2012'):
    # builds calendar using Python dates
    calendar = Calendar(month, year)
    cal_html = calendar.build()

    # provide values for use in building the Javascript calendar
    month = int(month)
    months = (
        'January', 'February', 'March', 'April',
        'May', 'June', 'July', 'August',
        'September', 'October', 'November', 'December'
    )
    month_name = months[month - 1]
    prev_year = int(year)
    next_year = int(year)

    # used for switching between months (links)
    prev_month = month - 1
    next_month = month + 1
    if month == 1:
        prev_month = 12
        prev_year -= 1
    elif month == 12:
        next_month = 1
        next_year += 1

    prev_month_name = months[prev_month - 1]
    next_month_name = months[next_month - 1]

    # Javascript calculates dates differently, so subtract 1
    month -= 1

    return render_template('calendar',
                           year=year, month=month,
                           month_name=month_name,
                           prev_month=prev_month,
                           prev_month_name=prev_month_name,
                           next_month=next_month, next_year=next_year,
                           next_month_name=next_month_name,
                           cal_html=cal_html)


if __name__ == "__main__":
    app.run(debug=True)

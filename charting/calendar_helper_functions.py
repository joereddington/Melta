from icalendar import Calendar, Event

def add_event(cal, summary, start, end):
        event = Event()
        event.add('summary', summary)
        event.add('dtstart', start)
        event.add('dtend', end)
        event.add('dtstamp', end)
        event['uid'] = summary+str(start)+str(end)
        event.add('priority', 5)

        cal.add_component(event)


def get_cal():
        cal = Calendar()
        cal.add('prodid', '-//My calendar product//mxm.dk//')
        cal.add('version', '2.0')
        return cal


def write_cal(outfilename, cal):
        f = open(outfilename, 'wb')
        f.write(cal.to_ical())
        f.close()



def get_content(infilename):
        with open(infilename) as f:
                content = f.readlines()
        return content


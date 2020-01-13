from bs4 import BeautifulSoup, NavigableString, Tag
import requests
import datetime
import csv

MONTHS = ["January","February","March","April","May","June","July","August","September","October","November","December"]

def get_table():
    url = "https://en.wikipedia.org/wiki/2019_in_spaceflight#Orbital_launches"
    req = requests.get(url)
    doc_tree = BeautifulSoup(req.text, "html.parser")

    for header in doc_tree.find_all('h2'):
        header_text = header.get_text(strip=True).strip()
        if header_text.find('Orbital launches') > -1:
            nextNode = header
            cnt = 0
            while True:
                nextNode = nextNode.nextSibling
                if nextNode is None:
                    break
                if isinstance(nextNode, Tag):
                    if nextNode.name == "h2":
                        break
                    cnt += 1
                    if cnt == 2:
                        return nextNode
            print(cnt)
    return None

def find_string_has_month(string):
    for i in range(len(MONTHS)):
        if MONTHS[i] in string:
            return i+1
    return -1

def find_td_has_rowspan(tag):
    return tag.name == "td" and tag.has_attr('rowspan')

def judge_successful_row(row_item):
    cols = row_item.find_all("td")
    for col in cols:
        col_text = col.get_text(strip=True).lower()
        if col_text.find("successful") == 0 or col_text.find("operational") == 0 or col_text.find("en route") == 0:
            return True
    return False

def get_launches_groupby_date():
    table = get_table()
    res_dict = dict()
    if table != None:
        items = table.find_all("tr")
        flag = False
        launch_rows, cnt, successes = 0, 0, 0
        curr_date = None
        for item in items:
            if len(item.find_all("table", class_="navbox hlist")) == 0:
                if not flag:
                    col_with_rowspan = item.find_all(find_td_has_rowspan)
                    if len(col_with_rowspan) >= 1:
                        string = col_with_rowspan[0].get_text(strip=True)
                        curr_month = find_string_has_month(string)
                        if curr_month > 0:
                            launch_rows = int(col_with_rowspan[0].attrs['rowspan'])
                            cnt = 1
                            curr_day = int(string.split()[0])
                            curr_date = datetime.datetime(2019, curr_month, curr_day)
                            flag = True
                            if judge_successful_row(item):
                                successes += 1
                else:
                    if judge_successful_row(item):
                        successes += 1
                    cnt += 1
                    if cnt == launch_rows:
                        if successes > 0:
                            date_str = curr_date.isoformat()
                            res_dict[date_str] = res_dict.get(date_str, 0) + 1
                        flag = False
                        curr_date = None
                        launch_rows, cnt, successes = 0, 0, 0
    return res_dict

def purse_output(res_dict):
    with open("gma_output.csv", "w", newline='') as csv_file:
        fieldnames = ['date', 'value']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        date = datetime.datetime(2019, 1, 1)
        for i in range(365):
            date_str = date.isoformat()
            writer.writerow({
                'date': date_str + "+00:00", 
                'value': res_dict.get(date_str, 0)
            })
            date = date + datetime.timedelta(days=1)

if __name__ == "__main__":
    res = get_launches_groupby_date()
    purse_output(res)
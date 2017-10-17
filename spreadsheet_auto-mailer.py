import gspread
import pprint
from oauth2client.service_account import ServiceAccountCredentials


def setup_connection(spreadsheet):
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    worksheet = client.open(spreadsheet).sheet1
    return worksheet


def send_email(is_sent, is_passing):
    if not is_sent:
        print("sending email...")
        if is_passing:
            print("you passed! congratulations :)")
        else:
            print("sorry, but you didn't pass yet! We'd really love to see you at the MakerSpace, so make sure to try again!")
            return True
    else:
        print("email already sent.")
        return False


def main():
    worksheet = setup_connection('CoMotion Quiz Test Automation')
    rows = worksheet.get_all_values()
    index = 0
    for row in rows:
        index = index + 1
        if (row[4] == "FALSE"):
            is_passing = (float(row[0])/30 > 0.8)
            is_sent = False
            if (send_email(is_sent, is_passing)):
                worksheet.update_acell('E' + str(index), "TRUE") # Updates the cell to reflect true

            else:
                print("these are not the droids you\'re looking for...")


main()

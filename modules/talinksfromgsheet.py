from oauth2client.service_account import ServiceAccountCredentials
import gspread
import validators
import time


def proccessGoogleDriveData(wp_links_info2: dict) -> bool:
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        "wp-and-gsheets-f367b7bccab9.json",
        scopes)  #access the json key you downloaded earlier
    file = gspread.authorize(
        credentials)  # authenticate the JSON key with gspread

    try:
        sheet = file.open('text_file_TA')  #open sheet
        sheet = sheet.sheet1

        rows_range = sheet.row_count
        rows_range = 12
        result_str = ''

        print("\n\n ++ ** START ** ++ \n")
        result_str += "\n\n ++ ** START ** ++ \n"
        for x in range(rows_range):

            rowRangeString = 'A' + str(x + 1) + ':B' + str(x + 1)
            row_cells = sheet.range(rowRangeString)
            rowName = "ROW " + str(x + 1)
            rowStr = ""

            foundURI = False
            flagCellToHighlight = False
            for rcell in row_cells:

                uri = str(rcell.value)
                validURI = validators.url(uri)

                if (rcell.value != '' and validURI == True):
                    rowStr += " " + rcell.value
                    flagValue = row_cells[1].value
                    flagRowIndex = x
                    foundURI = True

                    # compare WP links to on in the sheet
                    # print(wp_links_info['74']['data'])
                    wpl = dict()
                    for wpl in wp_links_info2.values():
                        # print(wpl['data'])
                        # print(wpl['post-id'])
                        if (uri == wpl['data']['permalink']):
                            result_str += "\n Go ride bike! \n"
                            sheet.update_acell("B" + str(flagRowIndex + 1),
                                               "1")
                            sheet.format(
                                "A" + str(flagRowIndex + 1), {
                                    "backgroundColor": {
                                        "red": 0.6,
                                        "green": 1.0,
                                        "blue": 0.4
                                    }
                                })
                    str_row = "ROW: {name} >> {val} [flag: {flag}] \n".format(
                        name=rowName, val=rowStr, flag=row_cells[1].value)
                    result_str += str_row

            if (rows_range == x + 1):
                print(" ++ ** DONE ** ++ \n\n")
                return result_str
            time.sleep(0.01)

    except IndexError:
        print("NOTICE: Bad list index!" + " Omg! Adam gonna love this one.\n")
        return False

    except gspread.exceptions.APIError as RESOURCE_EXHAUSTED:
        print(
            "NOTICE: Api error occurred! RESOURCE_EXHAUSTED " +
            "Give it a minute or two or 15. Then and only then, Adam should be allowed to be bothered with this!\n"
        )
        print(sheet['message'])
        return False

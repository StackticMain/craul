import urllib2, json
import gdata.spreadsheet.service

def main():

    resp_obj  = urllib2.urlopen("http://www.masseyratings.com/ratejson.php?s=268790")
    response = resp_obj.read()

    # Get the JSON data into a json object
    j = json.loads(response)
    print "::LOG::Just loaded response into JSON"
    # Parse json object for (k,v) pairs such that
    teams = []
    ilinks = []
    for item in j["DI"]:
        teams.append(item[0][0])
        ilinks.append(item[0][2])
    print "::LOG::Extracting the links from JSON"

    upd_links = []
    for item in ilinks:
        upd_links.append("http://www.masseyratings.com/" + item)
    print "::LOG::Concatentating domain with links"


    print "::LOG::Building JSON links"
    # Build json urls list by adding 'json' to urls
    links = []
    for item in upd_links:
        jlinks = item[:33] + 'json' + item[33:]
        links.append(jlinks)
    print "::LOG::Built JSON links"

    # Build list of responses to calling json urls
    # This process takes 17 seconds approx
    response_list = []
    for url in links:
        resp = urllib2.urlopen(url)
        response_list.append(json.loads(resp.read()))

    all_scores = []
    for item in response_list:
        all_scores.append(item["DI"])

    print all_scores

    stats = zip(teams, all_scores)

    result = []
    for (a,b) in enumerate(stats):
        print get_scores(a,b)
        result.append(get_scores(a,b))

    for items in result:
        print items

    result_sorted = []
    for items in result:
        for item in items:
            result_sorted.append(item)


    email = '' # enter email address here
    password = '' # enter password here'
    weight = '180'
    # Find this value in the url with 'key=XXX' and copy XXX below
    spreadsheet_key = '' #enter spreadsheet key here from URL of the google spreadsheet
    # All spreadsheets have worksheets. I think worksheet #1 by default always
    # has a value of 'od6'
    worksheet_id = 'od6'

    spr_client = gdata.spreadsheet.service.SpreadsheetsService()
    spr_client.email = email
    spr_client.password = password
    spr_client.source = 'Example Spreadsheet Writing Application'
    spr_client.ProgrammaticLogin()

    # Prepare the dictionary to write
    dict = {}
    for item in range(len(result_sorted)):
        dict[item] = { "date":result_sorted[item][0],
                       "host":result_sorted[item][1],
                       "opponent":result_sorted[item][2],
                       "host_outcome":result_sorted[item][3],
                       "host_score":result_sorted[item][4],
                       "opponent_score":result_sorted[item][5]}
    # print dict

    for i in range(len(dict)):
        entry = spr_client.InsertRow(dict[i], spreadsheet_key, worksheet_id)
        if isinstance(entry, gdata.spreadsheet.SpreadsheetsList):
          print "Insert row succeeded."
        else:
          print "Insert row failed."
          # K Camp - Lil Bit
          # Ace hood - Pain
          # Rich Gang/ Juvenile - Sho me love
    return 1

def get_scores(a_data, b_data):
    scores = []
    for game_result in b_data:
        if(game_result[7][0]==unicode('W') or game_result[7][0]==unicode('L')):
            date = game_result[1],
            opponent = game_result[3][0],
            host_outcome = game_result[7][0],
            host_score = game_result[9],
            opponent_score = game_result[10]
            scores.append([date, a_data, opponent, host_outcome, host_score, opponent_score])


if __name__ == '__main__':
    main()
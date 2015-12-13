import requests
import json
import os

TWFY_KEY = 'GWLD65EufaCzDMwrRyGYmsE7'


def distance_meaning(score):
    score = float(score)
    desc = "unknown about";
    if score > 0.95 and score <= 1.0:
        desc = "very strongly against"
    elif score > 0.85:
        desc = "strongly against"
    elif score > 0.6:
        desc = "moderately against"
    elif score > 0.4:
        desc = "a mixture of for and against"
    elif score > 0.15:
        desc = "moderately for"
    elif score > 0.05:
        desc = "strongly for"
    elif score >= 0.0:
        desc = "very strongly for"

    return desc


def mp_info(mp_id):
    url = 'http://www.theyworkforyou.com/api/getMPInfo?id=%s&output=js&key=%s' % (mp_id, TWFY_KEY)
    r = requests.get(url)
    j = r.json()
    print(j)

    import re

    policies = {
        996: "a transparent Parliament",
        811: "a smoking ban",
        1051: "introducing ID cards",
        363: "introducing foundation hospitals",
        1052: "university tuition fees",
        1053: "Labour's anti-terrorism laws",
        1049: "the Iraq war",
        984: "replacing Trident",
        1050: "the hunting ban",
        826: "equal gay rights",
        1030: "laws to stop climate change",
        1074: "greater autonomy for schools",
        1071: "allowing ministers to intervene in inquests",
        1079: "removing hereditary peers from the House of Lords",
        1087: "a stricter asylum system",
        1065: "more EU integration",
        1110: "increasing the rate of VAT",
        1084: "a more proportional system for electing MPs",
        1124: "automatic enrolment in occupational pensions",
        837: "a wholly elected House of Lords",
        975: "an investigation into the Iraq war",
        1132: "raising England's undergraduate tuition fee cap to 9,000 per year",
        1109: "encouraging occupational pensions",
    }

    votes = {}

    for item in j:
        if item.startswith('public_whip_dreammp'):

            key = item.replace('public_whip_dreammp', '')
            vote_id = re.findall(r'\d+', key)[0]
            print(key, vote_id)

            key = key.replace(vote_id + '_', '')

            if vote_id not in votes:
                votes[vote_id] = {}
            votes[vote_id][key] = j[item]

            if int(vote_id) in policies:
                votes[vote_id]['name'] = policies[int(vote_id)]
                # else:
                # print vote_id

    for vote in votes:
        v = distance_meaning(votes[vote]['distance'])
        votes[vote]['vote'] = v

    photo = None
    import os.path

    if os.path.exists('core/static/images/%s.jpg' % mp_id):
        photo = '%s.jpg' % mp_id
    if os.path.exists('core/static/images/%s.jpeg' % mp_id):
        photo = '%s.jpeg' % mp_id
    if os.path.exists('core/static/images/%s.png' % mp_id):
        photo = '%s.png' % mp_id

    return {
        'name': j['name'] if 'name' in j else "?",
        'party': j['party'] if 'party' in j else "Unknown party",
        'photo': photo,
        'votes': votes
    }


def get_all_mps_ids():
    """
    Will read the json file with all the mp names
    :return: None
    """
    f = open(os.path.join('data', 'mps.json'))
    with f as data_file:
        data = json.load(data_file)

    for item in data:
        res = item['person_id']
        print(res)
        get_mp_info(res)


def get_mp_info(mp_id):
    """
    gets the mp info from the site and writes into a file
    :param mp_id:
    :return: None
    """

    url = 'http://www.theyworkforyou.com/api/getMPInfo?id=%s&output=js&key=%s' % (mp_id, TWFY_KEY)
    r = requests.get(url)
    j = r.json()
    print(j)

    # write into file
    open_file = open(os.path.join('data', 'mps_info.json'), 'a')
    with open_file as outfile:
        d_value = dict({mp_id: j})
        json.dump(d_value, outfile)
        open_file.write(os.linesep)


def get_mp_json_from_file(mp_id):
    """
    get the json file of a specific person
    :param mp_id: the person_id
    :return: json string
    """
    # read json dump file
    fname = open(os.path.join('data', 'mps_info.json'))

    data = []
    with fname as f:
        for line in f:
            data.append(json.loads(line))

    for value in data:
        for key, value in value.items():
            # print(key, value)
            if key == '10133':
                print(value)
                return value


if __name__ == "__main__":
    # get_all_mps_ids()
    get_mp_json_from_file(10133)
    # mp_info(10133)


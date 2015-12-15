import requests
import json
import os
import re

TWFY_KEY = 'GWLD65EufaCzDMwrRyGYmsE7'

policies = {
    363: "introducing foundation hospitals",
    810: "greater regulation of gambling",
    811: "smoking bans",
    826: "equal gay rights",
    837: "a wholly elected House of Lords",
    856: "Parliamentary scrutiny — Reduce",
    975: "an investigation into the Iraq war",
    984: "replacing Trident with a new nuclear weapons system",
    996: "a transparent Parliament",
    1027: "a referendum on the UK's membership of the EU",
    1030: "measures to prevent climate change",
    1049: "the Iraq war",
    1050: "the hunting ban",
    1051: "introducing ID cards",
    1052: "university tuition fees",
    1053: "Labour's anti-terrorism laws",
    1065: "more EU integration",
    1071: "allowing ministers to intervene in inquests",
    1074: "greater autonomy for schools",
    1077: "Extradition — reciprocal between UK and US",
    1079: "removing hereditary peers from the House of Lords",
    1080: "Supports Government Budgets",
    1084: "a more proportional system for electing MPs",
    1087: "a stricter asylum system",
    1105: "the privatisation of Royal Mail",
    1109: "encouraging occupational pensions",
    1110: "increasing the rate of VAT",
    1113: "an equal number of electors per parliamentary constituency",
    1120: "capping civil service redundancy payments",
    1124: "automatic enrolment in occupational pensions",
    1132: "raising England's undergraduate tuition fee cap to £9,000 per year",
    1136: "fewer MPs in the House of Commons",
    6667: "the policies included in the 2010 Conservative - Liberal Democrat Coalition Agreement",
    6670: "a reduction in spending on welfare benefits",
    6671: "reducing central government funding of local government",
    6672: "reducing housing benefit for social tenants deemed to have excess bedrooms (which Labour describe as the 'bedroom tax')",
    6673: "paying higher benefits over longer periods for those unable to work due to illness or disability",
    6674: "raising welfare benefits at least in line with prices",
    6676: "reforming the NHS so GPs buy services on behalf of their patients",
    6677: "restricting the provision of services to private patients by the NHS",
    6678: "greater restrictions on campaigning by third parties, such as charities, during elections",
    6679: "reducing the rate of corporation tax",
    6680: "raising the threshold at which people start to pay income tax",
    6681: "increasing the tax rate applied to income over £150,000",
    6682: "ending financial support for some 16-19 year olds in training and further education",
    6683: "local councils keeping money raised from taxes on business premises in their areas",
    6684: "making local councils responsible for helping those in financial need afford their council tax and reducing the amount spent on such support",
    6685: "a banker's bonus tax",
    6686: "allowing marriage between two people of same sex",
    6687: "academy schools",
    6688: "use of UK military forces in combat operations overseas",
    6690: "measures to reduce tax avoidance",
    6691: "stronger tax incentives for companies to invest in assets",
    6692: "slowing the rise in rail fares",
    6693: "lower taxes on fuel for motor vehicles",
    6694: "higher taxes on alcoholic drinks",
    6695: "more powers for local councils",
    6696: "the introduction of elected Police and Crime Commissioners",
    6698: "fixed periods between parliamentary elections",
    6699: "higher taxes on plane tickets",
    6697: "selling England's state owned forests",
    6702: "spending public money to create guaranteed jobs for young people who have spent a long time unemployed",
    6703: "laws to promote equality and human rights",
    6704: "financial incentives for low carbon emission electricity generation methods",
    6705: "requiring pub companies to offer pub landlords rent-only leases",
    6706: "strengthening the Military Covenant",
    6707: "restricting the scope of legal aid",
    6708: "transferring more powers to the Welsh Assembly",
    6709: "transferring more powers to the Scottish Parliament",
    6710: "culling badgers to tackle bovine tuberculosis",
    6711: "an annual tax on the value of expensive homes (popularly known as a mansion tax)",
    6715: "allowing national security sensitive evidence to be put before courts in secret sessions",
    6716: "allowing employees to exchange some employment rights for shares in the company they work for",
    6718: "restrictions on fees charged to tenants by letting agents",
    6719: "limits on success fees paid to lawyers in no-win no fee cases",
    6720: "a statutory register of lobbyists",
    6721: "requiring the mass retention of information about communications",
}

# set of all vote ids
vote_set = set()


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
    """
    receives an id, pulls the json object from file and the processes
     the policies and votes
    :param mp_id: String
    :return: json object
    """
    # pulling the json object from file
    j = get_mp_json_from_file(mp_id)

    votes = {}

    for item in j:
        if item.startswith('public_whip_dreammp'):

            key = item.replace('public_whip_dreammp', '')
            vote_id = re.findall(r'\d+', key)[0]
            # vote_set.add(vote_id)
            print(key, vote_id)

            key = key.replace(vote_id + '_', '')

            if vote_id not in votes:
                votes[vote_id] = {}
            votes[vote_id][key] = j[item]

            if int(vote_id) in policies:
                votes[vote_id]['name'] = policies[int(vote_id)]
            else:
                print(vote_id)

    for vote in votes:
        v = distance_meaning(votes[vote]['distance'])
        votes[vote]['vote'] = v

    return {
        'name': j['name'] if 'name' in j else "?",
        'party': j['party'] if 'party' in j else "Unknown party",
        'votes': votes
    }


def get_all_mps_ids():
    """
    Will read the json file with all the mp names
    :return: list of ids
    """
    f = open(os.path.join('data', 'mps.json'))
    with f as data_file:
        data = json.load(data_file)

    for item in data:
        res = item['person_id']
        print(res)
        # get_mp_info(res)

    return data


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
            if int(key) == 10133:
                print(value)
                return value


def write_vote_ids():
    """
    write the list of vote ids to file
    :return: None
    """

    open_file = open(os.path.join('data', 'vote_ids.txt'), 'w')
    open_file.write("\n".join(vote_set))


def find_vote_label():
    """
    find all vote_ids that don't have labels
    :return: None
    """
    input_file = open(os.path.join('data', 'vote_ids.txt'))

    # read vote ids from file
    with input_file as inputs:
        for vote_id in inputs:
            if int(vote_id) not in policies:
                print(vote_id)


if __name__ == "__main__":
    # ids = get_all_mps_ids()
    # get_mp_json_from_file(10133)

    # for id in ids:
    #     mp_info(id)
    mp_info(10133)

    # write_vote_ids()
    # find_vote_label()


#/usr/bin/env python

# This code walks through the "data.json" files of 93rd(1973-1974) congress
# to 115th (2017-2018).
#
# This python code generates congress_data.csv file containing following info
#
# Attributes to a bill:
#   id:               bill ID
#   cosponsoes:       number of cosponsors
#   status:           status of the bill (e.g. enacated, passed, referred etc..)
#   committee:        the most related committee (e.g. House Judiciary)
#   subjects:         subject of the bill (e.g. Immigration)
#   congress:         congress (e.g. 115th)
#   billType:         type of a bill (e.g. s, hr, hres etc.)
#   state:            the state of which the sponsor of the bill came from
#   relatedbills:     number of related bills
#
#
# Source of data: ProPublica
#
# 1) Download bulk and raw data from the follwoing link:
#    https://www.propublica.org/datastore/dataset/congressional-data-bulk-legislation-bills
#
# 2) Unzip all zip file in a directory (e.g. 115.zip into ./data/115/)
#
# 3) Run this script in ./data directory

import os
import json
import csv
from collections import Counter

billid = []; cosponsors = []; sponsorName = []; sponsorTitle = []
status = []; committee = []
state = []; typesponsor = []
subjects1 = []; subject_prim = []; subject_scnd = []
relatedbills = []
congress = []; billType = []

def Appending(item):
    if (str(type(item)) == "<type NoneType>" or str(type(item)) == "<class 'NoneType'>"):
        temp1 = 'N/A'
    else:
        temp1 = item

    return temp1

# Writing all the data files into csv file.
print ("Writing data into files...")
filename1 = 'congress_data.csv'
with open(filename1, 'w', newline='') as csvfile:
    wr = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    wr.writerow(['Congress'] + ['Bill_ID'] + ['Bill_Type'] + ['State_sponsor'] + ['Sponsor_name'] +
                ['Sponsor_title'] + ['Num_cosponsors'] + ['Num_related_bills' ] + ['Committee'] +
                ['Subject_top_term'] + ['Primary_subject'] + ['Secondary_subject'] + ['Status'] )
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.json'):
                filename = os.path.join(root, file)
                with open(filename) as f:
                    data = json.load(f)
                    if (type(data) == dict):

                        congress.append(Appending(data["congress"]))

                        billType.append(Appending(data["bill_type"]))

                        billid.append(Appending(data["bill_id"]))

                        print ("Collecting information of bill ", data["bill_id"] , "....", end = '')

                        if (Appending(data["sponsor"]) == "N/A"):
                            sponsorName.append("N/A")
                            sponsorTitle.append("N/A")
                            state.append("N/A")
                        else:
                            sponsorName.append(Appending(data["sponsor"]["name"]))
                            sponsorTitle.append(Appending(data["sponsor"]["title"]))
                            state.append(Appending(data["sponsor"]["state"]))

                        if (Appending(data["cosponsors"]) == "N/A"):
                            cosponsors.append(0)
                        else:
                            cosponsors.append(len(data["cosponsors"]))

                        if (Appending(data["related_bills"]) == "N/A"):
                            relatedbills.append(0)
                        else:
                            relatedbills.append(len(data["related_bills"]))

                        if (data["committees"] != []):
                            committee.append(Appending(data["committees"][0]["committee"]))
                        else:
                            committee.append('N/A')

                        subjects1.append(Appending(data["subjects_top_term"]))

                        if (len(data["subjects"]) > 2):
                            subject_prim.append(data["subjects"][0])
                            subject_scnd.append(data["subjects"][1])
                        elif (len(data["subjects"]) > 1):
                            subject_prim.append(data["subjects"][0])
                            subject_scnd.append('N/A')
                        else:
                            subject_prim.append('N/A')
                            subject_scnd.append('N/A')

                        status.append(Appending(data["status"]))

                wr.writerow([str(congress[-1]), str(billid[-1]), str(billType[-1]), str(state[-1]),
                             str(sponsorName[-1]), str(sponsorTitle[-1]), str(cosponsors[-1]), str(relatedbills[-1]),
                             str(committee[-1]), str(subjects1[-1]), str(subject_prim[-1]), str(subject_scnd[-1]), str(status[-1])])
                print("Done")

# Writing summarized data to csv files
statusSet  = list(set(status))
statusSet.sort()
statusDict = dict(Counter(status))
filename2 = 'status_data.csv'
with open(filename2, 'w', newline='') as csvfile:
    wr2 = csv.writer(csvfile, delimiter = ',', quoting = csv.QUOTE_MINIMAL)
    wr2.writerow(['status'] + ['number_of_bills'])
    for i in range(0, len(statusSet)):
        #print statusSet[i] + (50 - len(statusSet[i]))*'-' +  str(statusDict[statusSet[i]])
        wr2.writerow([str(statusSet[i]), str(statusDict[statusSet[i]])])

committeeSet  = list(set(committee))
committeeSet.sort()
committeeDict = dict(Counter(committee))
filename3 = 'committee_data.csv'
with open(filename3, 'w', newline='') as csvfile:
    wr3 = csv.writer(csvfile, delimiter = ',', quoting = csv.QUOTE_MINIMAL)
    wr3.writerow(['committee'] + ['number_of_bills'])
    for i in range(0, len(committeeSet)):
        #print committeeSet[i] + (50 - len(committeeSet[i]))*'-' + str(committeeDict[committeeSet[i]])
        wr3.writerow([str(committeeSet[i]), str(committeeDict[committeeSet[i]])])

subjectsSet  = list(set(subjects1))
subjectsSet.sort()
subjectsDict = dict(Counter(subjects1))
filename4 = 'subject_data.csv'
with open(filename4, 'w', newline='') as csvfile:
    wr4 = csv.writer(csvfile, delimiter = ',', quoting = csv.QUOTE_MINIMAL)
    wr4.writerow(['bill_subject'] + ['number_of_bills'])
    for i in range(0, len(subjectsSet)):
        #print subjectsSet[i] + (50 - len(subjectsSet[i]))*'-' + str(subjectsDict[subjectsSet[i]])
        wr4.writerow([str(subjectsSet[i]), str(subjectsDict[subjectsSet[i]])])

# Print output informations
msg1 = 'All data is written in:'
msg2 = 'Summary of bill status is in:'
msg3 = 'Summary of committees is in:'
msg4 = 'Summary of subjects is in:'
print (msg1 + (40 - len(msg1))*'.' + filename1)
print (msg2 + (40 - len(msg2))*'.' + filename2)
print (msg3 + (40 - len(msg3))*'.' + filename3)
print (msg4 + (40 - len(msg4))*'.' + filename4)

import requests
from dateutil.parser import parse
from datetime import date
import csv
import sys

# For every mission we want to count the number of adults >= 18 and children for both participants and applications
def calculate_age(born):
  today = date.today()
  return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def is_applicant(participant):
  return participant['applicationDecision'] == None

auth_info = {
  'Authorization': 'Basic {}'.format(sys.argv[1]),
  'Content-Type': 'application/json'
}

missions = requests.get('https://lighthousefamilyretreat.focusmissions.com/api/1.0/missions?page=1&pageSize=999999', headers=auth_info).json()
print("Number of missions: {}".format(len(missions)))


with open('report.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',')
    filewriter.writerow(["missionId", "missionName", "missionStatus", 'firstName', 'lastName', 'age', 'email', 'phone', 'dateOfBirth', 'gender', 'address', 'confirmedDateTime', 'participantType', 'donationUrl', 'removedDateTime', 'applicationCompletionDate', 'applicationDecision', 'applicationDecisionDate', 'applicationDecisionComment', 'tripStory', 'fundRaisingGoal', 'hasMetReferencesRequirement', 'hasBackgroundCheck', 'donationBalance', 'isApplicant', 'profileQuestions', 'applicationQuestions', 'references', 'emergencyContacts', 'activityLog'])

    for mission in missions:
        if mission['missionStatus']['name'] != 'Launched':
            continue

        participants = requests.get('https://lighthousefamilyretreat.focusmissions.com/api/1.0/missions/{}/participants?page=1&pageSize=99999'.format(mission['id']), headers=auth_info).json()

        for person in participants:
            if person['applicationDecision'] == None or person['removedDateTime'] != None:
                continue

            age = calculate_age(parse(person['dateOfBirth']))
            if person['address'] != None:
                address = "{}\n{}, {} {}".format((str(person['address']['line1']) + "\n" + str(person['address']['line2'])).strip(), str(person['address']['city']),str(person['address']['province']), str(person['address']['postalCode']))
            else:
                address = "none"

            filewriter.writerow([
                # Mission
                mission['id'],
                mission['name'],
                mission['missionStatus']['name'],
                # Person
                person['firstName'],
                person['lastName'],
                age,
                person['email'],
                person['phone'],
                person['dateOfBirth'],
                person['gender'],
                address,
                person['confirmedDateTime'],
                person['participantType']['name'],
                person['donationUrl'],
                person['removedDateTime'],
                person['applicationCompletionDate'],
                person['applicationDecision']['name'],
                person['applicationDecisionDate'],
                person['applicationDecisionComment'],
                person['tripStory'],
                person['fundRaisingGoal'],
                person['hasMetReferencesRequirement'],
                person['hasBackgroundCheck'],
                person['donationBalance'],
                person['isApplicant'],
                person['profileQuestions'],
                person['applicationQuestions'],
                person['references'],
                person['emergencyContacts'],
                person['activityLog']
            ])

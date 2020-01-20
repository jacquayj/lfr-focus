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

class Participant:

    def __init__(self, api_person, api_mission):
        self.api_person = api_person
        self.api_mission = api_mission

        self.age = calculate_age(parse(api_person['dateOfBirth']))
        if api_person['address'] != None:

            self.address = ""
            if 'line1' in api_person['address'] and api_person['address']['line1'] != None:
                self.address += api_person['address']['line1']
            if 'line2' in api_person['address'] and api_person['address']['line2'] != None:
                self.address += "\n" + api_person['address']['line2']
            if 'line3' in api_person['address'] and api_person['address']['line3'] != None:
                self.address += "\n" + api_person['address']['line3']
            if 'line4' in api_person['address'] and api_person['address']['line4'] != None:
                self.address += "\n" + api_person['address']['line4']
            if 'line5' in api_person['address'] and api_person['address']['line5'] != None:
                self.address += "\n" + api_person['address']['line5']

            self.city = api_person['address']['city']
            self.state = api_person['address']['province']
            self.postal_code = api_person['address']['postalCode']
        else:
            self.address = "none"
            self.city = ""
            self.state = ""
            self.postal_code = ""

        self.csv_row = [
            # Mission
            api_mission['id'],
            api_mission['name'],
            api_mission['missionStatus']['name'],
            # Person
            api_person['firstName'],
            api_person['lastName'],
            self.age,
            api_person['email'],
            api_person['phone'],
            api_person['dateOfBirth'],
            api_person['gender'],
            self.address,
            self.city,
            self.state,
            self.postal_code,
            api_person['confirmedDateTime'],
            api_person['participantType']['name'],
            api_person['donationUrl'],
            api_person['removedDateTime'],
            api_person['applicationCompletionDate'],
            api_person['applicationDecision']['name'],
            api_person['applicationDecisionDate'],
            api_person['applicationDecisionComment'],
            api_person['tripStory'],
            api_person['fundRaisingGoal'],
            api_person['hasMetReferencesRequirement'],
            api_person['hasBackgroundCheck'],
            api_person['donationBalance'],
            api_person['isApplicant'],
            api_person['profileQuestions'],
            api_person['references'],
            api_person['emergencyContacts'],
            api_person['activityLog']
        ]

    def add_answers(self, question_headers):
        answer_cells_to_append = [""] * len(question_headers)

        for q in self.api_person['applicationQuestions']:
            try:
                # Find index of answer cells to add question answer to
                i = question_headers.index(q['name'])
                answer_cells_to_append[i] = q['answers'][0]['value']
            except Exception as e:
                pass
        
        self.csv_row.extend(answer_cells_to_append)
    


# This function fetches participants from the API and joins mission info
def fetch_participants(auth_info):
    participant_list = []
    missions = requests.get('https://lighthousefamilyretreat.focusmissions.com/api/1.0/missions?page=1&pageSize=999999', headers=auth_info).json()

    for mission in missions:
        if mission['missionStatus']['name'] != 'Launched':
            continue

        participants = requests.get('https://lighthousefamilyretreat.focusmissions.com/api/1.0/missions/{}/participants?page=1&pageSize=99999'.format(mission['id']), headers=auth_info).json()

        for api_person in participants:
            if api_person['applicationDecision'] == None or api_person['removedDateTime'] != None:
                continue
            participant_list.append(Participant(api_person, mission))
            #print(api_person['applicationQuestions'])

    return participant_list        

def get_unique_questions(participants):
    u_questions = []

    for p in participants:
        for q in p.api_person['applicationQuestions']:
            if not q['name'] in u_questions:
                u_questions.append(q['name'])
    
    return u_questions


def main():
    if len(sys.argv) <= 1:
        print("Please specifiy API key")
        exit()

    auth_info = {
        'Authorization': 'Basic {}'.format(sys.argv[1]),
        'Content-Type': 'application/json'
    }

    participants = fetch_participants(auth_info)

    with open('report.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',')

        csv_headers_to_append = get_unique_questions(participants)
        csv_headers = ["missionId", "missionName", "missionStatus", 'firstName', 'lastName', 'age', 'email', 'phone', 'dateOfBirth', 'gender', 'address', 'confirmedDateTime', 'participantType', 'donationUrl', 'removedDateTime', 'applicationCompletionDate', 'applicationDecision', 'applicationDecisionDate', 'applicationDecisionComment', 'tripStory', 'fundRaisingGoal', 'hasMetReferencesRequirement', 'hasBackgroundCheck', 'donationBalance', 'isApplicant', 'profileQuestions', 'references', 'emergencyContacts', 'activityLog']
        csv_headers.extend(csv_headers_to_append)

        filewriter.writerow(csv_headers)

        for p in participants:
            p.add_answers(csv_headers_to_append)
            filewriter.writerow(p.csv_row)


if __name__ == '__main__':
    main()
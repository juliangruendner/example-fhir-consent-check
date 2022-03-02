import requests
import json
import base64
import uuid
import csv


def get_next_link(link_elem):
    for elem in link_elem:
        if elem['relation'] == 'next':
            return elem['url']

    return None


def page_through_results_and_collect(resp):

    result_list = []
    next_link = get_next_link(resp.json()['link'])
    result_list = list(map(lambda entry: {"patient": entry['resource']['subject']['reference'].split('/')[1], "code": entry['resource']['code']['coding'][0]['code'], "value": entry['resource']['valueQuantity']['value']}, resp.json()['entry']))

    while next_link:

        resp = requests.get(next_link)
        result_list_temp = list(map(lambda entry: {"patient": entry['resource']['subject']['reference'].split('/')[1], "code": entry['resource']['code']['coding'][0]['code'], "value": entry['resource']['valueQuantity']['value']}, resp.json()['entry']))
        next_link = get_next_link(resp.json()['link'])
        result_list = result_list + result_list_temp

    return result_list

def page_through_results_and_collect_pat_ids(resp):

    result_list = []
    next_link = get_next_link(resp.json()['link'])
    result_list = list(map(lambda entry: entry['resource']['patient']['reference'].split('/')[1], resp.json()['entry']))

    while next_link:

        resp = requests.get(next_link)
        result_list_temp = result_list = list(map(lambda entry: entry['resource']['patient']['reference'].split('/')[1], resp.json()['entry']))
        next_link = get_next_link(resp.json()['link'])
        result_list = result_list + result_list_temp

    return result_list



fhir_base_url = "http://localhost:8081/fhir"




# Query for specific permission

consent_system="urn:oid:2.16.840.1.113883.3.1937.777.24.5.1"
consent_code="2.16.840.1.113883.3.1937.777.24.5.1.32"
consent_permission="deny"
resp = requests.get(f'{fhir_base_url}/Consent?mii-provision-provision-code-type={consent_system}|{consent_code}${consent_permission}')
print(resp.json())

# get list of patients, which have given permission
result_list = page_through_results_and_collect_pat_ids(resp)

# Create patient list for next query
subjects = ",".join(result_list)

print(subjects)

headers = {'Content-Type': "application/x-www-form-urlencoded"}

# Search for data based on consented patients
print("Search for feature = weight (http://loinc.org|29463-7) > 10 for our previously selected patients and print found resources (features)...")
payload = {'code': 'http://loinc.org|29463-7', 'value': 'gt10', 'subject': subjects}
resp = requests.post(f'{fhir_base_url}/Observation/_search', data=payload)

print(resp.json())
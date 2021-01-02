#!/usr/bin/env python3

import xml.etree.ElementTree as ET
from collections import defaultdict

# Returns a patent dictionary containing(UCID, Title, Applicants Names/Last-Names, Inventors Names/Last-Names, Abstract)
def parse_xml(xmlfile):
   # Create the dict which will hold the fetched data
   patent_dict = defaultdict(list)
   
   # Parse the xml tree
   tree = ET.parse(xmlfile)
   # Find the root (<patent-document>)
   root = tree.getroot()

   # Find patent's ucid
   patent_dict["ucid"] = root.attrib.get('ucid')

   # Find invention's title
   for tag in root.iter("invention-title"):
      if (tag.get('lang') == 'EN'):
         patent_dict["title"] = tag.text

   # Find name or last-name for each applicant
   for tag in root.iter("applicant"):
      if (tag.find('addressbook').find('name') != None):
         patent_dict['applicants'].append(tag.find('addressbook').find('name').text)
      elif (tag.find('addressbook').find('last-name') != None):
         patent_dict['applicants_last'].append(tag.find('addressbook').find('last-name').text)

   # Find name or last-name for each inventor
   for tag in root.iter("inventor"):
      if (tag.find('addressbook').find('name') != None):
         patent_dict['inventors'].append(tag.find('addressbook').find('name').text)
      elif (tag.find('addressbook').find('last-name') != None):
         patent_dict['inventors_last'].append(tag.find('addressbook').find('last-name').text)

   return patent_dict

# Formats tha patent dictionary data to Trec and saves them in queries.txt 
def transform_to_trec(patent_dict):
   query_file = open('queries.txt','a')
   query_file.write("<TOP>\n")

   # Prepare UCID tag
   ucid_tag = "<UCID>" + patent_dict['ucid'] + "</UCID>\n"
   # Prepare TITLE tag
   title_tag = "<TITLE>\n" + patent_dict['title'] + "\n</TITLE>\n"
   # Prepare APPLICANTS tag
   applicants_tag = "<APPLICANTS>\n" + ' '.join(map(str, patent_dict['applicants'])) + ' ' + ' '.join(map(str, patent_dict['applicants_last'])) + "\n</APPLICANTS>\n"
   # Prepare INVENTORS tag
   inventors_tag = "<INVENTORS>\n" + ' '.join(map(str, patent_dict['inventors'])) + ' ' + ' '.join(map(str, patent_dict['inventors_last'])) + "\n</INVENTORS>\n"

   query_file.write(ucid_tag)
   query_file.write(title_tag)
   query_file.write(applicants_tag)
   query_file.write(inventors_tag)

   query_file.write("</TOP>\n")
   query_file.close()

# Main
def main():
   # Target PAC Topics
   pac_topics = []

   # Read PAC Topics from MiniCollectionTopics.txt
   topics_file = open('../../Collections/MiniCollectionTopics.txt','r')
   lines = topics_file.readlines()
   topics_file.close()

   # Save all the PAC files names on a list after cleaning them up and appending '.xml' on them  
   for line in lines:
      pac_topics.append(line.replace("\tTest\n",".xml"))

   # Parse each pac xml as trec and save it 
   for file in pac_topics:
      transform_to_trec(parse_xml('../../Collections/PAC_topics/' + file))

if __name__ == "__main__":
   main()

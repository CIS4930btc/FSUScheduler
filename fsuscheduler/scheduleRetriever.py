"""
Name: Thomas Malone
FSU ID: tmm14f
Date: 7/25/2017
Class: CIS 4930
Assignment: Group Project Exam Schedule Scraper
Due Date: 8/4/2017
About this module: Scrapes FSU site for final exam information
"""
from __future__ import print_function
import requests
import string
import re
import sys
import os




def get_exam_info(url):

    main_page = requests.get(url)

    #print (main_page.text)

    dates_text = main_page.text[main_page.text.find(">Final Examination Week</"):main_page.text.find(">Block Examinations</")]
    block_exams_text = main_page.text[main_page.text.find(">Block Examinations</"):main_page.text.find(">Monday/Wednesday/Friday Classes</")]
    mwf_exams_text = main_page.text[main_page.text.find(">Monday/Wednesday/Friday Classes</"):main_page.text.find(">Tuesday/Thursday Classes</")]
    tr_exams_text = main_page.text[main_page.text.find(">Tuesday/Thursday Classes</"):main_page.text.find(">Make-Up Examinations:</")]

    #Date Retrieval Stuff
    dates_list = re.findall(r"[A-Z][a-z]{2}[\.]{0,1} [0-9]{1,2}</", dates_text)

    #Trim fat off date_list
    for i in range(0,len(dates_list)):
    	dates_list[i] = dates_list[i].replace("</", "")

    #Block Exam Stuff
    block_exam_classes = re.findall(r"<td>[A-Z]{3}[^<]+</td>", block_exams_text)
    block_exam_days = re.findall(r"<td>(Monday|Tuesday|Wednesday|Thursday|Friday)", block_exams_text)
    block_exam_times = re.findall(r"<td>[0-9]{1,2}:[0-9][0-9] . [0-9]{1,2}:[0-9][0-9] ....</td>", block_exams_text)
    
    #Trim fat off block_exam_classes
    for i in range(0,len(block_exam_classes)):
    	block_exam_classes[i] = block_exam_classes[i].replace("<td>", "")
    	block_exam_classes[i] = block_exam_classes[i].replace("</td>", "")

    #Adds dates to block_exam_days
    for i in range(0,len(block_exam_days)):
    	block_exam_days[i] = block_exam_days[i].replace("Monday", "Monday, " + dates_list[0])
    	block_exam_days[i] = block_exam_days[i].replace("Tuesday", "Tuesday, " + dates_list[1])
    	block_exam_days[i] = block_exam_days[i].replace("Wednesday", "Wednesday, " + dates_list[2])
    	block_exam_days[i] = block_exam_days[i].replace("Thursday", "Thursday, " + dates_list[3])
    	block_exam_days[i] = block_exam_days[i].replace("Friday", "Friday, " + dates_list[4])

    #Trim fat from block_exam_times
    for i in range(0,len(block_exam_times)):
    	block_exam_times[i] = block_exam_times[i].replace("<td>", "")
    	block_exam_times[i] = block_exam_times[i].replace(u"\u2013", "-")
    	if block_exam_times[i].find(" - ") == -1:
    		block_exam_times[i] = block_exam_times[i].replace("-", "- ")
    	block_exam_times[i] = block_exam_times[i].replace("</td>", "")

    #print (len(block_exam_classes))
    #print (len(block_exam_days))
    #print (len(block_exam_times))

    #Make composite array
    block_exam_info = []
    for i in range(0,len(block_exam_times)):
    	block_exam_info += [[block_exam_classes[i],block_exam_days[i],block_exam_times[i]]]

    #print (block_exam_info)


    #MWF stuff ## re.findall(r"<td>([0-9]{1,2}:[0-9][0-9] [a|p]\.m\.)|(----)</td>", mwf_exams_text) Does not return time or "----", returns time or empty string
    mwf_class_times = re.findall(r"<td>([0-9]{1,2}:[0-9][0-9] [a|p]\.m\.)|(----)</td>", mwf_exams_text)
    mwf_exam_days =  re.findall(r"<td>(Monday|Tuesday|Wednesday|Thursday|Friday)</td>", mwf_exams_text)
    mwf_exam_times =  re.findall(r"<td>[0-9]{1,2}:[0-9][0-9] . [0-9]{1,2}:[0-9][0-9] ....</td>", mwf_exams_text)

    #Trim fat from mwf_exam_times
    for i in range(0,len(mwf_exam_times)):
    	mwf_exam_times[i] = mwf_exam_times[i].replace("<td>", "")
    	mwf_exam_times[i] = mwf_exam_times[i].replace(u"\u2013", "-")
    	if mwf_exam_times[i].find(" - ") == -1:
    		mwf_exam_times[i] = mwf_exam_times[i].replace("-", "- ")
    	mwf_exam_times[i] = mwf_exam_times[i].replace("</td>", "")

    #Adds dates to mwf_exam_days
    for i in range(0,len(mwf_exam_days)):
    	mwf_exam_days[i] = mwf_exam_days[i].replace("Monday", "Monday, " + dates_list[0])
    	mwf_exam_days[i] = mwf_exam_days[i].replace("Tuesday", "Tuesday, " + dates_list[1])
    	mwf_exam_days[i] = mwf_exam_days[i].replace("Wednesday", "Wednesday, " + dates_list[2])
    	mwf_exam_days[i] = mwf_exam_days[i].replace("Thursday", "Thursday, " + dates_list[3])
    	mwf_exam_days[i] = mwf_exam_days[i].replace("Friday", "Friday, " + dates_list[4])

    #print (len(mwf_class_times))
    #print (len(mwf_exam_days))
    #print (len(mwf_exam_times))

    #Make composite array
    mwf_exam_info = []
    for i in range(0,len(mwf_exam_times)):
    	#[0] at end of class times because it's a dictionary(not sure why)
    	mwf_exam_info += [[mwf_class_times[i][0],mwf_exam_days[i],mwf_exam_times[i]]]

    #print (mwf_exam_info)

    #TR stuff ## re.findall(r"<td>([0-9]{1,2}:[0-9][0-9] [a|p]\.m\.)|(----)</td>", tr_exams_text) Does not return time or "----", returns time or empty string
    tr_class_times = re.findall(r"<td>([0-9]{1,2}:[0-9][0-9] [a|p]\.m\.)|(----)</td>", tr_exams_text)
    tr_exam_days =  re.findall(r"<td>(Monday|Tuesday|Wednesday|Thursday|Friday)</td>", tr_exams_text)
    tr_exam_times =  re.findall(r"<td>[0-9]{1,2}:[0-9][0-9] .[ ]?[0-9]{1,2}:[0-9][0-9] ....</td>", tr_exams_text)

    #Trim fat from tr_exam_times
    for i in range(0,len(tr_exam_times)):
    	tr_exam_times[i] = tr_exam_times[i].replace("<td>", "")
    	tr_exam_times[i] = tr_exam_times[i].replace(u"\u2013", "-")
    	if tr_exam_times[i].find(" - ") == -1:
    		tr_exam_times[i] = tr_exam_times[i].replace("-", "- ")
    	tr_exam_times[i] = tr_exam_times[i].replace("</td>", "")

    #Adds dates to tr_exam_days
    for i in range(0,len(tr_exam_days)):
    	tr_exam_days[i] = tr_exam_days[i].replace("Monday", "Monday, " + dates_list[0])
    	tr_exam_days[i] = tr_exam_days[i].replace("Tuesday", "Tuesday, " + dates_list[1])
    	tr_exam_days[i] = tr_exam_days[i].replace("Wednesday", "Wednesday, " + dates_list[2])
    	tr_exam_days[i] = tr_exam_days[i].replace("Thursday", "Thursday, " + dates_list[3])
    	tr_exam_days[i] = tr_exam_days[i].replace("Friday", "Friday, " + dates_list[4])

    #print (len(tr_class_times))
    #print (len(tr_exam_days))
    #print (len(tr_exam_times))

    #Make composite array
    tr_exam_info = []
    for i in range(0,len(tr_exam_times)):
    	#[0] at end of class times because it's a dictionary(not sure why)
    	tr_exam_info += [[tr_class_times[i][0],tr_exam_days[i],tr_exam_times[i]]]
    
    #print (tr_exam_info)

    #Composite dictionary of composite arrays
    exam_info = {"Block": block_exam_info, "MWF": mwf_exam_info, "TR": tr_exam_info}

    #Return composite dictionary
    return exam_info

#Bethany Sanders
def get_specific_final(semester, name, day, time):
    '''Searches the list returned by get_exam_info for the users final time'''
    print((semester))
    print((name))
    print((day))
    print((time))

    if(semester == "F"):
        print("going to site")
        exam_info = get_exam_info("http://www.registrar.fsu.edu/registration_guide/fall/exam_schedule/")
    else:
        print("going to site")
        exam_info = get_exam_info("http://www.registrar.fsu.edu/registration_guide/spring/exam_schedule/")

    day_finals = exam_info[day]
    result = ""

    for final in day_finals:
        if final[0] == time:
            print("getting result")
            result = str(final[1]) +  " " + str(final[2])

    return result;

if __name__ == "__main__":
	#print(get_exam_info("http://www.registrar.fsu.edu/registration_guide/fall/exam_schedule/"))
	#print(get_exam_info("http://www.registrar.fsu.edu/registration_guide/spring/exam_schedule/"))
     print(get_specific_final("F", "class", "MWF", "9:05 a.m."))

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
    if url == "http://www.registrar.fsu.edu/registration_guide/fall/exam_schedule/":
    	block_exams_text = main_page.text[main_page.text.find("<h2>Block Examinations</h2>"):main_page.text.find("<h2>Monday/Wednesday/Friday Classes</h2>")]
    	mwf_exams_text = main_page.text[main_page.text.find("<h2>Monday/Wednesday/Friday Classes</h2>"):main_page.text.find("<h2>Tuesday/Thursday Classes</h2>")]
    	tr_exams_text = main_page.text[main_page.text.find("<h2>Tuesday/Thursday Classes</h2>"):main_page.text.find("<h2>Make-Up Examinations:</h2>")]
    elif url == "http://www.registrar.fsu.edu/registration_guide/spring/exam_schedule/":
    	block_exams_text = main_page.text[main_page.text.find("<h2>Block Examinations</h2>"):main_page.text.find("<h2 class=\"pHeading2TOC\" id=\"toc_marker-3-2\">Monday/Wednesday/Friday Classes</h2>")]
    	mwf_exams_text = main_page.text[main_page.text.find("<h2 class=\"pHeading2TOC\" id=\"toc_marker-3-2\">Monday/Wednesday/Friday Classes</h2>"):main_page.text.find("<h2 class=\"pHeading2TOC\" id=\"toc_marker-3-3\">Tuesday/Thursday Classes</h2>")]
    	tr_exams_text = main_page.text[main_page.text.find("<h2 class=\"pHeading2TOC\" id=\"toc_marker-3-3\">Tuesday/Thursday Classes</h2>"):main_page.text.find("<h2 class=\"pHeading2TOC\" id=\"toc_marker-3-4\">Make-Up Examinations:</h2>")]
    else:
    	return None
    #print (block_exams_text)


    #Block Exam Stuff
    block_exam_classes = re.findall(r"<td>[A-Z]{3}[^<]+</td>", block_exams_text)
    block_exam_days = re.findall(r"<td>(Monday|Tuesday|Wednesday|Thursday|Friday)", block_exams_text)
    block_exam_times = re.findall(r"<td>[0-9]{1,2}:[0-9][0-9] . [0-9]{1,2}:[0-9][0-9] ....</td>", block_exams_text)

    #Trim fat off block_exam classes
    for i in range(0,len(block_exam_classes)):
    	block_exam_classes[i] = block_exam_classes[i].replace("<td>", "")
    	block_exam_classes[i] = block_exam_classes[i].replace("</td>", "")

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


    #MWF stuff
    # re.findall(r"<td>([0-9]{1,2}:[0-9][0-9] [a|p]\.m\.)|(----)</td>", mwf_exams_text) Does not return time or "----", returns time or empty string
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
    #print (len(mwf_class_times))
    #print (len(mwf_exam_days))
    #print (len(mwf_exam_times))

    #Make composite array
    mwf_exam_info = []
    for i in range(0,len(mwf_exam_times)):
    	#[0] at end of class times because it's a dictionary(not sure why)
    	mwf_exam_info += [[mwf_class_times[i][0],mwf_exam_days[i],mwf_exam_times[i]]]
    #print (mwf_exam_info)

    #TR stuff
    # re.findall(r"<td>([0-9]{1,2}:[0-9][0-9] [a|p]\.m\.)|(----)</td>", tr_exams_text) Does not return time or "----", returns time or empty string
    tr_class_times = re.findall(r"<td>([0-9]{1,2}:[0-9][0-9] [a|p]\.m\.)|(----)</td>", tr_exams_text)
    tr_exam_days =  re.findall(r"<td>(Monday|Tuesday|Wednesday|Thursday|Friday)</td>", tr_exams_text)
    tr_exam_times =  re.findall(r"<td>[0-9]{1,2}:[0-9][0-9] .[ ]?[0-9]{1,2}:[0-9][0-9] ....</td>", tr_exams_text)
    for i in range(0,len(tr_exam_times)):
    	tr_exam_times[i] = tr_exam_times[i].replace("<td>", "")
    	tr_exam_times[i] = tr_exam_times[i].replace(u"\u2013", "-")
    	if tr_exam_times[i].find(" - ") == -1:
    		tr_exam_times[i] = tr_exam_times[i].replace("-", "- ")
    	tr_exam_times[i] = tr_exam_times[i].replace("</td>", "")
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

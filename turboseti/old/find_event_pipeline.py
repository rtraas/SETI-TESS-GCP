#!/usr/bin/env python

'''
Front-facing script to find drifting, narrowband events in a set of generalized
cadences of ON-OFF radio SETI observations.
Part of the Breakthrough Listen software package turboSETI
In this code, the following terminology is used:
Hit = single strong narrowband signal in an observation
Event = a strong narrowband signal that is associated with multiple hits
        across ON observations

The main function contained in this file is *find_event_pipeline*
    Find_event_pipeline calls find_events from find_events.py to read a list
    of turboSETI .dat files. It then finds events within this group of files.

Usage (beta):
    import find_event_pipeline;
    find_event_pipeline.find_event_pipeline(dat_file_list_str,
                                            SNR_cut=10,
                                            check_zero_drift=False,
                                            filter_threshold=3,
                                            on_off_first='ON',
                                            number_in_cadence=6,
                                            on_source_complex_cadence=False,
                                            saving=True,
                                            user_validation=False)

    dat_file_list_str   The string name of a plaintext file ending in .lst
                        that contains the filenames of .dat files, each on a
                        new line, that were created with seti_event.py. The
                        .lst should contain a set of cadences (ON observations
                        alternating with OFF observations). The cadence can be
                        of any length, given that the ON source is every other
                        file. This includes Breakthrough Listen standard ABACAD
                        as well as OFF first cadences like BACADA. Minimum
                        cadence length is 2, maximum cadence length is
                        unspecified (currently tested up to 6).

                        Example: ABACAD|ABACAD|ABACAD

    SNR_cut             The threshold SNR below which hits in the ON source
                        will be disregarded. For the least strict thresholding,
                        set this parameter equal to the minimum-searched SNR
                        that you used to create the .dat files from
                        seti_event.py. Recommendation (and default) is 10.

    check_zero_drift    A True/False flag that tells the program whether to
                        include hits that have a drift rate of 0 Hz/s. Earth-
                        based RFI tends to have no drift rate, while signals
                        from the sky are expected to have non-zero drift rates.
                        Default is False.

    filter_threshold    Specification for how strict the hit filtering will be.
                        There are 3 different levels of filtering, specified by
                        the integers 1, 2, and 3. Filter_threshold = 1
                        returns hits above an SNR cut, taking into account the
                        check_zero_drift parameter, but without an ON-OFF check.
                        Filter_threshold = 2 returns hits that passed level 1
                        AND that are in at least one ON but no OFFs.
                        Filter_threshold = 3 returns events that passed level 2
                        AND that are present in *ALL* ONs. Default is 3.

    on_off_first        Tells the code whether the .dat sequence starts with
                        the ON or the OFF observation. Valid entries are 'ON'
                        and 'OFF' only. Default is 'ON'.

    number_in_cadence   The number of files in a single ON-OFF cadence.
                        Default is 6 for ABACAD.

    on_source_complex_cadence

                        If using a complex cadence (i.e. ons and offs not
                        alternating), this variable should be the string
                        target name used in the .dat filenames. The code will
                        then determine which files in your dat_file_list_str
                        cadence are ons and which are offs. Default is false.

    saving              A True/False flag that tells the program whether to
                        save the output array as a .csv. Default is True.

    user_validation     A True/False flag that, when set to True, asks if the
                        user wishes to continue with their input parameters
                        (and requires a 'y' or 'n' typed as confirmation)
                        before beginning to run the program. Recommended when
                        first learning the program, not recommended for
                        automated scripts. Default is False.

author:
    Version 3.0 - Raffy Traas (raffytraas14@gmail.com)
    Version 2.0 - Sofia Sheikh (ssheikhmsa@gmail.com),
    Version 1.0 - Emilio Enriquez (jeenriquez@gmail.com)

Last updated: 05/24/2020
***
NOTE: This code works for .dat files that were produced by seti_event.py
after turboSETI version 0.8.2, and blimpy version 1.1.7 (~mid 2019). The
drift rates *before* that version were recorded with the incorrect sign
and thus the drift rate sign would need to be flipped in the make_table
function.
***


Update notes: Updated support for files not beginning with 'spliced'.

NOTE: No support for spliced/non-spliced option select for when
'on_off_first' is 'TRUE'.
'''

#required packages and programs
import find_event
import pandas as pd

#required for find_event
import time
import numpy as np

def find_event_pipeline(dat_file_list_str,
                        SNR_cut=10,
                        check_zero_drift=False,
                        filter_threshold=3,
                        on_off_first='ON',
                        number_in_cadence=6,
                        on_source_complex_cadence=False,
                        saving=True,
                        user_validation=False):

    print()
    print("************   BEGINNING FIND_EVENT PIPELINE   **************")
    print()

    if on_source_complex_cadence == False:
        print("Assuming the first observation is an " + on_off_first)

    if on_source_complex_cadence != False:
        print("Assuming a complex cadence for the following on source: " + on_source_complex_cadence)

    #Opening list of files
    dat_file_list = open(dat_file_list_str).readlines()
    dat_file_list = [files.replace('\n','') for files in dat_file_list]
    dat_file_list = [files.replace(',','') for files in dat_file_list]
    n_files = len(dat_file_list)

    #Getting source names
    source_name_list = []
    for dat in dat_file_list:
        # if we want 5 use 5 (USE ONLY IF YOU'RE USING SPLICED FILES)
        if dat.split('_')[0] == 'spliced':
            source_name = dat.split('_')[5]
        # if we want 3 use 3 (because we're not using "spliced files")
        else:
            source_name = dat.split('_')[3]

        source_name_list.append(source_name)

    # This will be skipped because, by default, "on_source_complex_cadence" is set to "False"
    if on_source_complex_cadence != False:
        complex_cadence = []
        for i in range(0, len(source_name_list)):
            source = source_name_list[i]
            if source == on_source_complex_cadence:
                complex_cadence.append(1)
            else:
                complex_cadence.append(0)
        print("The derived cadence is: " + str(complex_cadence))

    print("There are " + str(len(dat_file_list)) + " total files in the filelist " + dat_file_list_str)
    print("therefore, looking for events in " + str(int(n_files/number_in_cadence)) + " on-off set(s)")
    print("with a minimum SNR of " + str(SNR_cut))

    if filter_threshold == 1:
        print("Present in an A source only, above SNR_cut")
    if filter_threshold == 2:
        print("Present in at least one A source with RFI rejection from the off-sources")
    if filter_threshold == 3:
        print("Present in all A sources with RFI rejection from the off-sources")

    if check_zero_drift == False:
        print("not including signals with zero drift")
    if check_zero_drift == True:
        print("including signals with zero drift")
    if saving == False:
        print("not saving the output files")
    if saving == True:
        print("saving the output files")

    # making the "name" variable have a global scale
    #name = None

    # Second attempt at making the "name" variable have a global scale
    #global name
    #name = None

    # Third attempt at making the "name" variable have a global scale
    # Need to put "global name" inside of the following "for" loop
    name = ''
    nm = ''
    if user_validation == True:
        question = "Do you wish to proceed with these settings?"
        while "the answer is invalid":
            reply = str(input(question+' (y/n): ')).lower().strip()
            if reply == '':
                return
            if reply[0] == 'y':
                break
            if reply[0] == 'n':
                return

        #Looping over number_in_cadence chunks.
        candidate_list = []
        for i in range((int(n_files/number_in_cadence))):
            file_sublist = dat_file_list[number_in_cadence*i:((i*number_in_cadence)+(number_in_cadence))]
            global name
            if complex_cadence == False:

                if on_off_first == 'ON':

                    # if we want 5 use 5 (USE ONLY IF YOU'RE USING SPLICED FILES)
                    #if dat.split('_')[0] == 'spliced':
                        #source_name = dat.split('_')[5]
                    # if we want 3 use 3 (because we're not using "spliced files")
                    if file_sublist[0].split('_')[0] == 'spliced':

                        name = file_sublist[0].split('_')[5]
                        id_num = (file_sublist[0].split('_')[6]).split('.')[0]
                    else:

                        name = file_sublist[0].split('_')[3]
                        id_num = (file_sublist[0].split('_')[4]).split('.')[0]
                # No support for spliced/non-spliced option select
            else:
                name = file_sublist[complex_cadence.index(1)].split('_')[5]
                id_num = file_sublist[complex_cadence.index(1)].split('_')[6].split('.')[0]


            nm = name
            print()
            print("***       " + name + "       ***")
            print()
            cand = find_event.find_events(file_sublist,
                                          SNR_cut=SNR_cut,
                                          check_zero_drift=check_zero_drift,
                                          filter_threshold=filter_threshold,
                                          on_off_first=on_off_first,
                                          complex_cadence=complex_cadence)
            cand_len = 1
            if cand is None:
                cand_len = 0
            if cand_len != 0:
                candidate_list.append(cand)
        if len(candidate_list) > 0:
            find_event_output_dataframe = pd.concat(candidate_list)
        else:
            "Sorry, no potential candidates with your given parameters :("
            find_event_output_dataframe = []

        print("************  ENDING FIND_EVENT PIPELINE   **************")
    nm = name
    if saving == True:
        if check_zero_drift == True:
            # Using 'nm' variable
            filestring = nm + '_' + id_num + '_f' + str(filter_threshold) + '_snr' + str(SNR_cut) + '_zero' + '.csv'
            # Using "name" variable
            #filestring = name + '_' + id_num + '_f' + str(filter_threshold) + '_snr' + str(SNR_cut) + '_zero' + '.csv'
        else:
            # Using 'nm' variable
            filestring = nm + '_' + id_num + '_f' + str(filter_threshold) + '_snr' + str(SNR_cut) + '.csv'
            # Using "name" variable
            #filestring = name + '_' + id_num + '_f' + str(filter_threshold) + '_snr' + str(SNR_cut) + '.csv'
        if not isinstance(find_event_output_dataframe, list):
            find_event_output_dataframe.to_csv(filestring)
        else:
            print("Sorry, no events to save :(")

    return(find_event_output_dataframe)
find_event_pipeline('HIP39826.lst')

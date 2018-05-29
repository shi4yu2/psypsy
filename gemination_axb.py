#! /usr/bin/env python3
#  -*- coding: utf-8 -*-

__author__ = 'ShY'
__copyright__ = 'Copyright 2018, SHY'
__version__ = '0.1.0 (20180529)'
__maintainer__ = 'ShY, Pierre Halle'
__email__ = 'shi4yu2@gmail.com'
__status__ = 'Development'

import pygame
import pygame.draw
import pygame.event
import pygame.font
import pygame.image
import sys
from pygame.locals import *

import libpsypsy.psypsyio as psypsyio
import libpsypsy.psypsyaxb as psypsyaxb
import libpsypsy.psypsyinterface as psypsyinterface


# ================================================================
# AXB exp ========================================================
def axb(screen, background, input_file, result_file, instructions, isi=1000, fixation_duration=500, train=False):
    try:
        # Import stimuli files =========================================
        # stimuli are organised in a python dictionary type, to view the content use print()
        trial, header_index = psypsyio.read_stimuli(input_file, "\t")
        # print(trial["trial_number"])

        # Create result file ===========================================
        result = open(result_file, "w")

        # Add header to result output file
        psypsyio.write_result_header(result, trial, result_columns)

        # Initialize counts for feedback
        nb_trials = nb_correct = nb_wrong = nb_missed = 0
        correct_rt = wrong_rt = 0

        for i in range(trial["trial_number"]):
            # for i in range(2):  # modify number in the range() to make test
            screen.fill(background)
            pygame.display.flip()

            # Pauses: 192 trials, 1 break
            if not train:
                if i == 95:
                    psypsyaxb.axb_pause(screen, screen_width, screen_height, background,
                                        instructions.get("pause"))

            # Processing sound stimuli =================================
            if train:
                path = "training/"
            else:
                path = "stim/"

            # Get stimuli path
            stimulus_a = path + trial["A"][i] + ".wav"
            stimulus_x = path + trial["X"][i] + ".wav"
            stimulus_b = path + trial["B"][i] + ".wav"
            sound_path = [stimulus_a, stimulus_x, stimulus_b]

            # Load stimuli & Compute sound stimuli duration
            mixed_sounds, duration_sounds = psypsyaxb.mix_sound_stimuli(sound_path)

            # Compute target result
            if trial["X"][i][:-2] == trial["A"][i][:-2]:
                # compare two strings of A and X if identical then A else B
                target_response = "A"
            else:
                target_response = "B"

            # Prepare output line
            trial_result = []
            for key in header_index:
                trial_result.append(trial[header_index[key]][i])

            # =*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
            # Play sounds and record response                           =
            # =*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
            # Display fixation point
            psypsyinterface.point_fixation(screen, fixation_duration)
            # 500ms of display
            psypsyinterface.clear_screen(screen, background)

            # Play A ==============
            start_sound_a = pygame.time.get_ticks()
            mixed_sounds[0].play()  # PLAY SOUND A
            while pygame.mixer.get_busy():  # sound playing
                continue
            end_sound_a = pygame.time.get_ticks()

            while pygame.time.get_ticks() - end_sound_a < 1000:
                continue
            pygame.event.pump()
            pygame.event.clear()  # clear event and wait for response

            # Play X and B and record response (Type, Time) =========
            xb_sequence = [mixed_sounds[1], mixed_sounds[2]]
            xb_measures = []
            response = False
            response_type = []
            response_time = []

            # indication for X and B
            # index_b == 0: ISI after X
            # index_b == 1: ISI after B
            index_b = 0

            for s in xb_sequence:
                # get start point of the sound
                duration = int(round(pygame.mixer.Sound.get_length(s), 3) * 1000)
                start_sound = pygame.time.get_ticks()
                xb_measures.append(start_sound)
                s.play()  # play sound

                # index_b == 1: 2000ms after sound B
                if index_b == 1:
                    isi_post = 2000
                else:
                    # index_b == 0: 1000ms after sound X
                    isi_post = 1000

                while pygame.mixer.get_busy() and not response or (
                        pygame.time.get_ticks() - start_sound <= duration + isi_post):
                    for e in pygame.event.get():
                        if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                            raise Exception
                        elif e.type == KEYDOWN:
                            if e.key == K_LSHIFT:
                                response_time = [pygame.time.get_ticks()]
                                response_type = ["A"]
                                response = True
                            elif e.key == K_RSHIFT:
                                response_time = [pygame.time.get_ticks()]
                                response_type = ["B"]
                                response = True
                        else:
                            response = False

                # Get end point of the sound
                if index_b == 1:
                    xb_measures.append(pygame.time.get_ticks() - 2000)
                elif index_b == 0:
                    xb_measures.append(pygame.time.get_ticks() - 1000)

                index_b += 1

            # Get measures
            start_sound_x = xb_measures[0]
            end_sound_x = xb_measures[1]
            start_sound_b = xb_measures[2]
            end_sound_b = xb_measures[3]

            # Handle empty response
            # response time ==============================
            if response_time != []:
                response_time_s = response_time[0]
                real_rt = response_time_s - start_sound_b
            else:
                response_time_s = 0
                real_rt = 0
            # response type ==============================
            if response_type != []:
                response_type_s = response_type[0]
            else:
                response_type_s = "NA"

            # Compute the correctness of response
            # And display feedback for training
            nb_trials += 1

            if response_type_s == target_response:
                correct = "T"
                nb_correct += 1
                correct_rt += real_rt
                if train:
                    psypsyinterface.display_text_colour(screen, str(real_rt) + " ms", colour=(0, 255, 0))
                    pygame.time.wait(500)
                    psypsyinterface.clear_screen(screen, background)
            elif response_type_s == "NA":
                correct = "F"
                nb_missed += 1
                if train:
                    psypsyinterface.display_text_colour(screen, "???")
                    pygame.time.wait(500)
                    psypsyinterface.clear_screen(screen, background)
            else:
                correct = "F"
                # Calculate wrong response number and mean(rt)
                nb_wrong += 1
                wrong_rt += real_rt
                if train:
                    for click in range(3):
                        psypsyinterface.display_text_colour(screen, str(real_rt) + "ms")
                        pygame.time.wait(100)
                        psypsyinterface.clear_screen(screen, background)
                        pygame.time.wait(50)

            # Append trial measures
            trial_result.extend([start_sound_a, duration_sounds[0], end_sound_a,
                                 start_sound_x, duration_sounds[1], end_sound_x,
                                 start_sound_b, duration_sounds[2], end_sound_b,
                                 response_time_s, target_response, response_type_s, real_rt, correct])

            # Output results
            psypsyio.write_result(result, trial_result)

            # inter-trial time
            pygame.time.wait(interTrial)

        resume = {"nb_trials": nb_trials,
                  "nb_correct": nb_correct,
                  "nb_wrong": nb_wrong,
                  "nb_missed": nb_missed,
                  "correct_rt": correct_rt,
                  "wrong_rt": wrong_rt}

    finally:
        if not train:
            print("End experiment\n")
            pygame.time.wait(1000)
        else:
            print("End training\n")

    return resume


# MAIN ==========================================================================
if __name__ == "__main__":
    # Parameter ==========================================================
    # == Program environment parameter ===================================
    font: str = "helvetica"
    background = (150, 150, 150)  # gray

    # Experiment parameter ===============================================
    isi = 1000  # ISI = 1000ms
    interTrial = 1000  # inter-trial time = 1000ms
    fixation_duration = 500  # fixation point duration
    # ====================================================================
    # == Parameter =======================================================

    # Instruction path
    instructions = {"start": "instructions/instruction_start.png",
                    "pause": "instructions/instruction_break.png",
                    "end_training": "instructions/instruction_end_training.png",
                    "end_exp": "instructions/instructions_end_exp.png"}

    # Result file columns ================================================
    result_columns = ["start_A", "duration_A", "end_A", "start_X", "duration_X", "end_X", "start_B",
                      "duration_B", "end_B", "RT", "target_Response", "response", "real_RT", "Correctness"]

    subj = sys.argv[1]
    axb_input = "list_trial/axb_" + subj + ".csv"
    training_input = "list_trial/training_" + subj + ".csv"
    axb_result = "result_axb/axb_" + subj + "_result" + ".csv"
    training_result = "result_axb/training_" + subj + "_result" + ".csv"

    screen, screen_width, screen_height = psypsyaxb.initialisation_pygame(background)

    # sampling rate for training
    pygame.mixer.quit()
    pygame.mixer.init(16000, -16, 2)

    # Training instruction
    psypsyinterface.display_instruction(instructions.get("start"),
                                        screen, screen_width, screen_height, background)

    resume = axb(screen, background, training_input, training_result, isi, fixation_duration, train=True)
    print("nb ok: " + str(resume["nb_correct"]) + "/" + str(resume["nb_trials"]))
    print(str(int(resume["correct_rt"]/resume["nb_correct"])))

    # AXB ===============================================================
    # sampling rate for axb
    pygame.mixer.quit()
    pygame.mixer.init(44100, -16, 2)

    # AXB instruction
    psypsyinterface.display_instruction(instructions.get("end_training"),
                                        screen, screen_width, screen_height, background)

    resume = axb(screen, background, axb_input, axb_result, isi, fixation_duration)

    psypsyinterface.display_instruction(instructions.get("end_exp"),
                                        screen, screen_width, screen_height, background)
    pygame.quit()

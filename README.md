# Gemination AXB task

# Installation:
1. Install all requirements
 - ```$ bash install.sh```

# AXB experiments:

## 1. Randomization 
- use `randomisation_config.py` to generate constraints (explanations are in the file)
- `libpsypsy.psypsyrandom` module
- stimuli files are generated after launching experience, and placed in `trial_gemination_axb/` folder
- results files are in `result_gemination_axb/` folder
- a file containing results for all subjects are generated after experiment.


## 2. Launch experiment    
- python3 gemination_axb.py [subj_N° in two digits] [part in one digit]

Example: 

```$ python3 gemination_axb.py 00 1```

```$ python3 gemination_axb.py 01 1```

...

```$ python3 gemination_axb.py 98 2```

```$ python3 gemination_axb.py 99 2```



## 3. Description of Experiment
1. display instruction of training
    - click `<space>` when finish reading instruction to continue
2. training session
3. display instruction of AXB
    - click `<space>` when finish reading instruction to continue
4. AXB session
    - trial_list.csv contains 192 trials
        - participants will have one breaks at 96th trial
        - No limite of time for breaks
        - once finish the break, click <space> to continue
5. Results
    - result files are in the `result_axb` folder
    - result is append to `result_total` file with subject number when experiment is finished
    - the response time is given both in absolute value (from the beginning of the excution of program) and in relative value (response time - start of sound B) 
        - if response before B: negative value
        - if response after B: positive value

4. Experiment parameters
    - Response A: left shift
    - Response B: right shift
    - ISI 1000ms
    - Limit of response time: 2s after the end of sound B
    - the experiment can be stopped any time by clicking ESC
    - background color ([0,0,0] for black and [255,255,255] for white)

# Experiment script: gemination_axb.py
    supporting files: libpsypsy/
                      ./psypsyio.py
                      ./psypsyinterface.py
                      ./psypsyaxb.py
                      ./psypsyrandom.py

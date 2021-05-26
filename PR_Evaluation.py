import time
import pandas as pd
import os
from tqdm import tqdm

PUNC = [',', '.', '?']
PUNC_NAMES = ["Comma", "Period", "Question Mark"]

def punc_to_puncname(punc):
    assert punc in PUNC, "Provide a valid punctuation sign, only: , . ? are allowed"
    return PUNC_NAMES[PUNC.index(punc)]

# Give filename like "test_speech" without any additions
def file_name_to_ref_p_and_restored_p(fileName):
    """
    Returns the appropriate filename based on the extension as denoted in the pipeline
    :param fileName:
    :return: Tuple of reference and restored filenames
    """
    refPuncFileName = fileName + "_reference_punc.txt"
    restoredPuncFileName = fileName + "_restored_punc.txt"
    return refPuncFileName, restoredPuncFileName

def get_ref_p_and_restored_p(refPuncFileName, restoredPuncFileName):
    """
    Retrieves reference punctuation and restored punctuations as strings
    :param refPuncFileName: string denoting reference punctuation filename
    :param restoredPuncFileName: string denoting restored punctuation filename
    :return:
    """
    textRefPunc, textRestoredPunc = "", ""
    with open(refPuncFileName, 'r', encoding='utf-8') as f1:
        textRefPunc = f1.read()
    with open(restoredPuncFileName, 'r', encoding='utf-8') as f2:
        textRestoredPunc = f2.read()
    return textRefPunc.lower(), textRestoredPunc.lower()

def split_punc(text):
    """
    Splits punctuation by adding a space before all punctuation characters
    """
    newText = ""
    for i in range(len(text)):
        curChar = text[i]
        if curChar in PUNC:
            newText += " "
        newText += curChar
    return newText

def ref_and_res_to_scores(fileName=None, refPuncFileName=None, resPuncFileName=None):
    """
    Get the scores by taking the reference punctuation and the restored punctuation
    while skipping the first and the last word to generate scores
    :param fileName: Consistent filename in format X_reference_punc.txt and X_restored_punc.txt
    :return:
    """
    if resPuncFileName is None and refPuncFileName is None and fileName is not None:
        refPuncFileName, resPuncFileName = file_name_to_ref_p_and_restored_p(fileName)

    refPunc, resPunc = get_ref_p_and_restored_p(refPuncFileName, resPuncFileName)

    refPunc = split_punc(refPunc).split()
    resPunc = split_punc(resPunc).split()
    # print(refPunc)
    # print(resPunc)

    # Go over reference punctuation text
    final_dict = {}
    for punc in PUNC:
        C, D, I, S, N = 0, 0, 0, 0, 0
        i, j = 1, 1
        goNext = True
        while goNext:
            refToken = refPunc[i]
            resToken = resPunc[j]

            # IF there is a match
            if refToken == resToken and LR_match(refPunc, resPunc, i, j):
                if refToken == punc:
                    C += 1

            # IF there is NOT a match
            elif refToken != resToken:
                # Substitution error
                if refToken == punc and resToken in PUNC and LR_match(refPunc, resPunc, i, j):
                    S += 1

                # Deletion error
                elif refToken in PUNC and resToken not in PUNC:
                    if LR_match(refPunc, resPunc, i, j, -1) and refToken == punc:
                        D += 1
                    i += 1

                # Insertion error
                elif refToken not in PUNC and resToken in PUNC:
                    if LR_match(refPunc, resPunc, i, j, 1) and resToken == punc:
                        I += 1
                    j += 1

            if i >= len(refPunc)-2 and j >= len(resPunc)-2:
                goNext = False
            if i < len(refPunc)-2:
                i += 1
            if j < len(resPunc)-2:
                j += 1

        statsDict = {
            "C": C,
            "D": D,
            "I": I,
            "S": S,
            "N": len(refPunc)}
        # punc_dict = {punc_to_puncname(punc) : statsDict}
        final_dict[punc_to_puncname(punc)] = statsDict

    return final_dict

# -1 if word in second text should be one to the left
# +1 if word in second text should be one to the right
def LR_match(text_1, text_2, i, j, dir=0):
    return text_1[i-1] == text_2[j-1] and text_1[i+1] == text_2[j+1+dir]

def add_metric_to_df(df, metric):
    metrics = []
    for punc_name in PUNC_NAMES:
        C = df.at[punc_name, "C"]
        D = df.at[punc_name, "D"]
        I = df.at[punc_name, "I"]
        S = df.at[punc_name, "S"]
        N = df.at[punc_name, "N"]
        metric_value = 0
        if C + D + I + S == 0:
            metric_value = float("NaN")

        elif metric == "SER":
            metric_value = (D + I + S) / (C + D + S)

        elif metric == "CER":
            metric_value = (D + I + S) / N

        elif metric == "Precision":
            if C + I + S == 0 or C == 0:
                metric_value = 0
            else:
                metric_value = C / (C + I + S)

        elif metric == "Recall":
            if C + D + S == 0 or C == 0:
                metric_value = 0
            else:
                metric_value = C / (C + D + S)

        elif metric == "F-Measure":
            if "Precision" in df and "Recall" in df:
                P = df.at[punc_name, "Precision"]
                R = df.at[punc_name, "Recall"]
                metric_value = (2*P*R) / (P+R)

        else:
            raise Exception("Must specify valid metric!")
        metrics.append(metric_value)

    df[metric] = metrics
    return df

def calculate_final_scores(score_dict_list):
    """
    Given a list of score dictionaries compute a final dictionary containing the combined scores
    :param score_dict_list: A list of score dictionaries
    :return: Dictionary containing added scores
    """
    final_scores_dict = {}
    for punc_name in PUNC_NAMES:
        total_C, total_D, total_I, total_S, total_N = 0, 0, 0, 0, 0
        # print(f"Current punctuation: {punc_name}")
        for score_dict in score_dict_list:
            cur_dict = score_dict[punc_name]
            # print(cur_dict)
            total_C += cur_dict["C"]
            total_D += cur_dict["D"]
            total_I += cur_dict["I"]
            total_S += cur_dict["S"]
            total_N += cur_dict["N"]
        final_scores_dict[punc_name] = {
            "C": total_C,
            "D": total_D,
            "I": total_I,
            "S": total_S,
            "N": total_N}
    return final_scores_dict

def get_all_score_dicts(ref_punc_folder_name, res_punc_folder_name):
    """
    Return a list of score dictionaries for a set of two folders. This function assumes the naming
    of the files in the folders are correct according to the diagram and hence if sorted
    match files. Both folders should be in the directory this script is also in.
    :param ref_punc_folder_name: Filename of the reference punctuation folder
    :param res_punc_folder_name: Filename of the restored punctuation folder
    :return: A list of score dictionaries
    """
    filenames_ref_punc = os.listdir(ref_punc_folder_name)
    filenames_res_punc = os.listdir(res_punc_folder_name)
    # print(f"Filenames Reference Punc: {filenames_ref_punc}")
    # print(f"Filenames Restored Punc: {filenames_res_punc}")
    # print(filenames_ref_punc)
    print(f"Number of reference punctuation files: {len(filenames_ref_punc)}")
    print(f"Number of restored punctuation files: {len(filenames_res_punc)}")
    counter = 0
    score_dicts_list = []
    start_timer = time.time()
    for i in tqdm(range(0, 461)):  # 301, 461
        # print(i)
        fileName = str(i)
        ref_punc_filename = ref_punc_folder_name + "\\" + fileName + "_reference_punc.txt"
        res_punc_filename = res_punc_folder_name + "\\" + "pr_" + fileName + "_asr_output.txt"
        if os.path.isfile(ref_punc_filename) == os.path.isfile(res_punc_filename) and os.path.isfile(
                ref_punc_filename):
            counter += 1
            score_dicts_list.append(ref_and_res_to_scores(refPuncFileName=ref_punc_filename,
                                                          resPuncFileName=res_punc_filename))
            # print("--- %s seconds ---" % (time.time() - start_time))
    print(f"--- Processed {counter} files in {time.time() - start_timer} seconds ---")


    # score_dicts_list = []
    # assert len(filenames_ref_punc) == len(filenames_res_punc), "Amount of restored punctuation and reference punctuation files should be equal to calculate scores!"
    # for i in range(len(filenames_ref_punc)):
    #     # print(f"ref file 0:3 {filenames_ref_punc[i][0:3]}")
    #     # print(f"res file 0:3 {filenames_res_punc[i][0:3]}")
    #     ref_path = ref_punc_folder_name + "\\" + filenames_ref_punc[i]
    #     res_path = res_punc_folder_name + "\\" + filenames_res_punc[i]
    #     score_dicts_list.append(ref_and_res_to_scores(refPuncFileName=ref_path,
    #                                                   resPuncFileName=res_path))
    return score_dicts_list

# textAsr = "Thank you welly much Mr precedent Ladies and Gentlemen I am strong."
# textTransc = "Thank you very much, Mr. President. Ladies and Gentlemen, I am strong."
# scores_dicts_valid = ref_and_res_to_scores(fileName="valid")
# scores_dicts_test = ref_and_res_to_scores(fileName="test")
# print(f"Valid: \n{scores_dicts_valid}")
# print(f"Test: \n{scores_dicts_test}")
# fin_dict = calculate_final_scores([scores_dicts_valid, scores_dicts_test])

# Start timer to calculate processing time
start_time = time.time()

# Get all the scores from the individual ref_punc and res_punc files
scores_dict_list = get_all_score_dicts(ref_punc_folder_name="reference_punc", res_punc_folder_name="pr_output")

# Add those scores up together
final_scores_dict = calculate_final_scores(scores_dict_list)
# print(f"Final Scores Dict: \n{final_scores_dict}")

# Convert dictionary to a dataframe
df = pd.DataFrame.from_dict(final_scores_dict, orient="index")

# Add metrics to dataframe
df = add_metric_to_df(df, metric="SER")
df = add_metric_to_df(df, metric="CER")
df = add_metric_to_df(df, metric="Precision")
df = add_metric_to_df(df, metric="Recall")
df = add_metric_to_df(df, metric="F-Measure")

# Print dataframe and processing time
print(df)
print("--- %s seconds ---" % (time.time() - start_time))

# Dataframe to csv
df.to_csv('PR_scores.csv')

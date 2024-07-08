from service.Modules.Sentence_identification_module.sinmorphic import get_sinhala_morphology


def check_subject(subject):
    correctness_status=0
    morphology_list = get_sinhala_morphology(subject)
    # Extract the description from the first element of morphology_list
    description = morphology_list[0]['description']

    # Split the description string based on the tab character ('\t')
    parts = description.split('\t')

    # Take the second part which contains the desired information
    desired_part = parts[1]
    if "ACC" in desired_part:
        correctness_status=1
    else:
        correctness_status=1
    return correctness_status

def Check_oubject(s_suject):
  status =0;
  morphology_list = get_sinhala_morphology(s_suject)
  description = morphology_list[0]['description']
  parts = description.split('\t')
  desired_part = parts[1]
  if "NOM" in desired_part:
    status =1;
  else:
    status =0;

  return status


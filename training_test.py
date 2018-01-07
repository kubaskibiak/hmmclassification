from train.model_training import *


# class_1 A - This content type covers a typical news coverage. For such type of videos the initial spoken part provides introduction and brief overview of the content of the video. Usually there are multiple ``talking heads'', may be worth extracting Spoken Text text and analyze for valuable information. Examples of such videos are studio-started news coverage which shifts to shots or report from outside the studio.The best summarization strategy for this type of videos requires extraction of the first segment of speech and further extraction of interesting scenes.
# class_2 B - This type of content covers all types of discussions or interviews. The discussion or interviews can be done in the TV studio or via a video conferencing link. Examples of such videos are panels and discussions with one or many experts. In this scenario the video does not contain any interesting visual information, while most of the information is conveyed via speech. For such video type the only feasible summarization is ASR and ASR result analysis.
# class_3 C - In this scenario there is no spoken text - only video with ambient noise and sounds. For such videos parts cut out using spatio-temporal analysis seem to be the best strategy. Examples of such videos are CCTV recordings or video recordings from a war zone.


class_list = ['class_1','class_2','class_3']
print(class_list)
for single_class in class_list:
    print(class_list)
    model = train_model(single_class)
    joblib.dump(model, "models/model_for_" + single_class + ".pkl")







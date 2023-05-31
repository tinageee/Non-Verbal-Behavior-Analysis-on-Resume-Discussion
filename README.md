# Resume_study_non_verbal_analysis
Studied vocal and head post differences between deceivers and truth tellers in a mock recruiter review session. Findings contribute to deception detection research.


Summary:
The analysis found that head position variance is not affected by role or the interaction between role and stage. However, there was a significant effect of the "role" factor on spectral features. The Truth-teller group showed higher variance of spectral change compared to the Deceiver group, indicating differences in vocal characteristics.



Head Position

Head position: Pitch, Roll, Yaw
Stages: Introduction, Note presentation, discussion
Roles: Deceiver, truth-teller

Note:
•	The Introduction and Note presentation stages were cut into each speaker's clips, each lasting less than 1 minute.
•	The Discussion stage was processed as a whole, lasting around 5 minutes.
•	To remove extreme values that may have skewed the results, we removed any values greater than the 95th percentile from the head position variance data.

Summary:
Overall, the following analysis suggests that head position variance is not significantly affected by the role or the interaction between role and stage.


Vocalic Features

Data preprocessing
1.	The data consisted of audio features obtained from players in the introduction and note-presentation.
2.	The audio features data was processed using openSmile, resulting in 88 features that were saved in a file called "raw_feature.csv".
3.	Standardized the openSmile features data using StandardScaler().
4.	Performed PCA to extract the top N principal components that accounted for more than 60% of the variance in the data. N=6
5.	Set the number of factors to 6. Performed factor analysis using the FactorAnalyzer() function in Python
6.	Only kept variables with absolute primary factor loadings > 0.5 and secondary factor loadings < 0.3.
7.	Grouped and sorted the variables based on the factors they loaded highest on to simplify the data structure and identify important variables for each factor.
8.	Calculate a score for each factor by taking a simple average of the corresponding variables of that factor based on Table 1 (If a variable has a negative loading, multiply the original value by -1 to ensure that it is scored correctly.) (vocal_grouped.csv)
9.	Run ANOVA test

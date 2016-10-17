## Kidlearn for php

Here is a small module to use kidlearn_lib on a php server. 

### Prerequisites : 

 * python 2.7 installed on the server 
 * numpy, scipy installed (check kidlearn_lib dependencies)
 * kidlearn_lib installed ( git clone https://github.com/flowersteam/kidlearn.git / python setup.py install)

### Usage :

* In htdocs folder : 
    * put kidlearn_php.py, 
    * put params_fils and graph/ folder which contain all files which are relatives to algorithms parameters and graph definition
    * stud_list_ex folder : contains exercise historic and the next exercise to do for each student. 

* kidlearn_php.py file : 
    * inputs : -i : algo_file_name / -s : student_id / -r : result (optional) 
    * outputs : the outputs are written in stud_list_ex folder, the next exercise for student "X" is written in "last_act_{X}.json" file and the historic of exercise is logged in "exlist_{X}.json" file. 

* Php example code : kid_firt_ex.php, kid_answer.php give example php code to use kidlearn_php.py :
    * kid_firt_ex.php presents code when the student make his first exercise and don't have made exercise before, so the command to execute don't have the result. 
    * kid_anser.php presents to use when a student gave an answer to a precedent exercise and the algorithm will use this answer to update the algorithm data.

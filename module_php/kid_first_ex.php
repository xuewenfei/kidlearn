<?php

   $stud_id = "S1"; // here you put the student ID
   $algo_file_name = "ZPDES"; // name of config file for the algorithm

   $str_command = "python kidlearn_php.py -i {$algo_file_name} -s {$stud_id}"; // str command to execute the script
   $command = escapeshellcmd($str_command); // def command
   shell_exec($command); // execution of the command

   $next_ex_file = "stud_list_ex/last_act_{$stud_id}.json"; //file 
   $next_ex_str = file_get_contents($next_ex_file, true);
   echo $next_ex_str; 
   $next_ex = json_decode($next_ex_str, true);
    
?>
    

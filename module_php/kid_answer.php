<?php
   $stud_id = "S1"; // here you put the student ID
   $result = 1; // here you put the student result of the last exercise

   $str_command = "python kidlearn_php.py -i ZPDES -o {$stud_id} -r {$result}"; // str command
   $command = escapeshellcmd($str_command); // def command
   shell_exec($command); // execution of the command

   $next_ex_file = "stud_list_ex/last_act_{$stud_id}.json"; //file 
   $next_ex_str = file_get_contents($next_ex_file, true);
   echo $next_ex_str; 
   $next_ex = json_decode($next_ex_str, true);
    
?>


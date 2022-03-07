<?php

function decode_and_write($fname)
{
    $filename = $fname;
    $file = fopen($filename, 'r');  //要解密的文件名

    // 判断是否为目标文件
    $magic_number = fread($file, 20);

    if (!preg_match('/\$[0|O]{6}/', $magic_number)) {
        exit("不是威盾加密的文件");
    }

    // 重置文件指针
    fseek($file, 5);
    $file_content = fread($file, filesize($filename));
    fclose($file);


    // 第一步：解码目标文件中的密文部分

    // 取出前面的变量定义，并执行
    $eval_pos = strpos($file_content, "eval");
    $vars = substr($file_content, 0, $eval_pos);
    eval($vars);

    // 获取解码函数名称，并解码密文
    $decode_var = substr($file_content, $eval_pos + 5, 7);
    $cipher1 = substr($file_content, $eval_pos + 14);
    $end_pos = strrpos($cipher1, ';');
    $cipher1 = substr($cipher1, 0, $end_pos - 3);
    $plaintext1 = eval("return {$decode_var}('$cipher1');");


    // 第二步：将解码密文得到的明文，再解码其中的密文，得到最后的明文代码

    $plaintext1 = str_replace('eval', 'return ', $plaintext1);
    $plaintext2 = substr(eval($plaintext1), 2);


    // 第三步：写回原来的文件
    $new_file = fopen($filename, 'w');
    fwrite($new_file, $plaintext2);
    fclose($new_file);
}

$fname = "X:\websites\binxin3.1\core\lib\Db.php";
decode_and_write($fname);
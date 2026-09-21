#include <stddef.h>
#include <string.h>

// void process_input(const unsigned char *data, size_t size)
// {
//     char buffer[16];
//     memcpy(buffer, data, size);
    
// }





int process_input(const unsigned char *data, size_t size)
{
    char buffer[16];
    if (size <= sizeof(buffer)){
    memcpy(buffer, data, size);
    return 1;
    }
    
    return 0;
    
}
 //& "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Tools\Llvm\x64\bin\clang.exe" -g "-fsanitize=fuzzer,address" target.c fuzz_target.c -o fuzzer.exe
#include <stdio.h>
#include <string.h>

int main() {
    char num1_str[50], num2_str[50], result_str[51]; 
    int carry = 0;
    int max_length;
    printf("Enter the first integer: ");
    fgets(num1_str, sizeof(num1_str), stdin);
    printf("Enter the second integer: ");
    fgets(num2_str, sizeof(num2_str), stdin);
    num1_str[strcspn(num1_str, "\n")] = '\0';
    num2_str[strcspn(num2_str, "\n")] = '\0';

    max_length = (strlen(num1_str) > strlen(num2_str)) ? strlen(num1_str) : strlen(num2_str);
    result_str[max_length + 1] = '\0';
    int i, j, k;
    for (i = strlen(num1_str) - 1, j = strlen(num2_str) - 1, k = max_length; i >= 0 || j >= 0; i--, j--, k--) {
        int digit1 = (i >= 0) ? num1_str[i] - '0' : 0;
        int digit2 = (j >= 0) ? num2_str[j] - '0' : 0;
        int sum = digit1 + digit2 + carry;

        carry = sum / 10;
        result_str[k] = (sum % 10) + '0';
    }
    if (carry > 0) {
        result_str[0] = carry + '0';
        printf("Sum of %s and %s is %s\n", num1_str, num2_str, result_str);
    } else {
        printf("Sum of %s and %s is %s\n", num1_str, num2_str, result_str + 1);
    }

    return 0;
}

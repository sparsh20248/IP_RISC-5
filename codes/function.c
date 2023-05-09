int addition(int a, int b) {
    return a + b;
}
int substraction(int a, int b) {
    return a - b;
}
int multiply(int a, int b) {
    return a * b;
}
int division(int a, int b) {
    return a / b;
}
int main() {
    int a = 165;
    int b = 15;
    int add = addition(a, b);
    int sub = substraction(a, b);
    int mul = multiply(a, b);
    int div = division(a, b);
}
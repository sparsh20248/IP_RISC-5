int fib(int number) {
    if(number == 0) {
        return 0;
    }
    return number + fib(number - 1);
}

int main() {
    int counter = 10;
    int result = fib(counter);
}
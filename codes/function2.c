int fib(int number) {
    if(number == 0) {
        return 0;
    }
    int answer = number + fib(number - 1);
    return answer;
}

int main() {
    int counter = 10;
    int result = fib(counter);
}
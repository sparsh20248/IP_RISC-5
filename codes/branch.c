int main() {
    int a = 5;
    int b = 6;
    int c = a + b;
    if( c > 10 ) {
        c = 2*b + a;
    } else {
        c = 2*a + b;
    }
}
int dp[10];
int arr[10];
int recursion(int counter) {
    if(counter == -1) return 1;
    dp[counter] = arr[counter] * recursion(counter - 1);
    return dp[counter];
}

int main() {
    arr[0] = 1;
    arr[1] = 2;
    arr[2] = 4;
    arr[3] = 8;
    arr[4] = 16;
    arr[5] = 32;
    arr[6] = 64;
    arr[7] = 128;
    arr[8] = 256;
    arr[9] = 512;
    int result = recursion(9);
}
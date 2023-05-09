int main() {
    int arr[5];
    arr[0] = 100;
    arr[1] = 200;
    arr[2] = 50;
    arr[3] = 300;
    arr[4] = 150;
    int flag = (arr[0]*arr[1] + arr[3] - arr[4] )/ arr[2];

    if(flag < arr[0]) {
        arr[0] = arr[0] + arr[1];
    } else {
        arr[0] = arr[0] + arr[2];
    }
}
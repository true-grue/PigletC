int n;
int a;
int b;
int i;
int t;

void main() {
  a = 0;
  b = 1;
  i = 0;
  n = 20;
  while (i < n) {
    t = a;
    a = b;
    b = t + b;
    i = i + 1;
  }
  print(a);
}

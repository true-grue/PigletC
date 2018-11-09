int r;
int n;

void main() {
  n = 5;
  r = 1;
  while (n > 1) {
    r = r * n;
    n = n - 1;
  }
  print(r);
}

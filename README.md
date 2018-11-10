# PigletC

A tiny C-like language compiler for [PigletVM](https://github.com/vkazanov/bytecode-interpreters-post). The compiler was made for teaching purposes.

PigletC is based on [raddsl](https://github.com/true-grue/raddsl) toolset.

An example of use.

```
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
```

```
PUSHI 1
PUSHI 5
STORE
PUSHI 0
PUSHI 1
STORE
L0:
PUSHI 1
LOAD
PUSHI 1
GREATER
JUMP_IF_FALSE L1
PUSHI 0
PUSHI 0
LOAD
PUSHI 1
LOAD
MUL
STORE
PUSHI 1
PUSHI 1
LOAD
PUSHI 1
SUB
STORE
JUMP L0
L1:
PUSHI 0
LOAD
PRINT
DONE
```

```
pigletvm-exec asm fact.c.pvm fact.c.b
pigletvm-exec run fact.c.b
120
Result value: 0
PROFILE: switch code finished took 0ms
120
Result value: 0
PROFILE: switch code (no range check) finished took 1ms
120
Result value: 0
PROFILE: threaded code finished took 0ms
120
Result value: 0
PROFILE: trace code finished took 1ms
```

#include <stdio.h>
#include "phase_detector.h"

int access_many() {
     PhaseDetector pd(0.5, 100, 10, 3);
     return 0;
}

int main() {
    access_many();
}

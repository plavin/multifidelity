mm: matmul-openmp.c
		gcc -fopenmp -o mm matmul-openmp.c
mm-asm: matmul-openmp.c
		gcc -S -fverbose-asm -fopenmp -o mm-asm matmul-openmp.c
mm-nosimd: matmul-openmp.c
		gcc -mno-sse -mno-avx -fopenmp -o mm-nosimd matmul-openmp.c
mm-noopt: matmul-openmp.c
		gcc -O0 -mno-sse -mno-avx -fopenmp -o mm-noopt matmul-openmp.c

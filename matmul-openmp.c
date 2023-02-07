#include <stdlib.h>
#include <stdio.h>
#include <assert.h>

typedef double dtype;

void ariel_enable() {
    printf("ARIEL-CLIENT: Library enabled.\n");
}

void fill(dtype *a, int N, double f) {
    for (int i = 0; i < N*N; i++) {
        a[i] = f;
    }
}

// Source: https://github.com/dmitrydonchenko/Block-Matrix-Multiplication-OpenMP/blob/master/block_matrix/Source.cpp
void block_matrix_mul_parallel(dtype *A, dtype *B, dtype *C, int size, int block_size)
{
    int i = 0, j = 0, k = 0, jj = 0, kk = 0;
    dtype tmp;
    int chunk = 1;
#pragma omp parallel shared(A, B, C, size, chunk) private(i, j, k, jj, kk, tmp)
    {
        //omp_set_dynamic(0);
        //omp_set_num_threads(4);
        #pragma omp for schedule (static, chunk)
        for (jj = 0; jj < size; jj += block_size)
        {
            for (kk = 0; kk < size; kk += block_size)
            {
                for (i = 0; i < size; i++)
                {
                    for (j = jj; j < ((jj + block_size) > size ? size : (jj + block_size)); j++)
                    {
                        tmp = 0.0f;
                        for (k = kk; k < ((kk + block_size) > size ? size : (kk + block_size)); k++)
                        {
                            tmp += A[i*size+k] * B[k*size+j];
                        }
                        C[i*size+j] += tmp;
                    }
                }
            }
        }
    }
}

int main(int argc, char** argv) {

    dtype *a, *b, *c, temp = 0;
    int N, s;

    if (argc < 3) {
        printf("Too few arguments.\n");
        printf("Usage: %s <matrix dimension> <block size>\n", argv[0]);
        exit(1);
    }

    N = atoi(argv[1]);
    s = atoi(argv[2]);

    if ( s > N || (N % s != 0)) {
        printf("Invalid arguments. Block size must divide matrix dimension.\n");
        exit(1);
    }

    a = (dtype*)malloc(sizeof(dtype) * N * N);
    b = (dtype*)malloc(sizeof(dtype) * N * N);
    c = (dtype*)malloc(sizeof(dtype) * N * N);

    fill(a, N, 3);
    fill(b, N, 2);
    fill(c, N, 0);

    ariel_enable();

    /*
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
#pragma omp parallel for
            for (int k = 0; k < N; k++) {
#pragma omp critical
                c[i*N + j] += a[i*N + k] * b[k*N + j];
            }
        }
    }
    */
    block_matrix_mul_parallel(a, b, c, N, s);

    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            printf("%.0lf ", c[i*N+j]);
        }
        printf("\n");
    }

}

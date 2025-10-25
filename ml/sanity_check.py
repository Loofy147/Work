import numpy as np

def main():
    print("Running environment sanity check...")
    try:
        A = np.array([[1, 2], [3, 4]])
        B = np.array([[5, 6], [7, 8]])
        C = np.dot(A, B)
        print("Matrix multiplication successful.")
        print("Result:")
        print(C)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
